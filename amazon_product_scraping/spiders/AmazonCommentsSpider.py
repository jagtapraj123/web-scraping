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

logger = logging.getLogger("scraper")
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


class AmazonCommentsSpider(scrapy.Spider):
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
    name = "AmazonCommentsSpider"
    rotate_user_agent = True
    allowed_domains = ["amazon.in"]
    with open("amazon_product_scraping/configuration_file/config.json") as file:
        input_data = json.load(file)
    start_urls = FileHelper.get_urls(input_data["product_data"]["old_data_file_path"])
    # start_urls = ["http://amazon.in/dp/B006G84U56"]

    def start_requests(self):
        """
        This class method must return an iterable with the first Requests to crawl for this spider.

        Set our proxy port http://scraperapi:API_KEY@proxy-server.scraperapi.com:8001 as the proxy in the meta parameter.
        """

        urls = self.start_urls

        for url in urls:
            asin = url.split("/dp/")[1].split("/")[0]
            for i in range(1, 6):
                yield scrapy.Request(
                    url="https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={}".format(
                        asin, i
                    ),
                    callback=partial(self.parse, asin),
                    meta={
                        "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                    },
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = []

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

        spider = super(AmazonCommentsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.handle_spider_closed, signals.spider_closed)
        return spider

    def parse(self, asin, response):
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

        helper = AmazonCommentsScrapingHelper()
        item = AmazonProductCommentsItem()

        try:
            comments = helper.get_comments(response)
        except:
            logging.error("Exception occured", exc_info=True)
            comments = []
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        dict = {"URL": self.failed_urls}
        df = pd.DataFrame(dict)
        df.to_csv(
            "amazon_product_scraping/data/InputData/amazon_product_comments_failed_urls.csv",
            index=False,
        )

        item["product_asin"] = asin
        item["product_comments"] = comments
        yield item

    def handle_spider_closed(self, reason):

        """
        A class method used to provide a shortcut to signals.connect() for the spider_closed signal.

        Parameters
        ----------
        reason : str
            a string which describes the reason why the spider was closed
        """

        self.crawler.stats.set_value("failed_urls", self.failed_urls)
