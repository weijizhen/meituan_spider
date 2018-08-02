# -*- coding: utf-8 -*-
import scrapy
import re


from scrapy.conf import settings
from hoelt.items import HoeltItem
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['meituan.com']
    offset = 0
    url='https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=3663AFA62227A87C7B8D924A4A7A61B4E9ED311B50C3C2B08E0A1597707BBE5F%401532745915720&cityId=807&offset='
    urls='&limit=20&startDay=20180728&endDay=20180728&q=&sort=defaults'
    start_urls = [
        url+str(offset)+urls
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
            ids = re.findall('"poiid":(.*?),"cooperationInfo":',response.text,re.S)
            if (ids!=[]):
                for id in ids:
                    url_h = 'http://hotel.meituan.com/'+str(id)+'/'
                    yield scrapy.Request(url_h,cookies=self.cookie,headers=self.headers,meta=self.meta,callback=self.get_url_h_html)

                if self.offset < 60:
                    self.offset +=20
                yield scrapy.Request(self.url+str(self.offset)+self.urls,callback=self.parse)
            else:
                pass

    def get_url_h_html(self,response):
        try:
            Item = HoeltItem()
            # 店名
            Item['name'] = response.xpath("//div/span[@class='fs26 fc3 pull-left bold']/text()").extract()
            if Item['name'].strip()=="":
                print('名字为空')
            # 地址
            Item['address'] = response.xpath('//div//div[@class="fs12 mt6 mb10"]/a[@target="_blank"]/text() | //div[@class="fs12 mt6 mb10"]//span/text()').extract()
            if Item['name'].strip()=="":
                print('地址为空')
            # 电话
            str = response.xpath('//div//div[@class = "mb10"]/text()').extract()[0]
            Item['phone'] = str[3:]

            #图片
            id = re.search(r'\\u002Ftdchotel\\u002F(.*?)\.', response.text).group(1)
            Item['img1'] = 'http://p1.meituan.net/750.0.0/tdchotel/'+id+'.jpg'
            #城市
            Item['city'] = response.xpath('//div//div[@class="breadcrumb-nav"]/a[1]/text()').extract()[0]
            yield Item
        except Exception as e :
            print(e)











        # id = re.findall(r'http://hotel.meituan.com/(.*?)/',response.url,re.S)
        # for ids in id:
        #     img_s = 'https://ihotel.meituan.com/group/v1/poi/' + ids + '/imgs?utm_medium=touch&version_name=999.9&classified=true'
        #     yield  scrapy.Request(img_s, cookies=self.cookie, headers=self.headers, meta=self.meta,callback=self.get_imgs)
    # def get_imgs(self,response):
    #     Item = HoeltItem()
    #     # 1张图片
    #     Item['img1'] = re.search('"http://p1.meituan.net/w.h/tdchotel/(.*?)\.', response.text, re.S).group(1)
    #     # 1张图片
    #     Item['img2'] = re.search('"http://p0.meituan.net/w.h/tdchotel/(.*?)\.', response.text, re.S).group(1)
    #     yield Item
    #     # h6 = re.search('"http://p1.meituan.net/w.h/tdchotel/(.*?)\.', response.text, re.S).group(1)
    #     # h7 = re.search('"http://p0.meituan.net/w.h/tdchotel/(.*?)\.', response.text, re.S).group(1)
