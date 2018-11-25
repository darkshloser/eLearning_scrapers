# -*- coding: utf-8 -*-
import scrapy
from course_scraper.items import CourseItem, AcademyItem


class ClassCentralSpider(scrapy.Spider):
    name = 'scrape-classcentral'
    allowed_domains = ['class-central.com']
    start_urls = ['https://www.class-central.com/universities']

    def parse(self, response):
        academies = response.xpath('//div[@class="universities"]/table/tbody//div[@class="rc-PartnerBox vertical-box"]/a/@href').extract()
        i = 1
        for academy in academies:
            abs_url = response.urljoin(academy)
            yield scrapy.Request(abs_url, callback=self.academy_details)


    def academy_details(self, response):
        academy_item =AcademyItem()
        academy_item['academy_title'] = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="partnerText bt3-col-sm-9"]/h1/text()').extract()
        academy_item['academy_description'] = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="partnerText bt3-col-sm-9"]/p/text()').extract()
        academy_item['academy_logo'] = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="bt3-col-sm-3"]/div[@class="partnerLogo"]/img/@src').extract()
        academy_item['academy_banner'] = response.xpath("//div[contains(@class, 'partnerBanner')]//@style").re_first(r'url\(([^\)]+)')
        return academy_item

    def course_details(self, response):
        pass

        # item =CourseScraperItem()
        # item['title'] = response.xpath('//div[@class="rc-PartnerBoxes horizontal-box wrap"]/div[@class="rc-PartnerBox vertical-box"]/a/@href').extract()
        # return item
