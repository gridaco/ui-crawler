# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MobbinItem(scrapy.Item):
    url = scrapy.Field()
    app_name = scrapy.Field()
    app_desc = scrapy.Field()
    app_url = scrapy.Field()
    category = scrapy.Field()
    mobbin_patterns = scrapy.Field()
    mobbin_elements = scrapy.Field()

    # image_id = scrapy.Field()
    # file_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

