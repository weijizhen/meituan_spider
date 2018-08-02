# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    #商品名字
    name = scrapy.Field()
    #地址
    address = scrapy.Field()
    #电话
    phone = scrapy.Field()
    #图片
    img1 = scrapy.Field()
    #图片
    img2 = scrapy.Field()
    #菜品
    Dishes = scrapy.Field()
    #城市
    city = scrapy.Field()



