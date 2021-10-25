import scrapy
from scrapy import settings
from amazon_product_scraping.items import AmazonSearchCount, AmazonSearchProductList
from math import ceil
from scrapy.http.response.html import HtmlResponse
from urllib.parse import quote
from webscrapingapi_scrapy_sdk import WebScrapingApiSpider, WebScrapingApiRequest
from functools import partial


class AmazonSearchListSpider(WebScrapingApiSpider):
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
    name = "AmazonSearchListSpider"
    rotate_user_agent = True
    # allowed_domains = ["amazon.in"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_product_scraping.pipelines.NewListingProductURLToMongoPipeline': 300
        }
    }

    def start_requests(self):
        """
        This class method must return an iterable with the first Requests to crawl for this spider.

        Set our proxy port http://scraperapi:API_KEY@proxy-server.scraperapi.com:8001 as the proxy in the meta parameter.
        """
        if "https://tinyurl.com/xpme2pv4" in self.urls:
            # Count link
            yield WebScrapingApiRequest(
                url="https://tinyurl.com/xpme2pv4",
                callback= partial(self.parse_count, "https://tinyurl.com/xpme2pv4")
                # meta={
                #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                # }
            )
        else:
            # ProductList links
            assert self.cold_run == False
            for url in self.urls:
                yield WebScrapingApiRequest(
                    url=url,
                    callback= partial(self.parse_product_list, url)
                    # meta={
                    #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                    # }
                )

    def __init__(self, cold_run, failed_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = failed_urls
        self.cold_run = cold_run
        # self.urls = [
        #     "http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote("https://www.amazon.in/s?k=shampoo&i=beauty&rh=n%3A1355016031%2Cp_89%3ABiotique%7CDove%7CHead+%26+Shoulders%7CL%27Oreal+Paris%7CTRESemme".encode('utf-8')))
        # ]
        self.urls = [
            "https://tinyurl.com/xpme2pv4", # https://www.amazon.in/s?k=shampoo&i=beauty&rh=n%3A1355016031%2Cp_89%3ABiotique%7CDove%7CHead+%26+Shoulders%7CL%27Oreal+Paris%7CTRESemme
        ]

    def parse_count(self, url, response):
        """
        A class method used to parse the response for each request, extract scraped data as dicts.

        Parameters
        ----------
        response : object
            represents an HTTP response

        Returns
        -------
        count
            extracted count of products appearing in search
        """

        print(response.url, response.status)
        if response.status != 200:
            if url not in self.failed_urls:
                self.failed_urls.append(url)

        item = AmazonSearchCount()
        counts = (
            response.xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()')
            .extract_first()
        )
        print(counts)
        counts = counts.split() if isinstance(counts, str) else []
        print(counts)
        try:
            count = int(counts[counts.index('of')+1].replace(',', ''))
        except:
            try:
                count = int(counts[counts.index('over')+1].replace(',', ''))
            except:
                count = 0
                print("No count of products found")
                if url not in self.failed_urls:
                    self.failed_urls.append(url)

        item["count"] = count
        print("**********\n Count:", count)
        yield item
        # TODO Remove '/5'
        for i in range(1, min(51, ceil(count/48))):
            yield WebScrapingApiRequest(
                url = url + quote("?page={}".format(i).encode('utf-8')),
                callback= partial(self.parse_product_list, url),
                # meta={
                #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                # }
            )

    def parse_product_list(self, url, response):
        """
        A class method used to parse the response for each request, extract scraped data as dicts.

        Parameters
        ----------
        response : object
            represents an HTTP response

        Returns
        -------
        dicts
            extract the scraped data as dicts
        """
        if response.status != 200:
            if url not in self.failed_urls:
                self.failed_urls.append(url)

        print(response.url, response.status)
        items = AmazonSearchProductList()
        # /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[1]
        # /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[2]
        # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]
        try:
            asins = set(response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div/@data-asin').extract())
            asins.discard('')
            products = []
            for asin in asins:
                products.append({'product_asin': asin, 'product_url': 'https://www.amazon.in/dp/{}'.format(asin)})
            
            if len(asins) == 0:
                if url not in self.failed_urls:
                    self.failed_urls.append(url)
            # if len(products) == 0 and url not in self.failed_urls:
            #     if url not in self.failed_urls:
            #         self.failed_urls.append(url)
        except:
            if url not in self.failed_urls:
                self.failed_urls.append(url)

        items['products'] = products
        # print("****\nItem:", items)
        print(len(products))
        yield items

# from requests import get