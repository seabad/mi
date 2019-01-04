# -*- coding: utf-8 -*-
import scrapy, uuid
from mi.items import LorealProductItem 

class LorealSpider(scrapy.Spider):
    name = 'loreal'
    allowed_domains = ['www.lorealparis.com.cn']

    def start_requests(self):
        #url filename = 'quotes-%s.html' % page
        urls = []
        
        for i in range(1,8):
            url_link = 'http://www.lorealparis.com.cn/SkinCare/SubCategory/-1.loreal?pageindex=%s' % i
            urls.append(url_link)
        for i in range(1,5):
            url_link = 'http://www.lorealparis.com.cn/HairCare/SubCategory/-1.loreal?pageindex=%s' % i
            urls.append(url_link)
        
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
            
            
    def parse(self, response):
        
        #获取所有product list
        for product in response.css("div.product-list li"): 
            item = LorealProductItem()
            #获取图片地址
            item['imgurl'] = response.urljoin(product.css("div.product-img img::attr(src)").extract_first())
            item['imgname'] = uuid.uuid1() #给图片重命名
            item['title'] = product.css("div.caption-title::text").extract_first().strip() 
            item['subtitle'] = product.css("div.caption-subtitle a::text").extract_first().strip()
            item['attr'] = product.css("p::text").extract_first().strip()
            item['price'] = product.css("p.price::text").extract_first().strip()
            yield item