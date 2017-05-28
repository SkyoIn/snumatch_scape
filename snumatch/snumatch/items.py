# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SnumatchItem(scrapy.Item):
    id = scrapy.Field()
    nick_name = scrapy.Field()
    email = scrapy.Field()
    gender = scrapy.Field()
    birthyear = scrapy.Field()
    graduate = scrapy.Field()
    location = scrapy.Field()
    phone_number = scrapy.Field()
    intro_text = scrapy.Field()
    image_url = scrapy.Field()
