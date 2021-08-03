import scrapy
import json
from amazon_product_scraping.items import AmazonProductScrapingItem
from amazon_product_scraping.utils.AmazonScrapingHelper import AmazonScrapingHelper
from amazon_product_scraping.utils.FileHelper import FileHelper
import logging
import pandas as pd
from scrapy import signals

logger = logging.getLogger("scraper")
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


class AmazonProductSalePriceBSRSpider(scrapy.Spider):
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
        a list of URLs for the spider to start crawling from"""

    handle_httpstatus_all = True
    name = "AmazonProductSalePriceBSRSpider"
    rotate_user_agent = True
    allowed_domains = ["amazon.in"]
    with open("amazon_product_scraping/configuration_file/config.json") as file:
        input_data = json.load(file)
    # start_urls = FileHelper.get_urls(input_data["product_data"]["all_urls_path"])
    start_urls = ["http://amazon.in/dp/B08T3325CD"]

    def start_requests(self):
        """
        This class method must return an iterable with the first Requests to crawl for this spider.

        Set our proxy port http://scraperapi:API_KEY@proxy-server.scraperapi.com:8001 as the proxy in the meta parameter.
        """

        urls = self.start_urls

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
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

        spider = super(AmazonProductSalePriceBSRSpider, cls).from_crawler(
            crawler, *args, **kwargs
        )
        crawler.signals.connect(spider.handle_spider_closed, signals.spider_closed)
        return spider

    def parse(self, response):
        """
        A class method used to parse the response for each request, extract scraped data as dicts and save failed urls in a csv file.

        Parameters
        ----------
        response : object
            represents an HTTP response

        Raise
        -----
        Exception
            If not exist xpath of attributes of each request

        Returns
        -------
        dicts
            extract the scraped data as dicts
        """

        # filename = response.url.split("/")[-1] + ".html"
        # with open(filename, "wb") as f:
        #     f.write(response.body)

        items = AmazonProductScrapingItem()
        helper = AmazonScrapingHelper()

        try:
            title = helper.get_title(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            title = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            sale_price = helper.get_sale_price(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            sale_price = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            best_seller_rank = helper.get_best_seller_rank(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            best_seller_rank = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            asin = helper.get_asin(response)
            if asin == "NA" and response.url not in self.failed_urls:
                self.failed_urls.append(response.url)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            asin = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            product_details = helper.get_product_details(response)
            if product_details == {} and response.url not in self.failed_urls:
                self.failed_urls.append(response.url)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            product_details = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        dict = {"URL": self.failed_urls}
        df = pd.DataFrame(dict)
        df.to_csv(
            "amazon_product_scraping/data/InputData/recurrent_saleprice_bsr_failed_urls.csv",
            index=False,
        )

        items["product_name"] = title
        items["product_sale_price"] = sale_price
        items["product_best_seller_rank"] = best_seller_rank
        items["product_asin"] = asin
        items["product_details"] = product_details
        yield items

    def handle_spider_closed(self, reason):
        """
        A class method used to provide a shortcut to signals.connect() for the spider_closed signal.

        Parameters
        ----------
        reason : str
            a string which describes the reason why the spider was closed
        """

        self.crawler.stats.set_value("failed_urls", self.failed_urls)
