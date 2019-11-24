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
    ITEM_PIPELINES = {'CreepyCrawlers.pipelines.CreepycrawlersPipeline': 300}
    custom_settings = {'ITEM_PIPELINES': ITEM_PIPELINES}

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
            if page_num == 80:
                break

        return driver.page_source.encode('utf-8')


    def parse(self, response):
        result = []
        response = scrapy.http.HtmlResponse(response.url, body=self.getMoreRequests(response.url))
        projects = response.xpath('//div/@data-project').getall()
        for project_data_string in projects:
            project_data = json.loads(project_data_string)
            project = TechProject()
            project['id'] = project_data['id']
            project['Creator'] = project_data['creator']
            project['url'] = project_data['urls']['web']['project']
            project['NumBackers'] = project_data['backers_count']
            project['DaysToGo'] = self.calculate_days(project_data['deadline'])
            project['DollarsPleged'] = project_data['converted_pledged_amount']
            project['DollarsGoal'] = math.floor(project_data['goal'] * project_data['fx_rate'])
            project['AllOrNothing'] = True

            yield scrapy.Request(project_data['urls']['web']['project'], callback=self.parse_item, meta={'project': project})

    def calculate_days(self, timestamp):
        d_time = datetime.fromtimestamp(timestamp)
        return (d_time - datetime.now()).days


    def parse_item(self, response):
        project = response.meta['project']
        project['Title'] = response.xpath('//title/text()').get().strip()
        project['Text'] = response.text

        project['rewards'] = self.get_rewards(response)
        return project

    def get_rewards(self, response):
        #TODO
        pass