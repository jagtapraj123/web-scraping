from urllib.parse import quote
import scrapy
from amazon_product_scraping.items import AmazonSearchProductList
from webscrapingapi_scrapy_sdk import WebScrapingApiSpider, WebScrapingApiRequest
from functools import partial


class AmazonTop100BSRSpider(WebScrapingApiSpider):
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
    name = "AmazonTop100BSRSpider"
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
        # print(self.failed_urls)
        # if len(self.failed_urls) != 0:
        #     urls = self.failed_urls
        # else:
        #     urls = self.start_urls

        for url in self.urls:
            yield WebScrapingApiRequest(
                url=url,
                callback=partial(self.parse, url)
                # meta={
                #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                # },
            )

    def __init__(self, cold_run, failed_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = failed_urls
        self.cold_run = cold_run
        # self.urls = [
        #     "http://api.scrapeup.com/?api_key={}&url={}".format("0b0df76f8a0571637677d78f121444ed", quote("https://www.amazon.in/gp/bestsellers/beauty/1374334031/ref=zg_bs_nav_beauty_3_9851597031".encode('utf-8'))),
        #     "http://api.scrapeup.com/?api_key={}&url={}".format("0b0df76f8a0571637677d78f121444ed", quote("https://www.amazon.in/gp/bestsellers/beauty/1374334031/ref=zg_bs_pg_2?ie=UTF8&pg=2".encode('utf-8'))),
        # ]
        self.urls = [
            "https://tinyurl.com/x8we47hb", # https://www.amazon.in/gp/bestsellers/beauty/1374334031/ref=zg_bs_nav_beauty_3_9851597031
            "https://tinyurl.com/hwnp6vz3", # https://www.amazon.in/gp/bestsellers/beauty/1374334031/ref=zg_bs_pg_2?ie=UTF8&pg=2
        ]

    def parse(self, url, response):
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
        print(type(response))
        print(response.url, response.status)
        if response.status != 200:
            if url not in self.failed_urls:
                self.failed_urls.append(url)

        items = AmazonSearchProductList()
        links_xpath = (
            response.xpath('//div[@id="zg-center-div"]')
            .xpath('//a[@class="a-link-normal"]/@href')
            .extract()
        )
        if len(links_xpath) == 0:
            if url not in self.failed_urls:
                self.failed_urls.append(url)
        try:
            links = [i for i in links_xpath if "/dp/" in i]
            asins = [(i.split("/dp/")[1]).split("/")[0] for i in links]
        except:
            if url not in self.failed_urls:
                self.failed_urls.append(url)
        # bsr_xpath = response.xpath(
        #     '//div[@id="zg-center-div"]//span//span//text()'
        # ).extract()
        # bsr = [i + " in Shampoos (Beauty)" for i in bsr_xpath if "#" in i]

        # items["links"] = links
        # items["asin"] = asin
        # items["bsr"] = bsr

        products = []
        for asin in asins:
            products.append({'product_asin': asin, 'product_url': 'https://www.amazon.in/dp/{}'.format(asin)})
        
        print(len(products))
        items['products'] = products
        yield items
