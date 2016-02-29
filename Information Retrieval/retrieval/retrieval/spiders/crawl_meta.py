import scrapy
from scrapy.pipelines.files import FilesPipeline
import re
import json
import import_data as import_data
from retrieval.items import MetaItem

class MetaSpider(scrapy.Spider):
    name = "meta retrieval"
    start_urls = import_data.generateSearchURLs()[:2]

    def parse(self, response):
        item = MetaItem()
        url = response.xpath('//a[@title="Show document details"]/@href').extract()[0]
        print 80 * "="
        print "URL"
        print 80 * "="
        print url
        print 80 * "#"
        request = scrapy.Request(url, callback=self.parse_next)
        request.meta['item'] = item

        return request

    def parse_next(self, response):
        item = response.meta['item']
        url = response.url
        start_index = url.index("eid=") + 4
        end_index = url.index("&", start_index)
        eid = url[start_index:end_index]
        print 80 * "="
        print "EID"
        print 80 * "="
        print eid
        print 80 * "#"
        item['url'] = import_data.generateMetaURL(eid)
        yield FilesPipeline(item['url'])
