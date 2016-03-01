import scrapy
import import_data as import_data
from retrieval.items import MetaRetrievalItem


class CSVSpider(scrapy.Spider):
    name = "csv retrieval"
    print "CSV RETRIEVAL"
    print 80*"="
    start_urls = import_data.generateSearchURLs()[:1]


    def parse(self, response):
        yield MetaRetrievalItem(
                file_urls=import_data.jsonToTextList("meta_url100to1000.json")
        )