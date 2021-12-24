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
def run(bsr_100: bool = False, search_list: bool = False, price_bsr_move: bool = False, comments: bool = False, sos: bool = False):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('run_summary.log', 'a') as f:
        f.write("\n********************\n")
        f.write("Scraper started : {}\n\n".format(time))

    if bsr_100:
        # # Top 100 BSR Spider
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
            yield process.crawl(AmazonTop100BSRSpider, 
            start_urls = [
                "https://tinyurl.com/x8we47hb", # https://www.amazon.in/gp/bestsellers/beauty/1374334031/ref=zg_bs_nav_beauty_3_9851597031
                "https://tinyurl.com/hwnp6vz3", # https://www.amazon.in/gp/bestsellers/beauty/1374334031/ref=zg_bs_pg_2?ie=UTF8&pg=2
            ],
            cold_run=cold_run, failed_urls=failed_urls, success_counts=success_counts)
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
        
    if search_list:
        # # Search List Spider
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
            yield process.crawl(AmazonSearchListSpider,
            start_urls = [
                "https://tinyurl.com/xpme2pv4", # https://www.amazon.in/s?k=shampoo&i=beauty&rh=n%3A1355016031%2Cp_89%3ABiotique%7CDove%7CHead+%26+Shoulders%7CL%27Oreal+Paris%7CTRESemme
                # "https://tinyurl.com/y5ksfjaz", 
                # "https://tinyurl.com/ycku6d56",
                # "https://tinyurl.com/2p9cyy28",
                # "https://tinyurl.com/2p8bfv5z"
            ],
            cold_run=cold_run, failed_urls=failed_urls, success_counts=success_counts)
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

    if bsr_100 or search_list:
        # # Product Info Spider
        # # # process = CrawlerProcess(settings=settings)
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
    
    if price_bsr_move:
        # # Product Sale Price BSR Spider
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
    
    if comments:
        # # Product Comments Spider
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
    
    if sos:
        # # Share of Search Spider
        failed_urls = []
        cold_run = True
        total_success_counts = {
            'added': 0
        }
        for i in range(10):
            success_counts = {
                'added': 0
            }
            yield process.crawl(AmazonShareOfSearchSpider, time=time, cold_run=cold_run, failed_urls=failed_urls, keywords=[
                "Anti dandruff shampoo",
                # "Dandruff Shampoo",
                # "Himalaya Anti Dandruff Shampoo",
                # "Dove Anti Dandruff Shampoo",
                # "Meera Anti Dandruff Shampoo",
                # "Head & Shoulders Anti Dandruff Shampoo",
                # "Clear Anti Dandruff Shampoo",
                # "Anti Dandruff Shampoo for men",
                # "Anti Dandruff Shampoo for women"
                # "shampoo for dry and frizzy hair", "shampoo and conditioner combo", "shampoo and conditioner", "shampoo 1 litre", "dandruff shampoo", "hair fall control shampoo", "shampoo for oily scalp", "shampoo for dry hair", "shampoo for coloured hair", "shampoo for thin hair", "shampoo for men", "shampoo for women"
                ], pages=1, success_counts=success_counts)
            cold_run = False
            total_success_counts['added'] += success_counts['added']
            print(failed_urls)
            with open('run_summary.log', 'a') as f:
                f.write("Run {}:\nFound and Added rank of {} products in AmazonShareOfSearchSpider\n\t- {} URLs failed\n\n".format(i+1, success_counts['added'], len(failed_urls)))
            if len(failed_urls) == 0:
                break

        with open('run_summary.log', 'a') as f:
            f.write("AmazonShareOfSearchSpider Summary:\nFound and Added rank of {} products in AmazonShareOfSearchSpider\n".format(total_success_counts['added']))
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

# run(bsr_100=True, search_list=True, price_bsr_move=True, comments=True, sos=True)
# reactor.run()
