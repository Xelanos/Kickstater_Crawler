import scrapy
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
from lxml.html import etree
import time



def getMoreRequests(url):
    driver = webdriver.PhantomJS(
        executable_path="C:\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    page_num = 0

    while driver.find_element_by_xpath('//*[@class="load_more mt3"]/a'):
        break
        driver.find_element_by_xpath(
            '//*[@class="load_more mt3"]/a').click()
        page_num += 1
        print("getting page number " + str(page_num))
        time.sleep(1)
        if page_num == 1:
            break

    return driver.page_source.encode('utf-8')

response = getMoreRequests('https://www.kickstarter.com/discover/advanced?category_id=16')

htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)




soup = BeautifulSoup(response, 'html.parser')
# projects_grid = soup.find('div', id="projects")
projects = soup.find_all('div',  {"class": "js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg"})

for project in projects:
    print(project['data-projects'])

## '//div[contains(@data-project)]/@data-project').getall()