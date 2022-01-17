from amazon_product_scraping.items import AmazonShareOfSearchItem, AmazonSearchCount, AmazonShareOfSearchRanksItem
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
    rotate_user_agent : Boolean
        True
    allowed_domains : list
        contains base-URLs for the allowed domains for the spider to crawl
    start_urls : list
        a list of URLs for the spider to start crawling from
    """

    # Make Debug = False while deploying
    debug = False
    handle_httpstatus_all = True
    name = "AmazonShareOfSearchSpider"
    rotate_user_agent = True
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

        if self.cold_run:
            for url in self.urls:
                self.add_to_failed('count', {'url': url})

                yield WebScrapingApiRequest(
                    url = url,
                    callback = partial(self.parse_count, {'url': url})
                )
        else:
            for func, params in self.failed_urls:
                if func == 'count':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        callback = partial(self.parse_count, params)
                    )
                elif func == 'list':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        callback = partial(self.parse_product_list, params)
                    )
                elif func == 'data':
                    yield WebScrapingApiRequest(
                        url = params['url'],
                        callback = partial(self.parse_product_data, params)
                    )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = kwargs['failed_urls']
        self.cold_run = kwargs['cold_run']
        self.keywords = kwargs['keywords']
        self.pages = kwargs['pages']
        self.success_counts = kwargs['success_counts']
        self.time = kwargs['time']
        self.urls = []
        self.mongo_db = kwargs['mongo_db']
        self.present_check_func = None

    def add_to_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        if wrapper not in self.failed_urls:
            self.failed_urls.append(wrapper)
            return True
        else:
            return False

    def remove_from_failed(self, parser_func, params):
        wrapper = [parser_func, params]
        if self.debug:
            print("Removing", wrapper)
        if wrapper in self.failed_urls:
            self.failed_urls.remove(wrapper)
            return True
        else:
            return False

    def parse_count(self, params, response):
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
        print(params)

        failed = False
        if response.status != 200:
            failed = True

        item = AmazonSearchCount()
        if not failed:
            counts = (
                response.xpath('//*[@id="search"]/span/div//h1/div/div[1]/div/div/span[1]/text()')
                .extract_first()
            )
            print(counts)
            counts = counts.split() if isinstance(counts, str) else []
            print(counts)
            try:
                if 'over' in counts:
                    count = int(counts[counts.index('over')+1].replace(',', ''))
                    per_page = int(counts[counts.index('of')-1].split('-')[1].replace(',', ''))
                elif 'of' in counts:
                    count = int(counts[counts.index('of')+1].replace(',', ''))
                    per_page = int(counts[counts.index('of')-1].split('-')[1].replace(',', ''))
                else:
                    count = int(counts[counts.index('results')-1].replace(',', ''))
                    per_page = count
            except:
                count = None
                print("No count of products found")
                failed = True
        
        if not failed:
            item["count"] = count
            print("**********\n Count:", count)

        if failed:
            if self.debug:
                with open('fails/OP_{}.html'.format('temp_count_fail'), 'w', encoding='utf-8') as f:
                    f.write(response.text)
            yield None
        else:
            if self.debug:
                with open('fails/OP_{}.html'.format('temp_count_succ'), 'w', encoding='utf-8') as f:
                    f.write(response.text)
            self.remove_from_failed('count', params)
            yield item
            if isinstance(count, int):
                for i in range(1, min(self.pages+1, ceil(count/per_page)+1)):
                    next_page_url = params['url'] + "&page={}".format(i)
                    self.add_to_failed('list', {'url': next_page_url})
                    yield WebScrapingApiRequest(
                        url = next_page_url,
                        callback= partial(self.parse_product_list, {'url': next_page_url}),
                        # meta={
                        #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                        # }
                    )

    def parse_product_list(self, params, response):
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

        items = AmazonShareOfSearchRanksItem()
        keyword = ' '.join(params['url'].split('?k=')[1].split('&')[0].split('+'))
        page = int(params['url'].split('&page=')[1].split('&')[0])-1
        rank = page*60

        if not failed:
            # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div
            asins = response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div/@data-asin').extract()
            if len(asins) == 0:
                failed = True

        if failed:
            yield None
        else:
            self.remove_from_failed('list', params)

            i = 0
            product_ranks = []
            if self.debug:
                with open('fails/havells/OP_{}.html'.format(page), 'w', encoding='utf-8') as f:
                    f.write(response.text)
            for asin in asins:
                i += 1
                if asin != '':
                    # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/ div /div/div/div/div/div[2]/div[1]/div/span/a/span[2]/span
                    sponsored_text = response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[{}]/div//div/div/div/div/div[2]/div[1]/div/span/a/span[2]/span/text()'.format(i)).extract()
                    isSponsored = True if len(sponsored_text) > 0 else False
                    rank += 1
                    # print(rank, isSponsored)
                    '''
                    item['product_asin'] = asin
                    item['product_title'] = title
                    item['product_brand'] = brand
                    item['keyword'] = params['keyword']
                    item['product_rank'] = params['rank']
                    item['product_sale_price'] = sale_price
                    item['product_original_price'] = original_price
                    item['product_fullfilled'] = fullfilled
                    item['sponsored'] = params['sponsored']
                    '''
                    product_ranks.append({
                        'product_asin': asin,
                        'keyword': keyword,
                        'product_rank': rank,
                        'sponsored': isSponsored
                    })

                    if not self.present_check_func({'product_asin': asin}):
                        url = 'https://www.amazon.in/dp/{}'.format(asin)
                        # if isSponsored:
                        #     print('Sponsored', i, rank)
                        wrapper = {
                            'url': url
                        }

                        if self.add_to_failed('data', wrapper):
                            yield WebScrapingApiRequest(
                                url = url,
                                callback=partial(self.parse_product_data, wrapper),
                                # meta={
                                #     "proxy": "http://scraperapi:1ee5ce80f3bbdbad4407afda1384b61e@proxy-server.scraperapi.com:8001"
                                # }
                            )
            items['product_ranks'] = product_ranks
            yield items

    def parse_product_data(self, params, response):
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
        
        asin = params['url'].split('/dp/')[1].split('/')[0]
        item = AmazonShareOfSearchItem()
        helper = AmazonScrapingHelper()
        
        if not failed:
            if self.debug:
                print("title")
            try:
                title = helper.get_title(response)
            except Exception:
                title = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("brand")
            try:
                brand = helper.get_brand(response)
            except Exception:
                brand = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("offers")
            try:
                offers = helper.get_offers(response)
            except Exception:
                offers = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("orig_price")
            try:
                original_price = helper.get_original_price(response)
            except Exception:
                original_price = "NA"
                failed = True
        
        if not failed:
            if self.debug:
                print("category")
            try:
                category = helper.get_category(response)
            except Exception:
                category = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("icons")
            try:
                icons = helper.get_icons(response)
            except Exception:
                icons = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("details")
            try:
                product_details = helper.get_product_details_1(response, self.time)
                if product_details == {}:
                    product_details = helper.get_product_details_2(response, self.time)
                if product_details == {} and self.cold_run:
                    failed = True
            except Exception:
                product_details = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("imp_info")
            try:
                important_information = helper.get_important_information(response)
            except Exception:
                important_information = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("description")
            try:
                product_description = helper.get_product_description(response)
            except Exception:
                product_description = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("bought_together")
            try:
                bought_together = helper.get_bought_together(response)
            except Exception:
                bought_together = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("variations")
            try:
                variations = helper.get_variations(response)
            except Exception:
                variations = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("Sale Price")
            try:
                sale_price = helper.get_sale_price(response, self.time)['value']
            except Exception:
                sale_price = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("BSR")
            try:
                best_seller_rank = helper.get_best_seller_rank_1(response, self.time)['value']
                if best_seller_rank == "NA":
                    best_seller_rank = helper.get_best_seller_rank_2(response, self.time)['value']
            except Exception:
                best_seller_rank = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("fulfilled")
            try:
                fullfilled = helper.get_fullfilled(response, self.time)['value']
            except Exception:
                fullfilled = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("rating")
            try:
                rating = helper.get_rating(response, self.time)['value']
            except Exception:
                rating = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("reviews")
            try:
                total_reviews = helper.get_total_reviews(response, self.time)['value']
            except Exception:
                total_reviews = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("availability")
            try:
                availability = helper.get_availability(response, self.time)['value']
            except Exception:
                availability = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("sub discount")
            try:
                subscription_discount = helper.get_subscription_discount(response, self.time)['value']
            except Exception:
                subscription_discount = "NA"
                failed = True

        if not failed:
            if self.debug:
                print("Assigning")
            
            item["product_name"] = title
            item["product_brand"] = brand
            item["product_offers"] = offers
            item["product_original_price"] = original_price
            item["product_category"] = category
            item["product_icons"] = icons
            item["product_details"] = product_details
            item["product_asin"] = asin
            item["product_important_information"] = important_information
            item["product_description"] = product_description
            item["product_bought_together"] = bought_together
            item["product_variations"] = variations

            item["product_sale_price"] = sale_price
            item["product_rating"] = rating
            item["product_total_reviews"] = total_reviews
            item["product_best_seller_rank"] = best_seller_rank
            item["product_fullfilled"] = fullfilled
            item["product_availability"] = availability
            item["product_subscription_discount"] = subscription_discount
        
        if failed:
            yield None
        else:
            self.remove_from_failed('data', params)

            ############# TEMP ################
            if self.debug:
                # if sale_price == "NA" or sale_price is "":
                with open('fails/SP_{}.html'.format(asin), 'w', encoding='utf-8') as f:
                    f.write(response.text)
                # if original_price == "NA" or original_price is "":
                    # with open('fails/havells/OP_{}.html'.format(asin), 'w', encoding='utf-8') as f:
                    #     f.write(response.text)
                # print("**DEBUG:**/n {}".format(item))
            ####################################
                print("Sending to pipeline")
            yield item
            # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/span/div/div/div/div/div[2]/div[1]/div/span/a/span[2]/span
            # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/span/div/div/div/div/div[2]/div[1]/div/span/a/span[2]/span
            # //*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[4]/div/span/div/div/div/div/div[2]/div[1]/div/span/a/span[2]/span
