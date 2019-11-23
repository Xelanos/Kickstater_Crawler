import scrapy
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from w3lib.html import remove_tags
import time
import json
from datetime import datetime
import math

from CreepyCrawlers.items import TechProject, Reward


class CreepyCrawler(CrawlSpider):
    name = 'CreepyCrawler'
    start_urls = ['https://www.kickstarter.com/discover/advanced?category_id=16']
    allowed_domains = ['kickstarter.com']
    download_delay = 1.5

    def getMoreRequests(self, url):
        driver = webdriver.PhantomJS(executable_path="C:\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        page_num = 0

        while driver.find_element_by_xpath('//*[@id="projects"]/div[4]/a'):
            driver.find_element_by_xpath('//*[@id="projects"]/div[4]/a').click()
            page_num += 1
            print("getting page number " + str(page_num))
            time.sleep(1)
            if page_num == 1:
                break

        return driver.page_source.encode('utf-8')


    def parse(self, response):
        result = []
        # response = scrapy.http.HtmlResponse(response.url, body=self.getMoreRequests(response.url))
        projects = response.xpath('//div/@data-project').getall()
        for project_data_string in projects[:2]:
            project_data = json.loads(project_data_string)
            project = TechProject()
            project['id'] = project_data['id']
            project['Creator'] = project_data['creator']
            project['url'] = project_data['urls']['web']['project']
            project['Title'] = 1  #TODO
            project['Text'] = 3 #TODO
            project['NumBackers'] = project_data['backers_count']
            project['DaysToGo'] = self.calculate_days(project_data['deadline'])
            project['DollarsPleged'] = project_data['converted_pledged_amount']
            project['DollarsGoal'] = math.floor(project_data['goal'] * project_data['fx_rate'])
            project['AllOrNothing'] = 2 #TODO

            yield scrapy.Request(project_data['urls']['web']['rewards'], callback=self.parse_rewerds, meta={'project': project})

    def calculate_days(self, timestamp):
        d_time = datetime.fromtimestamp(timestamp)
        return (d_time - datetime.now()).days


    def parse_rewerds(self, response):
        project = response.meta['project']
        rewards = []
        for reward_html in response.xpath('//li[@class="hover-group js-reward-available pledge--available pledge-selectable-sidebar"]'):
            print(reward_html.get())
            reward = Reward()
            reward['Text'] = '1'
            reward['Price'] = remove_tags(reward_html.xpath('/h2/span[1]').get()).strip()
            reward['NumBackers'] = remove_tags(reward_html.xpath('.//[@class="pledge__backer-count"]').get()).strip().split(' ', 1)[0]
            rewards.append(reward)
        project['rewards'] = rewards
        return project


def parse_item(response):
    project = TechProject()
    project['url'] = response.url
    project['Title'] = response.xpath('//title/text()').get().strip()
    project['Title'] = response.xpath('//title/text()').get().strip()
    project['NumBackers'] = remove_tags(response.xpath('//*[@id="react-project-header"]/div/div/div[3]/div/div[2]/div[2]/div/span').get())
    project['DaysToGo'] = remove_tags(response.xpath('//*[@id="react-project-header"]/div/div/div[3]/div/div[2]/div[3]/div/div/span[1]').get())
    project['DollarsPleged'] = remove_tags(response.xpath('//*[@id="react-project-header"]/div/div/div[3]/div/div[2]/div[1]/div[2]/span/span').get())
    project['DollarsGoal'] = remove_tags(response.xpath('//*[@id="react-project-header"]/div/div/div[3]/div/div[2]/div[1]/span/span[2]/span').get())
    project['AllOrNothing'] = remove_tags(response.xpath('//*[@id="react-project-header"]/div/div/div[3]/div/div[2]/div[1]/span/span[2]/span').get())
    project['rewards'] = response.xpath('//*[@class="NS_projects__rewards_list js-project-rewards"]').getall()
    print(project)
    return project