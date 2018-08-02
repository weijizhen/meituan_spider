# -*- coding: utf-8 -*-
import scrapy

import re

from Mt.items import MtItem
from scrapy.conf import settings
from scrapy.spider import Spider
from scrapy.http import Request
import os

class MtSpider(scrapy.Spider):
    name = "mt"
    allowed_domains = ["meituan.com"]
    offst = 1
    url = 'http://hz.meituan.com/meishi/pn'
    p = '/'
    start_urls = [
        url +str(offst)+p
    ]

    cookie = settings['COOKIE']  # 带着Cookie向网页发请求,发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302],  # 对哪些异常返回进行处理
    }

    def parse(self, response):
            html =re.findall(r'["poiId":]{8}([0-9]+),["frontImg":"]',response.text,re.S)#这是获取一页中的商店ID
            for htmls in html:
                poiId_Url = 'http://hz.meituan.com/meishi/'+str(htmls)+'/'
                yield scrapy.Request(poiId_Url,cookies=self.cookie,
                    headers=self.headers, meta=self.meta,callback= self.get_htmls)
            if self.offst <=1:
                self.offst +=1
            yield scrapy.Request(self.url+str(self.offst)+self.p,callback=self.parse,cookies=self.cookie,headers=self.headers,meta=self.meta)
    def get_htmls(self,response):
        Item = MtItem()
        # 店名
        Item['name'] = re.search('["poiId":]{8}([0-9]+),"name":"(.*?)","avgScore"', response.text, re.S).group(2)
        # 地址
        Item['address'] = re.search('"address":"(.*?)","phone":"', response.text, re.S).group(1)
        # 电话
        Item['phone'] = re.findall(r'["phone":"]{9}(.*?)[","openTime":"]{14}(.*?)["]', response.text, re.S)
        #彩品
        Item['Dishes'] = re.findall(r'","name":"(.*?)","price":',response.text, re.S)
        #1张图片
        Item['img1'] = re.search('"frontImgUrl":"(.*?)","albumImgUrls":', response.text, re.S).group(1)
        #1张图片
        Item['img2'] = re.search('"albumImgUrls":\["(.*?)","http:', response.text, re.S).group(1)
        #城市
        Item['city'] = re.search(',"cityName":"(.*?)","userName":"","title":"',response.text,re.S).group(1)
        yield Item


