# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request


class MiPipeline(object):
          
    def open_spider(self, spider):
        self.file = open('LorealProductInfo.csv', 'wb')
        self.exporter = CsvItemExporter(self.file,
        fields_to_export=['title',
                          'subtitle',
                          'image_urls',
                          'image_paths',
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
            raise DropItem('Drop item without title')

class LorealProductInfoPipeline(object):
          
    def open_spider(self, spider):
        self.file = open('LorealProductInfo.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
            
class LorealProductImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url = image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_paths
        return item