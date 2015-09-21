import scrapy
from retrieval.items import RetrievalItem
import getArticleTitle

# Retrieve abstracts from the scopus web-page
class RetrievalSpider(scrapy.Spider):
    name = "abstract retrieval"
    allowed_domains = ["scopus.com"]
    #titles = getArticleTitle.getArticleInfo("tcp_articles.txt")
    start_urls = getArticleTitle.generateSearchURLs()[0:30]

    def parse(self, response):
        item = RetrievalItem()
        item['url'] = response.xpath('//a[@title="Show document details"]/@href').extract()[0]
        item["Abstract title"] = response.xpath('//span[@class="docTitle"]/a/text()').extract()[0].encode('ascii', 'ignore')
        request = scrapy.Request(item['url'], callback=self.parse_next)
        request.meta['item'] = item

        print "\n\n#############################   hei #############################\n\n\n\n"
        print "\n\n#############################   hei #############################\n\n\n\n"
        return request

    def parse_next(self, response):
        item = response.meta['item']
        print response.xpath('//h1[@class="txtTitle svTitle marginT2 marginB7"]/text()').extract()
        item['abstract'] = response.xpath('//p[@id="recordAbs"]/text()').extract()
        yield item
