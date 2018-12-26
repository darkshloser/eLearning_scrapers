# -*- coding: utf-8 -*-
import scrapy


class ClassCentralSpider(scrapy.Spider):
    name = 'class-central'
    allowed_domains = ['class-central.com']
    start_urls = ['http://class-central.com/']

    def parse(self, response):
        pass
