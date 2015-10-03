import scrapy
from retrieval.items import RetrievalItem
import import_data

# Retrieve abstracts from the scopus web-page
class RetrievalSpider(scrapy.Spider):
    name = "abstract retrieval"
    allowed_domains = ["scopus.com"]
    #titles = getArticleTitle.getArticleInfo("tcp_articles.txt")
    start_urls = import_data.generateSearchURLs()[10000:]

    def parse(self, response):
        item = RetrievalItem()
        item['url'] = response.xpath('//a[@title="Show document details"]/@href').extract()[0]
        item["title"] = response.xpath('//span[@class="docTitle"]/a/text()').extract()[0].encode('ascii', 'ignore')
        request = scrapy.Request(item['url'], callback=self.parse_next)
        request.meta['item'] = item

        return request

    def parse_next(self, response):
        item = response.meta['item']
        item['abstract'] = response.xpath('//p[@id="recordAbs"]/text()').extract()
        yield item
