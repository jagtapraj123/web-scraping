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


class AmazonProductSpider(scrapy.Spider):
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
    name = "AmazonProductSpider"
    rotate_user_agent = True
    allowed_domains = ["amazon.in"]
    with open("amazon_product_scraping/configuration_file/config.json") as file:
        input_data = json.load(file)
    start_urls = FileHelper.get_urls(input_data["product_data"]["old_data_file_path"])
    # start_urls = ["http://amazon.in/dp/B08K3HQ4M4"]
    # start_urls = ["http://amazon.in/dp/B0031TSC34", "http://amazon.in/dp/B08HJC7GXS", "http://amazon.in/dp/B08HH3YLGZ", "http://amazon.in/dp/B01N1KE7D5", "http://amazon.in/dp/B01HBA74PU", "http://amazon.in/dp/B01IOPY3G4", "http://amazon.in/dp/B00AREI5KG", "http://amazon.in/dp/B01H7BOYNS", "http://amazon.in/dp/B01HBA4VMY", "http://amazon.in/dp/B077SSHGPM", "http://amazon.in/dp/B08BXLVDF1", "http://amazon.in/dp/B081BG8LDS", "http://amazon.in/dp/B08BXJ3WD9", "http://amazon.in/dp/B01BK7FF24", "http://amazon.in/dp/B07FJ7NDGK", "http://amazon.in/dp/B07MQWT396", "http://amazon.in/dp/B07M857C6Z", "http://amazon.in/dp/B07FJ7W7PH", "http://amazon.in/dp/B07F7LB4T9", "http://amazon.in/dp/B089H69JCW", "http://amazon.in/dp/B07HLZDR9S", "http://amazon.in/dp/B07HMCC4RF", "http://amazon.in/dp/B07HMCZJ2P", "http://amazon.in/dp/B07HLZDKNN", "http://amazon.in/dp/B01CGETA9Y", "http://amazon.in/dp/B082Y7WWH1", "http://amazon.in/dp/B07TWQF5GH", "http://amazon.in/dp/B07QF8FLYN", "http://amazon.in/dp/B082Y8VVKG", "http://amazon.in/dp/B088HP22TP", "http://amazon.in/dp/B07J314NP8", "http://amazon.in/dp/B071P13PSJ", "http://amazon.in/dp/B01M9EB7ZK", "http://amazon.in/dp/B093SXXN5V", "http://amazon.in/dp/B08HP7LJ7K", "http://amazon.in/dp/B093SWNYYS"]

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

        spider = super(AmazonProductSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        print(response)
        helper = AmazonScrapingHelper()
        items = AmazonProductScrapingItem()

        try:
            title = helper.get_title(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            title = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            brand = helper.get_brand(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            brand = "NA"
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
            offers = helper.get_offers(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            offers = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            original_price = helper.get_original_price(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            original_price = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            fullfilled = helper.get_fullfilled(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            fullfilled = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            rating = helper.get_rating(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            rating = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            total_reviews = helper.get_total_reviews(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            total_reviews = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            availability = helper.get_availability(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            availability = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            category = helper.get_category(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            category = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            icons = helper.get_icons(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            icons = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            best_seller_rank = helper.get_best_seller_rank_1(response)
            if best_seller_rank[0]["value"] == "NA":
                best_seller_rank = helper.get_best_seller_rank_2(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            best_seller_rank = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            product_details = helper.get_product_details_1(response)
            if product_details == {}:
                product_details = helper.get_product_details_2(response)
            if product_details == {} and response.url not in self.failed_urls:
                self.failed_urls.append(response.url)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            product_details = "NA"
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
            important_information = helper.get_important_information(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            important_information = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            product_description = helper.get_product_description(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            product_description = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            bought_together = helper.get_bought_together(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            bought_together = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            subscription_discount = helper.get_subscription_discount(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            subscription_discount = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        try:
            variations = helper.get_variations(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            variations = "NA"
            if response.url not in self.failed_urls:
                self.failed_urls.append(response.url)

        dict = {"URL": self.failed_urls}
        df = pd.DataFrame(dict)
        df.to_csv(
            "amazon_product_scraping/data/InputData/amazon_product_data_failed_urls.csv",
            index=False,
        )

        items["product_name"] = title
        items["product_brand"] = brand
        items["product_sale_price"] = sale_price
        items["product_offers"] = offers
        items["product_original_price"] = original_price
        items["product_fullfilled"] = fullfilled
        items["product_rating"] = rating
        items["product_total_reviews"] = total_reviews
        items["product_availability"] = availability
        items["product_category"] = category
        items["product_icons"] = icons
        items["product_best_seller_rank"] = best_seller_rank
        items["product_details"] = product_details
        items["product_asin"] = asin
        items["product_important_information"] = important_information
        items["product_description"] = product_description
        items["product_bought_together"] = bought_together
        items["product_subscription_discount"] = subscription_discount
        items["product_variations"] = variations
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
