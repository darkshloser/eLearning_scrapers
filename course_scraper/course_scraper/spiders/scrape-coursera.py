# -*- coding: utf-8 -*-
import scrapy
import csv
from course_scraper.items import CourseItem, AcademyItem


class CourseraSpider(scrapy.Spider):
    name = 'scrape-coursera'
    allowed_domains = ['coursera.org']
    start_urls = ['https://www.coursera.org/about/partners/']

    def parse(self, response):
        sel = scrapy.Selector(response)
        # store all the information into *.csv files
        academy_csv = open("academy.csv", "a+")
        fieldnames = ['platform', 'title', 'description', 'logo', 'banner']
        academy_writer = csv.DictWriter(academy_csv, fieldnames=fieldnames)
        course_csv = open("course.csv", "a+")
        fieldnames =  [
                      'platform', 'issuer', 'title', 'about', 'purpose',
                      'tutors', 'level', 'duration', 'language', 'stars',
                      'logo', 'banner', 'link'
                      ]
        course_writer = csv.DictWriter(course_csv, fieldnames=fieldnames)
        specialization_csv = open("specialization.csv", "a+")
        fieldnames =  ['platform', 'issuer', 'title', 'about', 'courses']
        specialization_writer = csv.DictWriter(
                                               course_csv,
                                               fieldnames=fieldnames)
        tutors_csv = open("tutors.csv", "a+")
        fieldnames = ['title', 'description', 'logo', 'banner']
        tutors_writer = csv.DictWriter(tutors_csv, fieldnames=fieldnames)

        item = AcademyItem()
        academies = sel.xpath('//div[@class="rc-PartnerApp"]/div[1]/div[2]/div[2]/div/a/@href').extract()
        for academy in academies:
            abs_url = response.urljoin(academy)
            request = scrapy.Request(abs_url, callback=self.academy_details)
            request.meta['item'] = item
            request.meta['academy_csv'] = academy_csv
            request.meta['specialization_csv'] = specialization_csv
            request.meta['course_csv'] = course_csv
            request.meta['tutors_csv'] = tutors_csv
            request.meta['academy_writer'] = academy_writer
            request.meta['course_writer'] = course_writer
            request.meta['specialization_writer'] = specialization_writer
            request.meta['tutors_writer'] = tutors_writer
            yield request

    def return_val(self, arg):
        if isinstance(arg, str):
            return arg
        elif isinstance(arg, list):
            if len(arg) > 0:
                return arg[0]
        return ''

    def academy_details(self, response):
        academy_writer = response.meta['academy_writer']
        course_writer = response.meta['course_writer']
        title = response.xpath('//div[@class="rc-PartnerHeader"]/div[2]/div/div[2]/h1/text()').extract()
        description = response.xpath('//div[@class="rc-PartnerHeader"]/div[2]/div/div[2]/p/text()').extract()
        logo = response.xpath('//div[@class="rc-PartnerHeader"]/div[2]/div/div[1]/div/img/@src').extract()
        banner = response.xpath("//div[@class='rc-PartnerHeader']/div[1]//@style").re_first(r'url\(([^\)]+)')
        title = self.return_val(title)
        description = self.return_val(description)
        logo = self.return_val(logo)
        banner = self.return_val(banner)
        academy_writer.writerow({'title': str(title),
                                 'description': str(description),
                                 'logo': str(logo),
                                 'banner': str(banner)})
        courses = response.xpath('//div[@class="rc-PartnerApp"]/div[1]/div[2]/div[1]/div/div/a/@href').extract()
        course_logo = response.xpath('//div[@class="rc-PartnerApp"]/div[1]/div[2]/div[1]/div[1]/div/a/img/@src').extract()
        for idx, course in enumerate(courses):
            course_url = response.urljoin(course)
            request_course = scrapy.Request(course_url, callback=self.parseCourseDetails)
            request_course.meta['course_writer'] = course_writer
            request_course.meta['specialization_writer'] = specialization_writer
            request_course.meta['course_logo'] = course_logo[idx]
            yield request_course


    def parseCourseDetails(self, response):
        course_writer = response.meta['course_writer']
        specialization_writer = response.meta['specialization_writer']
        course_logo = response.meta['course_logo']
        title = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[2]/div[1]/main/div[1]/h1/span/text()').extract()
        is_specialization = True if len(response.xpath("//*[contains(@id, 'courses')]")) else False
        if is_specialization:
            print("SPECIALIZATION")
            # 'platform', 'issuer', 'title', 'about', 'courses'

        else:
            print("COURSE")
            issuer = about = table = level = duration = language = stars = ""
            # 'platform', 'issuer', 'title', 'about', 'purpose',
            # 'tutors', 'level', 'duration', 'language', 'stars',
            # 'logo', 'banner', 'link'
            banner = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[1]//@style').re_first(r'url\(([^\)]+)')
            issuer = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/span/text()').extract()
            about = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/p/text()').extract()
            table = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[5]/table/tbody/tr/td/span/text()').extract()
            table_elements = ['Level', 'Language', 'Commitment', 'User Ratings']
            for item in table_elements:
                item_index = [i for i, s in enumerate(table) if item in s]
                if item != 'User Ratings':
                    item_value = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[5]/table/tbody/tr['+str(item_index[0])+']/td[2]/text()').extract()
                else:
                    item_value = response.xpath('//div[@id="rendered-content"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[5]/table/tbody/tr['+str(item_index[0])+']/td[2]/div/div/span[1]/text()')[1].extract()

                if item == 'Level':
                    level = item_value
                elif item == 'Language':
                    language = item_value
                elif item == 'Commitment':
                    duration = item_value
                elif item == 'User Ratings':
                    stars = item_value
            course_writer.writerow({'platform': 'Coursera',
                                    'issuer': str(issuer),
                                    'title': str(title),
                                    'about': str(about),
                                    'level': str(level),
                                    'duration': str(duration),
                                    'language': str(language),
                                    'stars': str(stars),
                                    'logo': str(course_logo),
                                    'banner': str(banner),
                                    'link': str(response.url)})

#ldks;
