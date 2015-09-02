import scrapy

class RetrievalSpider(scrapy.Spider):
    name = "retrieval"
    start_urls = [
        "http://www.biogeosciences.net/6/1361/2009/bg-6-1361-2009.html"
    ]

    def parse(self, response):
        print "\n\n#############################   hei #############################\n\n\n\n"

        abstract = response.xpath('//span[@class="pb_abstract"]/text()').extract()
        print abstract

        print "\n\n\n\n#############################   Ha det #############################\n\n"

        f = open("first-retrieval.txt", "w")
        f.write(str(abstract))
        f.close()

