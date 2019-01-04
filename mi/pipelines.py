# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import re


class MiPipeline(object):
          
    def open_spider(self, spider):
        self.file = open('product.csv', 'wb')
        self.exporter = CsvItemExporter(self.file,
        fields_to_export=['title',
                          'subtitle',
                          'imgurl',
                          'imgname',
                          'attr',
                          'price',
                          ])
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if item['title'] is not None:
            self.exporter.export_item(item)
            return item
        else:
            raise DropItem('Item without title: %s' % item)

class LorealImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['imgurl']:
            yield Request(image_url,meta={'item':item['imgname']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        image_guid = request.url.split('/')[-1]
        # name2 = request.url.split('/')[-2]
        filename = u'full/{0}'.format(image_guid)
        return filename
        # return 'full/%s' % (image_guid)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item