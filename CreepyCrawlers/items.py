# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CreepycrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Reward(scrapy.Item):
    Text = scrapy.Field()
    Price = scrapy.Field()
    NumBackers = scrapy.Field()

class TechProject(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    Creator = scrapy.Field()
    Title = scrapy.Field()
    Text = scrapy.Field()
    DollarsPleged = scrapy.Field()
    DollarsGoal = scrapy.Field()
    NumBackers = scrapy.Field()
    DaysToGo = scrapy.Field()
    AllOrNothing = scrapy.Field()
    rewards = scrapy.Field()


