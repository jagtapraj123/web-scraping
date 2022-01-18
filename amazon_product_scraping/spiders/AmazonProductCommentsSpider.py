from amazon_product_scraping.items import AmazonProductCommentsItem
from amazon_product_scraping.utils.AmazonScrapingHelper import AmazonCommentsScrapingHelper
import logging
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
    rotate_user_agent : Boolean
        True
    allowed_domains : list
        contains base-URLs for the allowed domains for the spider to crawl
    start_urls : list
        a list of URLs for the spider to start crawling from
    """

    debug = False
    handle_httpstatus_all = True
    name = "AmazonProductCommentsSpider"
    rotate_user_agent = True
    
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

        if self.cold_run:
            for url in self.urls:
                self.add_to_failed('comms', {'url': url})
                yield WebScrapingApiRequest(
                    url=url,
                    callback=partial(self.parse_comms, {'url': url})
                )
        else:
            for func, params in self.failed_urls:
                if func == 'comms':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        callback = partial(self.parse_comms, params)
                    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = kwargs['failed_urls']
        self.cold_run = kwargs['cold_run']
        self.count = kwargs['count']
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

        spider = super(AmazonProductCommentsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.handle_spider_closed, signals.spider_closed)
        return spider

    def parse_comms(self, params, response):
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

        print(response.url, response.status)
        print(params)

        failed = False
        if response.status != 200:
            failed = True

        asin = params['url'].split("/product-reviews/")[1].split("/")[0]
        helper = AmazonCommentsScrapingHelper()
        item = AmazonProductCommentsItem()

        try:
            comments = helper.get_comments(response)
            # if len(comments) == 0 and self.cold_run:
            #     failed = True
        except:
            logging.error("Exception occured", exc_info=True)
            comments = []
            failed = True

        item["product_asin"] = asin
        item["product_comments"] = []
        for comm in comments:
            if self.count > 0 or (self.count < 0 and (datetime.datetime.now() - comm['date']).days <= -self.count):
                item["product_comments"].append(comm)
        
        if failed:
            if self.debug:
                print("**DEBUG:**/n {}".format(item))
                with open('fails/Comments_{}.html'.format(asin), 'w', encoding='utf-8') as f:
                    f.write(response.text)
            yield None
        else:
            self.remove_from_failed('comms', params)

            if self.count < 0 and len(comments) > 0:
                if (datetime.datetime.now() - comments[-1]['date']).days <= -self.count:
                    # next_page_url = "{}&pageNumber={}".format(url.split("&pageNumber=")[0], 1+int(url.split("&pageNumber=")[1]))
                    # curr_url = unquote(url.split("&url=")[1])
                    # next_page_url = "{}&url={}".format(url.split("&url=")[0], quote("{}&pageNumber={}".format(curr_url.split("&pageNumber=")[0], 1+int(curr_url.split("&pageNumber=")[1])).encode('utf-8')))
                    next_page_url = "{}&pageNumber={}".format(params['url'].split("&pageNumber=")[0], 1+int(params['url'].split("&pageNumber=")[1]))
                    self.add_to_failed('comms', {'url': next_page_url})
                    yield WebScrapingApiRequest(
                        url=next_page_url,
                        callback=partial(self.parse_comms, {'url': next_page_url})
                        # meta={
                        #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                        # },
                    )
            elif self.count > 0 and len(comments) > 0:
                if int(params['url'].split("&pageNumber=")[1]) < self.count/10:
                    next_page_url = "{}&pageNumber={}".format(params['url'].split("&pageNumber=")[0], 1+int(params['url'].split("&pageNumber=")[1]))
                    self.add_to_failed('comms', {'url': next_page_url})
                    yield WebScrapingApiRequest(
                        url=next_page_url,
                        callback=partial(self.parse_comms, {'url': next_page_url})
                        # meta={
                        #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                        # },
                    )
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
