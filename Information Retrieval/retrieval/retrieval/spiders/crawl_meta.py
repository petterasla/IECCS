import scrapy
import import_data as import_data
from retrieval.items import MetaItem


class MetaSpider(scrapy.Spider):
    name = "meta retrieval"
    print "META RETRIEVAL"
    print 80*"="
    start_urls = import_data.generateSearchURLs()[10000:]


    def parse(self, response):
        item = MetaItem()
        url = response.xpath('//a[@title="Show document details"]/@href').extract()[0]
        request = scrapy.Request(url, callback=self.parse_next)
        request.meta['item'] = item
        return request

    def parse_next(self, response):
        item = response.meta['item']
        url = response.url
        start_index = url.index("eid=") + 4
        end_index = url.index("&", start_index)
        eid = url[start_index:end_index]
        item['url'] = import_data.generateMetaURL(eid)
        yield item