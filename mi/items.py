# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LorealProductItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()        
    subtitle = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    attr = scrapy.Field()
    price = scrapy.Field()
    pass