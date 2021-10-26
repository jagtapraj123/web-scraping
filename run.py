from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from amazon_product_scraping.spiders.AmazonTop100BSRSpider import AmazonTop100BSRSpider
from amazon_product_scraping.spiders.AmazonSearchListSpider import AmazonSearchListSpider
from amazon_product_scraping.spiders.AmazonProductInfoSpider import AmazonProductInfoSpider
from amazon_product_scraping.spiders.AmazonProductSalePriceBSRSpider import AmazonProductSalePriceBSRSpider
from amazon_product_scraping.spiders.AmazonProductCommentsSpider import AmazonProductCommentsSpider
from amazon_product_scraping.spiders.AmazonShareOfSearchSpider import AmazonShareOfSearchSpider
from scrapy.utils.project import get_project_settings


settings = get_project_settings()
process = CrawlerRunner(settings=settings)

@defer.inlineCallbacks
def run():
    failed_urls = []
    cold_run = True
    for _ in range(10):
        yield process.crawl(AmazonTop100BSRSpider, cold_run=cold_run, failed_urls=failed_urls)
        cold_run = False
        if len(failed_urls) == 0:
            break

    failed_urls = []
    cold_run = True
    for _ in range(10):
        yield process.crawl(AmazonSearchListSpider, cold_run=cold_run, failed_urls=failed_urls)
        cold_run = False
        if len(failed_urls) == 0:
            break

    # # process = CrawlerProcess(settings=settings)
    failed_urls = []
    cold_run = True
    for _ in range(10):
        yield process.crawl(AmazonProductInfoSpider, cold_run=cold_run, failed_urls=failed_urls)
        cold_run = False
        if len(failed_urls) == 0:
            break
    
    failed_urls = []
    cold_run = True
    for _ in range(10):
        yield process.crawl(AmazonProductSalePriceBSRSpider, cold_run=cold_run, failed_urls=failed_urls)
        cold_run = False
        if len(failed_urls) == 0:
            break

    failed_urls = []
    cold_run = True
    for _ in range(10):
        yield process.crawl(AmazonProductCommentsSpider, cold_run=cold_run, failed_urls=failed_urls, count=50)
        cold_run = False
        if len(failed_urls) == 0:
            break

    failed_urls = []
    cold_run = True
    for _ in range(10):
        yield process.crawl(AmazonShareOfSearchSpider, cold_run=cold_run, failed_urls=failed_urls, keywords=["hairfall control shampoo", "Shampoo for smooth hair"], pages=5)
        cold_run = False
        if len(failed_urls) == 0:
            break
    # process.join()
    # print("******************************\nReturned: ",d)
    # d.addBoth(lambda _ : reactor.stop())
    # d.addCallback(print)
    # print(d)
    # print(a)
    # a.addCallback(print)
    print(failed_urls)
    # process.start()
    reactor.stop()

run()
reactor.run()
