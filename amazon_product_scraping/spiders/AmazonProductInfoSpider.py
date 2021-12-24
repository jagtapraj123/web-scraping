from amazon_product_scraping.items import AmazonProductInfoItem
from amazon_product_scraping.utils.AmazonScrapingHelper import AmazonScrapingHelper
import logging
from scrapy import signals
from webscrapingapi_scrapy_sdk import WebScrapingApiSpider, WebScrapingApiRequest
from functools import partial

logger = logging.getLogger("scraper")
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


class AmazonProductInfoSpider(WebScrapingApiSpider):
    """
    A class for scrapy spider.

    Attributes
    ----------
    handle_httpstatus_all : Boolean
        True
    name : str
        spider name which identify the spider
    rotate_user_agent : Boolean
        True
    allowed_domains : list
        contains base-URLs for the allowed domains for the spider to crawl
    start_urls : list
        a list of URLs for the spider to start crawling from
    """

    debug = False
    handle_httpstatus_all = True
    name = "AmazonProductInfoSpider"
    rotate_user_agent = True

    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_product_scraping.pipelines.AmazonProductInfoToMongoPipeline': 300
        }
    }

    def start_requests(self):
        """
        This class method must return an iterable with the first Requests to crawl for this spider.

        Set our proxy port http://scraperapi:API_KEY@proxy-server.scraperapi.com:8001 as the proxy in the meta parameter.
        """

        if self.cold_run:
            for url in self.urls:
                self.add_to_failed('info', {'url': url})
                yield WebScrapingApiRequest(
                    url=url,
                    callback=partial(self.parse_info, {'url': url})
                )
        else:
            for func, params in self.failed_urls:
                if func == 'info':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        callback=partial(self.parse_info, params)
                    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = kwargs['failed_urls']
        self.cold_run = kwargs['cold_run']
        self.success_counts = kwargs['success_counts']
        self.urls = []
        self.mongo_db = kwargs['mongo_db']

    def add_to_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        if wrapper not in self.failed_urls:
            self.failed_urls.append(wrapper)

    def remove_from_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        if wrapper in self.failed_urls:
            self.failed_urls.remove(wrapper)

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

        spider = super(AmazonProductInfoSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.handle_spider_closed, signals.spider_closed)
        return spider

    def parse_info(self, params, response):
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

        print(response.url, response.status)
        print(params)

        failed = False
        if response.status != 200:
            failed = True

        helper = AmazonScrapingHelper()
        item = AmazonProductInfoItem()

        try:
            title = helper.get_title(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            title = "NA"
            failed = True

        try:
            brand = helper.get_brand(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            brand = "NA"
            failed = True

        # try:
        #     sale_price = helper.get_sale_price(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     sale_price = "NA"
        #     failed = True

        try:
            offers = helper.get_offers(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            offers = "NA"
            failed = True

        try:
            original_price = helper.get_original_price(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            original_price = "NA"
            failed = True

        # try:
        #     fullfilled = helper.get_fullfilled(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     fullfilled = "NA"
        #     failed = True

        # try:
        #     rating = helper.get_rating(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     rating = "NA"
        #     failed = True

        # try:
        #     total_reviews = helper.get_total_reviews(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     total_reviews = "NA"
        #     failed = True

        # try:
        #     availability = helper.get_availability(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     availability = "NA"
        #     failed = True

        try:
            category = helper.get_category(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            category = "NA"
            failed = True

        try:
            icons = helper.get_icons(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            icons = "NA"
            failed = True

        # try:
        #     best_seller_rank = helper.get_best_seller_rank_1(response)
        #     if best_seller_rank[0]["value"] == "NA":
        #         best_seller_rank = helper.get_best_seller_rank_2(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     best_seller_rank = "NA"
        #     failed = True

        try:
            product_details = helper.get_product_details_1(response)
            if product_details == {}:
                product_details = helper.get_product_details_2(response)
            if product_details == {} and self.cold_run:
                failed = True
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            product_details = "NA"
            failed = True
        
        # print(product_details)
        try:
            # asin = helper.get_asin(response)
            asin = params['url'].split('/dp/')[1]
            if asin == "NA":
                failed = True
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            asin = "NA"
            failed = True

        try:
            important_information = helper.get_important_information(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            important_information = "NA"
            failed = True

        try:
            product_description = helper.get_product_description(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            product_description = "NA"
            failed = True

        try:
            bought_together = helper.get_bought_together(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            bought_together = "NA"
            failed = True

        # try:
        #     subscription_discount = helper.get_subscription_discount(response)
        # except Exception:
        #     logging.error("Exception occurred", exc_info=True)
        #     subscription_discount = "NA"
        #     failed = True

        try:
            variations = helper.get_variations(response)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            variations = "NA"
            failed = True

        item["product_name"] = title
        item["product_brand"] = brand
        # item["product_sale_price"] = sale_price
        item["product_offers"] = offers
        item["product_original_price"] = original_price
        # item["product_fullfilled"] = fullfilled
        # item["product_rating"] = rating
        # item["product_total_reviews"] = total_reviews
        # item["product_availability"] = availability
        item["product_category"] = category
        item["product_icons"] = icons
        # item["product_best_seller_rank"] = best_seller_rank
        item["product_details"] = product_details
        item["product_asin"] = asin
        item["product_important_information"] = important_information
        item["product_description"] = product_description
        item["product_bought_together"] = bought_together
        # item["product_subscription_discount"] = subscription_discount
        item["product_variations"] = variations

        if failed:
            if self.debug:
                print("**DEBUG:**/n {}".format(item))
                with open('fails/{}.html'.format(asin), 'w', encoding='utf-8') as f:
                    f.write(response.text)
            yield None
        else:
            self.remove_from_failed('info', params)
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
