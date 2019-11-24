# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter

class CreepycrawlersPipeline(object):

    def open_spider(self, spider):
        self.file = open('results.jl', 'wb')
        self.exp = JsonItemExporter(self.file, indent=4)
        self.exp.start_exporting()


    def close_spider(self, spider):
        self.exp.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exp.export_item(item)
        return item
