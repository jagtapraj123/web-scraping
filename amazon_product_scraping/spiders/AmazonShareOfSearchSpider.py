import scrapy
from scrapy import settings
from amazon_product_scraping.items import AmazonShareOfSearchItem
from math import ceil
from functools import partial
from amazon_product_scraping.utils.AmazonScrapingHelper import AmazonScrapingHelper
from webscrapingapi_scrapy_sdk import WebScrapingApiSpider, WebScrapingApiRequest


class AmazonShareOfSearchSpider(WebScrapingApiSpider):
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
    name = "AmazonShareOfSearchSpider"
    rotate_user_agent = True
    # allowed_domains = ["amazon.in"]
    # urls = [
    #     "https://www.amazon.in/s?k=hair+fall+control+shampoo"
    # ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_product_scraping.pipelines.ShareOfSearchPipeline': 300
        }
    }

    def start_requests(self):
        """
        This class method must return an iterable with the first Requests to crawl for this spider.

        Set our proxy port http://scraperapi:API_KEY@proxy-server.scraperapi.com:8001 as the proxy in the meta parameter.
        """

        for url in self.urls:
            yield WebScrapingApiRequest(
                url=url,
                callback=partial(self.parse_product_list, url)
                # meta={
                #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                # }
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = kwargs['failed_urls']
        self.cold_run = kwargs['cold_run']
        self.keywords = kwargs['keywords']
        self.pages = kwargs['pages']
        self.success_counts = kwargs['success_counts']
        self.urls = []


    # def parse_count(self, response):
    #     """
    #     A class method used to parse the response for each request, extract scraped data as dicts.

    #     Parameters
    #     ----------
    #     response : object
    #         represents an HTTP response

    #     Returns
    #     -------
    #     count
    #         extracted count of products appearing in search
    #     """

    #     if response.status != 200:
    #         if response.url not in self.failed_urls:
    #             self.failed_urls.append(response.url)

    #     item = AmazonSearchCount()
    #     counts = (
    #         response.xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()')
    #         .extract_first()
    #     )
    #     print(counts)
    #     counts = counts.split() if isinstance(counts, str) else []
    #     print(counts)
    #     try:
    #         count = int(counts[counts.index('of')+1].replace(',', ''))
    #     except:
    #         try:
    #             count = int(counts[counts.index('over')+1].replace(',', ''))
    #         except:
    #             count = 0
    #             print("No count of products found")
    #             if response.url not in self.failed_urls:
    #                 self.failed_urls.append(response.url)

    #     item["count"] = count
    #     print("**********\n Count:", count)
    #     yield item
    #     # TODO Remove '/5'
    #     for i in range(1, ceil(count/48)):
    #         yield scrapy.Request(
    #             url = response.url + "&page={}".format(i),
    #             callback=self.parse_product_list,
    #             # meta={
    #             #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
    #             # }
    #         )

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
        print(response.url, response.status)
        print(url)
        if response.status != 200:
            if url not in self.failed_urls:
                self.failed_urls.append(url)
    
        # items = AmazonSearchProductList()
        # /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[1]
        # /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[2]
        # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]
        asins = response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div/@data-asin').extract()
        # asins.remove('')
        # products = []
        # for asin in asins:
        #     products.append({'product_asin': asin, 'product_url': 'https://www.amazon.in/dp/{}'.format(asin)})
        
        # if len(asins) == 0:
        #     if response.status != 200:
        #         if url not in self.failed_urls:
        #             self.failed_urls.append(url)

        # items['products'] = products
        # # print("****\nItem:", items)
        # yield items
        keyword = ' '.join(url.split('?k=')[1].split('&')[0].split('+'))
        page = int(url.split('&page=')[1].split('&')[0])-1
        rank = page*60
        yield None
        for asin in asins:
            if asin != '':
                rank += 1
                url = 'https://www.amazon.in/dp/{}'.format(asin)
                # print(url)
                yield WebScrapingApiRequest(
                    url = url,
                    callback=partial(self.parse_product_data, url, keyword, rank),
                    # meta={
                    #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                    # }
                )

    def parse_product_data(self, url, keyword, rank, response):
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

        # if response.status != 200:
        #     if url not in self.failed_urls:
                # self.failed_urls.append(url)
        print(response.url, response.status)
        print(url)
        asin = url.split('/dp/')[1].split('/')[0]
        item = AmazonShareOfSearchItem()
        helper = AmazonScrapingHelper()

        try:
            title = helper.get_title(response)
        except Exception:
            # logging.error("Exception occurred", exc_info=True)
            title = "NA"
            # if url not in self.failed_urls:
            #     self.failed_urls.append(url)

        try:
            brand = helper.get_brand(response)
        except Exception:
            # logging.error("Exception occurred", exc_info=True)
            brand = "NA"
            # if url not in self.failed_urls:
            #     self.failed_urls.append(url)

        try:
            sale_price = helper.get_sale_price(response)['value']
        except Exception:
            # logging.error("Exception occurred", exc_info=True)
            sale_price = "NA"
            # if url not in self.failed_urls:
            #     self.failed_urls.append(url)

        try:
            original_price = helper.get_original_price(response)
        except Exception:
            # logging.error("Exception occurred", exc_info=True)
            original_price = "NA"
            # if url not in self.failed_urls:
            #     self.failed_urls.append(url)

        try:
            fullfilled = helper.get_fullfilled(response)['value']
        except Exception:
            # logging.error("Exception occurred", exc_info=True)
            fullfilled = "NA"
            # if url not in self.failed_urls:
            #     self.failed_urls.append(url)

        item['product_asin'] = asin
        item['product_title'] = title
        item['product_brand'] = brand
        item['keyword'] = keyword
        item['product_rank'] = rank
        item['product_sale_price'] = sale_price
        item['product_original_price'] = original_price
        item['product_fullfilled'] = fullfilled
        # print(item)
        yield item