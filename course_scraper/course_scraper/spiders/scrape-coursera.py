# -*- coding: utf-8 -*-
import scrapy
import csv
from course_scraper.items import CourseItem, AcademyItem


class CourseraSpider(scrapy.Spider):
    name = 'scrape-coursera'
    allowed_domains = ['coursera.org']
    start_urls = ['https://www.coursera.org/about/partners/']

    def parse(self, response):
        academies = response.xpath('//div[@class="rc-PartnerBoxes horizontal-box wrap"]/div[@class="rc-PartnerBox vertical-box"]/a/@href').extract()
        for academy in academies:
            academy_csv = open("academy.csv", "a+")
            fieldnames = ['title', 'description', 'logo', 'banner']
            academy_writer = csv.DictWriter(academy_csv, fieldnames=fieldnames)
            course_csv = open("course.csv", "a+")
            fieldnames = ['title', 'description', 'logo', 'banner']
            course_writer = csv.DictWriter(course_csv, fieldnames=fieldnames)
            tutors_csv = open("tutors.csv", "a+")
            fieldnames = ['title', 'description', 'logo', 'banner']
            tutors_writer = csv.DictWriter(tutors_csv, fieldnames=fieldnames)
            item = AcademyItem()
            abs_url = response.urljoin(academy)
            request = scrapy.Request(abs_url, callback=self.parseDetails)
            request.meta['item'] = item
            request.meta['academy_csv'] = academy_csv
            request.meta['course_csv'] = course_csv
            request.meta['tutors_csv'] = tutors_csv
            request.meta['academy_writer'] = academy_writer
            request.meta['course_writer'] = course_writer
            request.meta['tutors_writer'] = tutors_writer
            yield request

    def parseDetails(self, response):
        self.academy_details(response)
        pass

    def academy_details(self, response):
        academy_writer = response.meta['academy_writer']
        title = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="partnerText bt3-col-sm-9"]/h1/text()').extract()
        description = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="partnerText bt3-col-sm-9"]/p/text()').extract()
        logo = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="bt3-col-sm-3"]/div[@class="partnerLogo"]/img/@src').extract()
        banner = response.xpath("//div[contains(@class, 'partnerBanner')]//@style").re_first(r'url\(([^\)]+)')
        academy_writer.writerow({'title': str(title), 'description': str(description), 'logo': str(logo), 'banner': str(banner)})
        # self.course_details(response)
    #
    # def course_details(self, response):
    #     course_writer = response.meta['course_writer']
    #     course_csv = response.meta['course_csv']
    #     courses = response.xpath('//div[@class="bt3-col-md-12"]/div[@class="rc-Course"]/a/@href').extract()
    #     course_picture = response.xpath('//div[@class="bt3-col-md-12"]/div[@class="rc-Course"]/a/img/@src').extract()[0]
    #     i = 1
    #     for course in courses:
    #         print("------------------------")
    #         course_url = response.urljoin(course)
    #         print(course_url)
    #         response_course scrapy.Request(course_url, callback=self.parseCourseDetails)
    #         title = response.xpath('//div[@class="bt3-container banner-container"]/div/div[@class="bt3-col-sm-9 bt3-col-sm-offset-3 header-container"]/h1[@class="title display-3-text"]/text()')
    #         course_writer.writerow({'title': title})
    #         yield response_course
    #         # request_course.meta['course_picture'] = response.xpath('//div[@class="bt3-col-md-12"]/div[@class="rc-Course"]/a/img['+str(i)+']/@src').extract()[0]
    #         # request_course.meta['course_csv'] = course_csv
    #         # request_course.meta['course_writer'] = course_writer
    #         # return request_course
    #
    #
    # def parseCourseDetails(self, response):
    #     print("klkkk+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     course_writer = response.meta['course_writer']
    #     course_picture = response.meta['course_picture']
    #     title = response.xpath('//div[@class="partnerInfo bt3-container"]/div/div[@class="partnerText bt3-col-sm-9"]/h1/text()').extract()[0]
    #     course_writer.writerow({'pic': 'jhkfjdshk'})
    #     # item =CourseScraperItem()
    #     # item['title'] = response.xpath('//div[@class="rc-PartnerBoxes horizontal-box wrap"]/div[@class="rc-PartnerBox vertical-box"]/a/@href').extract()
    #     # return item
    #
    #




#ldks;
