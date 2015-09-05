import scrapy


class RetrievalSpider(scrapy.Spider):
    name = "retrieval"
    start_urls = [
        "http://www.scopus.com/results/results.url?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1=CLIMATIC EFFECTS ON THE PHENOLOGY OF GEOPHYTES&field1=TITLE&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&subjects=LFSC&subjects=HLSC&subjects=PHSC&subjects=SOSC&src=s&st1=CLIMATIC EFFECTS ON THE PHENOLOGY OF GEOPHYTES&st2=&sot=b&sdt=b&sl=&s=TITLE%28CLIMATIC EFFECTS ON THE PHENOLOGY OF GEOPHYTES%29&sid=&searchId=&txGid=&sort=plf-f&originationType=b&rr=&null="
    ]

    def parse(self, response):
        url = response.xpath('//a[@title="Show document details"]/@href').extract()
        request = scrapy.Request(url[0], callback=self.parse_next)
        return request

    def parse_next(self, response):

        print "\n\n#############################   hei #############################\n\n\n\n"

        abstract = response.xpath('//p[@id="recordAbs"]/text()').extract()
        print abstract

        print "\n\n#############################   hei #############################\n\n\n\n"

        f = open("first-retrieval.txt", "w")
        f.write(str(abstract))
        f.close()