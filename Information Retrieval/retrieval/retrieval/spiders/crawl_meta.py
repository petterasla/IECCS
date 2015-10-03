import scrapy
import re
import json
import import_data
from retrieval.items import MetaItem

class MetaSpider(scrapy.Spider):
    name = "meta retrieval"
    start_urls = import_data.generateMetaURLs()[9000:]

    def parse(self, response):
        item = MetaItem()
        metaString = re.sub('<[^>]*>', '', response.xpath('//body/p/text()').extract()[0])
        jsonMetaString = "[" + str(metaString) + "]"

        metaDict = json.loads(jsonMetaString)[0]
        item["status"] = metaDict["status"]
        item["message"] = metaDict["message"]

        yield item

