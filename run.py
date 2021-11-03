from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from amazon_product_scraping.spiders.AmazonTop100BSRSpider import AmazonTop100BSRSpider
from amazon_product_scraping.spiders.AmazonSearchListSpider import AmazonSearchListSpider
from amazon_product_scraping.spiders.AmazonProductInfoSpider import AmazonProductInfoSpider
from amazon_product_scraping.spiders.AmazonProductSalePriceBSRSpider import AmazonProductSalePriceBSRSpider
from amazon_product_scraping.spiders.AmazonProductCommentsSpider import AmazonProductCommentsSpider
from amazon_product_scraping.spiders.AmazonShareOfSearchSpider import AmazonShareOfSearchSpider
from scrapy.utils.project import get_project_settings
import datetime


settings = get_project_settings()
process = CrawlerRunner(settings=settings)

@defer.inlineCallbacks
def run():
    with open('run_summary.log', 'a') as f:
        f.write("\n********************\n")
        f.write("Scraper started : {}\n\n".format(datetime.datetime.now()))

    failed_urls = []
    cold_run = True
    total_success_counts = {
        'new': 0,
        'existing': 0
    }
    for i in range(10):
        success_counts = {
            'new': 0,
            'existing': 0
        }
        yield process.crawl(AmazonTop100BSRSpider, cold_run=cold_run, failed_urls=failed_urls, success_counts=success_counts)
        cold_run = False
        total_success_counts['new'] += success_counts['new']
        total_success_counts['existing'] += success_counts['existing']
        with open('run_summary.log', 'a') as f:
            f.write("Run {}:\nFound {} products in AmazonTop100BSRSpider\n\t- {} new products were added to DB\n\t- {} products were already in DB\n\n".format(i+1, success_counts['new']+success_counts['existing'], success_counts['new'], success_counts['existing']))
        if len(failed_urls) == 0:
            break
    
    with open('run_summary.log', 'a') as f:
        f.write("AmazonTop100BSRSpider Summary:\nFound {} products in AmazonTop100BSRSpider\n\t- {} new products were added to DB\n\t- {} products were already in DB\n".format(total_success_counts['new']+total_success_counts['existing'], total_success_counts['new'], total_success_counts['existing']))
        f.write("\tFailed URLs: {}\n".format(len(failed_urls)))
        for j in range(len(failed_urls)):
            f.write("\t\t{}. {}\n".format(j+1, failed_urls[j]))
        f.write("\n")

    failed_urls = []
    cold_run = True
    total_success_counts = {
        'new': 0,
        'existing': 0
    }
    for i in range(10):
        success_counts = {
            'new': 0,
            'existing': 0
        }
        yield process.crawl(AmazonSearchListSpider, cold_run=cold_run, failed_urls=failed_urls, success_counts=success_counts)
        cold_run = False
        total_success_counts['new'] += success_counts['new']
        total_success_counts['existing'] += success_counts['existing']
        with open('run_summary.log', 'a') as f:
            f.write("Run {}:\nFound {} products in AmazonSearchListSpider\n\t- {} new products were added to DB\n\t- {} products were already in DB\n\n".format(i+1, success_counts['new']+success_counts['existing'], success_counts['new'], success_counts['existing']))
        if len(failed_urls) == 0:
            break
    
    with open('run_summary.log', 'a') as f:
        f.write("AmazonSearchListSpider Summary:\nFound {} products in AmazonSearchListSpider\n\t- {} new products were added to DB\n\t- {} products were already in DB\n".format(total_success_counts['new']+total_success_counts['existing'], total_success_counts['new'], total_success_counts['existing']))
        f.write("\tFailed URLs: {}\n".format(len(failed_urls)))
        for j in range(len(failed_urls)):
            f.write("\t\t{}. {}\n".format(j+1, failed_urls[j]))
        f.write("\n")

    # # process = CrawlerProcess(settings=settings)
    failed_urls = []
    cold_run = True
    total_success_counts = {
        'new': 0,
        'added': 0
    }
    for i in range(10):
        success_counts = {
            'new': 0,
            'added': 0
        }
        yield process.crawl(AmazonProductInfoSpider, cold_run=cold_run, failed_urls=failed_urls, success_counts=success_counts)
        cold_run = False
        total_success_counts['new'] += success_counts['new']
        total_success_counts['added'] += success_counts['added']
        with open('run_summary.log', 'a') as f:
            f.write("Run {}:\nFound {} products in AmazonProductInfoSpider\n\t- {} successfully added to DB\n\n".format(i+1, success_counts['new'], success_counts['added']))
        if len(failed_urls) == 0:
            break

    with open('run_summary.log', 'a') as f:
        f.write("AmazonProductInfoSpider Summary:\nFound {} products in AmazonProductInfoSpider\n\t- {} successfully added to DB\n".format(total_success_counts['new'], total_success_counts['added']))
        f.write("\tFailed URLs: {}\n".format(len(failed_urls)))
        for j in range(len(failed_urls)):
            f.write("\t\t{}. {}\n".format(j+1, failed_urls[j]))
        f.write("\n")
    
    failed_urls = []
    cold_run = True
    total_success_counts = {
        'new': 0,
        'added': 0
    }
    for i in range(10):
        success_counts = {
            'new': 0,
            'added': 0
        }
        yield process.crawl(AmazonProductSalePriceBSRSpider, cold_run=cold_run, failed_urls=failed_urls, success_counts=success_counts)
        cold_run = False
        total_success_counts['new'] += success_counts['new']
        total_success_counts['added'] += success_counts['added']
        with open('run_summary.log', 'a') as f:
            f.write("Run {}:\nFound {} products in AmazonProductSalePriceBSRSpider\n\t- {} successfully added to DB\n\n".format(i+1, success_counts['new'], success_counts['added']))
        if len(failed_urls) == 0:
            break

    with open('run_summary.log', 'a') as f:
        f.write("AmazonProductSalePriceBSRSpider Summary:\nFound {} products in AmazonProductSalePriceBSRSpider\n\t- {} successfully added to DB\n".format(total_success_counts['new'], total_success_counts['added']))
        f.write("\tFailed URLs: {}\n".format(len(failed_urls)))
        for j in range(len(failed_urls)):
            f.write("\t\t{}. {}\n".format(j+1, failed_urls[j]))
        f.write("\n")

    failed_urls = []
    cold_run = True
    total_success_counts = {
        'prods_checked': 0,
        'prods_with_new_comms': 0,
        'new_comments': 0
    }
    for i in range(10):
        success_counts = {
            'prods_checked': 0,
            'prods_with_new_comms': 0,
            'new_comments': 0
        }
        yield process.crawl(AmazonProductCommentsSpider, cold_run=cold_run, failed_urls=failed_urls, count=-1, success_counts=success_counts)
        cold_run = False
        total_success_counts['prods_checked'] += success_counts['prods_checked']
        total_success_counts['prods_with_new_comms'] += success_counts['prods_with_new_comms']
        total_success_counts['new_comments'] += success_counts['new_comments']
        with open('run_summary.log', 'a') as f:
            f.write("Run {}:\nChecked {} products in AmazonProductCommentsSpider\n\t- {} products had new comments\n\t- {} comments successfully added to DB\n\n".format(i+1, success_counts['prods_checked'], success_counts['prods_with_new_comms'], success_counts['new_comments']))
        if len(failed_urls) == 0:
            break

    with open('run_summary.log', 'a') as f:
        f.write("AmazonProductCommentsSpider Summary:\nChecked {} products in AmazonProductCommentsSpider\n\t- {} products had new comments\n\t- {} comments successfully added to DB\n\n".format(total_success_counts['prods_checked'], total_success_counts['prods_with_new_comms'], total_success_counts['new_comments']))
        f.write("\tFailed URLs: {}\n".format(len(failed_urls)))
        for j in range(len(failed_urls)):
            f.write("\t\t{}. {}\n".format(j+1, failed_urls[j]))
        f.write("\n")

    failed_urls = []
    cold_run = True
    total_success_counts = {
        'added': 0
    }
    for i in range(10):
        success_counts = {
            'added': 0
        }
        yield process.crawl(AmazonShareOfSearchSpider, cold_run=cold_run, failed_urls=failed_urls, keywords=["hairfall control shampoo", "Shampoo for smooth hair"], pages=5, success_counts=success_counts)
        cold_run = False
        total_success_counts['added'] += success_counts['added']
        with open('run_summary.log', 'a') as f:
            f.write("Run {}:\nFound and Added rank of {} products in AmazonShareOfSearchSpider".format(i+1, success_counts['added']))
        if len(failed_urls) == 0:
            break

    with open('run_summary.log', 'a') as f:
        f.write("AmazonShareOfSearchSpider Summary:\nFound and Added rank of {} products in AmazonShareOfSearchSpider".format(total_success_counts['added']))
        f.write("\tFailed URLs: {}\n".format(len(failed_urls)))
        for j in range(len(failed_urls)):
            f.write("\t\t{}. {}\n".format(j+1, failed_urls[j]))
        f.write("\n")
    # process.join()
    # print("******************************\nReturned: ",d)
    # d.addBoth(lambda _ : reactor.stop())
    # d.addCallback(print)
    # print(d)
    # print(a)
    # a.addCallback(print)
    # print(failed_urls)
    # process.start()
    reactor.stop()

run()
reactor.run()
