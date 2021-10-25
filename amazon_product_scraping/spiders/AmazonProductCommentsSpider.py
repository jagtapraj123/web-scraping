from time import strptime
from urllib.parse import quote, unquote
import scrapy
import json
from amazon_product_scraping.items import AmazonProductCommentsItem
from amazon_product_scraping.utils.AmazonScrapingHelper import (
    AmazonCommentsScrapingHelper,
)

from amazon_product_scraping.utils.FileHelper import FileHelper
import logging
import pandas as pd
from scrapy import signals
from functools import partial
import datetime
from webscrapingapi_scrapy_sdk import WebScrapingApiSpider, WebScrapingApiRequest

logger = logging.getLogger("scraper")
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


class AmazonProductCommentsSpider(WebScrapingApiSpider):
    """
    A class for scrapy spider.

    Attributes
    ----------
    handle_httpstatus_all : Boolean
        True
    name : str
        spider name which identify the spider
    rotate_user_agent : Bollean
        True
    allowed_domains : list
        contains base-URLs for the allowed domains for the spider to crawl
    start_urls : list
        a list of URLs for the spider to start crawling from
    """

    handle_httpstatus_all = True
    name = "AmazonProductCommentsSpider"
    rotate_user_agent = True
    # allowed_domains = ["amazon.in"]
    # with open("amazon_product_scraping/configuration_file/config.json") as file:
    #     input_data = json.load(file)
    # # start_urls = FileHelper.get_urls(input_data["product_data"]["old_data_file_path"])
    # start_urls = ["http://amazon.in/dp/B006G84U56"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_product_scraping.pipelines.CommentsToMongoPipeline': 400
        }
    }

    def start_requests(self):
        """
        This class method must return an iterable with the first Requests to crawl for this spider.

        Set our proxy port http://scraperapi:API_KEY@proxy-server.scraperapi.com:8001 as the proxy in the meta parameter.
        """

        for url in self.urls:
            # asin = url.split("/dp/")[1].split("/")[0]
            # for i in range(1, 6):
            yield WebScrapingApiRequest(
                url=url,
                callback=partial(self.parse, url)
                # meta={
                #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                # },
            )

    def __init__(self, cold_run, failed_urls, count=-1,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = failed_urls
        self.count = count
        self.cold_run = cold_run
        self.urls = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        A class method used by Scrapy to create a spider.

        Parameters
        ----------
        crawler : object
            crawler to which the spider will be bound
        args : list
            arguments passed to the __init__() method
        kwargs : dict
            keyword arguments passed to the __init__() method

        Returns
        -------
        str
            spider
        """

        spider = super(AmazonProductCommentsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.handle_spider_closed, signals.spider_closed)
        return spider

    def parse(self, url, response):
        """
        A class method used to parse the response for each request, extract scraped data as dicts and save failed urls in a csv file.

        Parameters
        ----------
        asin : str
            Asin of the product for which comments are being scraped

        response : object
            represents an HTTP response

        Raise
        -----
        Exception
            If not exist xpath of attributes of each request

        Returns
        -------
        list of dicts
            extract the scraped comments as a list of dicts
        """
        # print("****\nParsing\n******")
        print(response.url, response.status)
        if response.status != 200:
            if url not in self.failed_urls:
                self.failed_urls.append(url)
        # print(url)
        asin = url.split("/product-reviews/")[1].split("/")[0]
        helper = AmazonCommentsScrapingHelper()
        item = AmazonProductCommentsItem()

        try:
            comments = helper.get_comments(response)
        except:
            logging.error("Exception occured", exc_info=True)
            comments = []
            if url not in self.failed_urls:
                self.failed_urls.append(url)

        # dict = {"URL": self.failed_urls}
        # df = pd.DataFrame(dict)
        # df.to_csv(
        #     "amazon_product_scraping/data/InputData/amazon_product_comments_failed_urls.csv",
        #     index=False,
        # )

        item["product_asin"] = asin
        item["product_comments"] = []
        for comm in comments:
            if self.count > 0 or (self.count < 0 and (datetime.datetime.now() - comm['date']).days <= -self.count):
                item["product_comments"].append(comm)
        yield item

        if self.cold_run:
            if self.count < 0 and len(comments) > 0:
                if (datetime.datetime.now() - comments[-1]['date']).days <= -self.count:
                    # next_page_url = "{}&pageNumber={}".format(url.split("&pageNumber=")[0], 1+int(url.split("&pageNumber=")[1]))
                    # curr_url = unquote(url.split("&url=")[1])
                    # next_page_url = "{}&url={}".format(url.split("&url=")[0], quote("{}&pageNumber={}".format(curr_url.split("&pageNumber=")[0], 1+int(curr_url.split("&pageNumber=")[1])).encode('utf-8')))
                    next_page_url = "{}&pageNumber={}".format(url.split("&pageNumber=")[0], 1+int(url.split("&pageNumber=")[1]))
                    yield WebScrapingApiRequest(
                        url=next_page_url,
                        callback=partial(self.parse, url)
                        # meta={
                        #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                        # },
                    )
            elif self.count > 0 and len(comments) > 0:
                if int(url.split("&pageNumber=")[1]) < self.count/10:
                    next_page_url = "{}&pageNumber={}".format(url.split("&pageNumber=")[0], 1+int(url.split("&pageNumber=")[1]))
                    yield WebScrapingApiRequest(
                        url=next_page_url,
                        callback=partial(self.parse, url)
                        # meta={
                        #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                        # },
                    )

        

    def handle_spider_closed(self, reason):

        """
        A class method used to provide a shortcut to signals.connect() for the spider_closed signal.

        Parameters
        ----------
        reason : str
            a string which describes the reason why the spider was closed
        """

        self.crawler.stats.set_value("failed_urls", self.failed_urls)
