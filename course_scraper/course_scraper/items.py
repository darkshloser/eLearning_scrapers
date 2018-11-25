# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AcademyItem(Item):
    academy_title = Field()
    academy_description = Field()
    academy_logo = Field()
    academy_banner = Field()
    # academy_url = Field()
    # courses = Field()


class CourseItem(Item):
    course_title = Field()
    course_description = Field()
    course_rating = Field()
    course_tutors = Field()
    course_duration = Field()
    course_part_of_program = Field()
