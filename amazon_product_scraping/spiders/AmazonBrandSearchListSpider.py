from amazon_product_scraping.items import AmazonSearchProductList
from webscrapingapi_scrapy_sdk import WebScrapingApiSpider, WebScrapingApiRequest
from functools import partial


class AmazonBrandSearchListSpider(WebScrapingApiSpider):
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
    name = "AmazonBrandSearchListSpider"
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
                self.add_to_failed('brand_list', {'url': url})
                yield WebScrapingApiRequest(
                    url = url,
                    params = {
                        'render_js': 1,
                        'wait_until': 'domcontentloaded',
                        'wait_for': 5000,
                    },
                    callback = partial(self.parse_brand_list, {'url': url}),
                )
        else:
            for func, params in self.failed_urls:
                if func == 'brand_list':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        params = {
                            'render_js': 1,
                            'wait_until': 'domcontentloaded',
                        'wait_for': 5000,
                        },
                        callback = partial(self.parse_brand_list, params),
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
        if self.debug:
            print("Adding: {}".format(wrapper))
        if wrapper not in self.failed_urls:
            self.failed_urls.append(wrapper)

    def remove_from_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        if wrapper in self.failed_urls:
            self.failed_urls.remove(wrapper)

    def parse_brand_list(self, params, response):
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
        if not failed:
            # //*[@id="a-page"]/div[2]/div
            # links_xpath = response.xpath('//*[@id="ekc875jqle"]/div/div//div//li//a/@href').extract()
            links_xpath = response.xpath('//*[@id="a-page"]/div[2]/div//div/div//div//li//a/@href').extract()
            
            if len(links_xpath) == 0:
                failed = True

            links = [i for i in links_xpath if "/dp/" in i]
            # asins = [(i.split("/dp/")[1]).split("/")[0] for i in links]
            # asins = [i.split("/dp/")[1].split("/")[0].split('?')[0] for i in links]
            asins = []
            for i in links:
                try:
                    asins.append(i.split("/dp/")[1].split("/")[0].split('?')[0])
                except:
                    pass
            if len(asins) == 0:
                failed = True

        if not failed:
            products = []
            for asin in asins:
                products.append({'product_asin': asin, 'product_url': 'https://www.amazon.in/dp/{}'.format(asin)})
            
            print(len(products))
            item['products'] = products
        
        if failed:
            yield None
            if self.debug:
                print("**DEBUG:**/n {}".format(str(item).encode('utf-8')))
                with open('fails/Brand_Search_{}.html'.format(params['url'].split('/')[-1]), 'w', encoding='utf-8') as f:
                    f.write(response.text)
        else:
            # if self.debug:
            #     print("**DEBUG:**/n {}".format(item))
            #     with open('fails/100_BSR_{}.html'.format(params['url'].split('/')[-1]), 'w', encoding='utf-8') as f:
            #         f.write(response.text)
            self.remove_from_failed('brand_list', params)
            yield item
