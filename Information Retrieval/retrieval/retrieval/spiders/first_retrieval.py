import scrapy
from retrieval.items import RetrievalItem
import getArticleTitle

# Retrieve abstracts from the scopus web-page
class RetrievalSpider(scrapy.Spider):
    name = "abstract retrieval"
    allowed_domains = ["scopus.com"]
    titles = getArticleTitle.getArticleInfo("tcp_articles.txt")
    start_urls = getArticleTitle.generateSearchURLs()[10]

    def parse(self, response):
        item = RetrievalItem()
        item['url'] = response.xpath('//a[@title="Show document details"]/@href').extract()[0]
        request = scrapy.Request(item['url'], callback=self.parse_next)
        request.meta['item'] = item
        return request

    def parse_next(self, response):
        item = response.meta['item']
        print "\n\n#############################   hei #############################\n\n\n\n"

        item['abstract'] = response.xpath('//p[@id="recordAbs"]/text()').extract()
        print item['abstract']

        print "\n\n#############################   hei #############################\n\n\n\n"

        yield item

        """f = open("first-retrieval.txt", "w")
        f.write(str(abstract))
        f.close()"""