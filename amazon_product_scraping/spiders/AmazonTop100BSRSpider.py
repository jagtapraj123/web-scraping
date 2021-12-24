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
    rotate_user_agent : Boolean
        True
    allowed_domains : list
        contains base-URLs for the allowed domains for the spider to crawl
    start_urls : list
        a list of URLs for the spider to start crawling from
    """

    debug = False
    handle_httpstatus_all = True
    name = "AmazonTop100BSRSpider"
    rotate_user_agent = True
    
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
        
        if self.cold_run:
            for url in self.urls:
                self.add_to_failed('bsr_list', {'url': url})
                yield WebScrapingApiRequest(
                    url = url,
                    callback = partial(self.parse_bsr_list, {'url': url})
                )
        else:
            for func, params in self.failed_urls:
                if func == 'bsr_list':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        callback = partial(self.parse_bsr_list, params)
                    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = kwargs['failed_urls']
        self.cold_run = kwargs['cold_run']
        self.success_counts = kwargs['success_counts']
        self.mongo_db = kwargs['mongo_db']
        if self.cold_run:
            self.urls = kwargs['start_urls']
        else:
            self.urls = []

    def add_to_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        print("Adding: {}".format(wrapper))
        if wrapper not in self.failed_urls:
            self.failed_urls.append(wrapper)

    def remove_from_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        if wrapper in self.failed_urls:
            self.failed_urls.remove(wrapper)

    def parse_bsr_list(self, params, response):
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
        print(params)

        failed = False
        if response.status != 200:
            failed = True

        item = AmazonSearchProductList()
        links_xpath = response.xpath('//div[@id="zg-center-div"]').xpath('//a[@class="a-link-normal"]/@href').extract()
        
        if len(links_xpath) == 0:
            failed = True
        try:
            links = [i for i in links_xpath if "/dp/" in i]
            # asins = [(i.split("/dp/")[1]).split("/")[0] for i in links]
            asins = [(i.split("/dp/")[1]).split("/")[0].split('?')[0] for i in links]
        except:
            failed = True
        # bsr_xpath = response.xpath(
        #     '//div[@id="zg-center-div"]//span//span//text()'
        # ).extract()
        # bsr = [i + " in Shampoos (Beauty)" for i in bsr_xpath if "#" in i]

        # item["links"] = links
        # item["asin"] = asin
        # item["bsr"] = bsr

        products = []
        for asin in asins:
            products.append({'product_asin': asin, 'product_url': 'https://www.amazon.in/dp/{}'.format(asin)})
        
        print(len(products))
        item['products'] = products
        if failed:
            yield None
            if self.debug:
                print("**DEBUG:**/n {}".format(item))
                with open('fails/100_BSR_{}.html'.format(params['url'].split('/')[-1]), 'w', encoding='utf-8') as f:
                    f.write(response.text)
        else:
            # if self.debug:
            #     print("**DEBUG:**/n {}".format(item))
            #     with open('fails/100_BSR_{}.html'.format(params['url'].split('/')[-1]), 'w', encoding='utf-8') as f:
            #         f.write(response.text)
            self.remove_from_failed('bsr_list', params)
            yield item
