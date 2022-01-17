# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from urllib.parse import quote
import pymongo
from itemadapter import ItemAdapter
from amazon_product_scraping.items import AmazonSearchProductList, AmazonProductInfoItem, AmazonProductDailyMovementItem, AmazonShareOfSearchItem, AmazonProductCommentsItem, AmazonShareOfSearchRanksItem
from amazon_product_scraping.items import FlipkartSearchProductList, FilpkartProductInfoItem, FlipkartProductDailyMovementItem, FlipkartShareOfSearchItem, FlipkartRankItem, FlipkartProductCommentsItem

class CommentsToMongoPipeline:
    """
    A class used to save the scraped item in MongoDB.

    Attributes
    ----------
    collection_name : str
        MongoDB collection name
    mongo_uri : str
        MongoDB address
    mongo_db : str
        MongoDB database name
    """
    input_collection_name = "product_list"
    output_collection_name = "product_comments"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nComments Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0}))
            # spider.urls = []
            for prod in input_prods:
                # spider.urls.append(prod['product_url'])
                if spider.count > 0:
                    # for i in range(1, 1+math.ceil(spider.count/10)):
                    i = 1
                    spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={}".format(prod['product_asin'], i))
                    # spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=five_star&pageNumber={}".format(prod['product_asin'], i))
                    # spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=four_star&pageNumber={}".format(prod['product_asin'], i))
                    # spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=three_star&pageNumber={}".format(prod['product_asin'], i))
                    # spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=two_star&pageNumber={}".format(prod['product_asin'], i))
                    # spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=one_star&pageNumber={}".format(prod['product_asin'], i))
                        # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={}".format(
                        #     prod['product_asin'], i
                        # ).encode('utf-8'))))
                else:
                    spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={}".format(prod['product_asin'], 1))
                    # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={}".format(
                    #     prod['product_asin'], 1
                    # ).encode('utf-8'))))
        # if spider.cold_run:
        #     asins_list = pd.read_csv('../data_csvs/asins.csv')
        #     for asin in asins_list['ASIN']:
        #         print(asin)
        #         for i in range(1, 1+math.ceil(spider.count/10)):
        #             spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=five_star&pageNumber={}".format(asin, i))
        #             spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=four_star&pageNumber={}".format(asin, i))
        #             spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=three_star&pageNumber={}".format(asin, i))
        #             spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=two_star&pageNumber={}".format(asin, i))
        #             spider.urls.append("https://www.amazon.in/Himalaya-Herbals-Anti-Shampoo-400ml/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&filterByStar=one_star&pageNumber={}".format(asin, i))


    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        if spider.name == "AmazonProductCommentsSpider" and isinstance(item, AmazonProductCommentsItem):
            # existing_item = self.db[self.collection_name_comments].find_one(
            #     {"product_asin": item["product_asin"]}
            # )
            # print("****ITEM:\n", item)
            print(len(item['product_comments']))
            spider.success_counts['prods_checked'] += 1
            spider.success_counts['prods_with_new_comms'] += 1 if len(item['product_comments']) > 0 else 0
            spider.success_counts['new_comments'] += len(item['product_comments'])

            for comment in item["product_comments"]:
                comment["date"] = comment["date"].strftime("%Y-%m-%d %H:%M:%S")
                self.db[self.output_collection_name].find_one_and_update(
                    {"product_asin": item["product_asin"]},
                    {
                        "$push": {
                            "comments": comment,
                        }
                    },
                    upsert=True,
                )
            return item

class NewListingProductURLToMongoPipeline:
    
    collection_name = "product_list"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db
        self.company_client = spider.company_client

        print("*******\nNew Listing URL Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        if spider.name == "AmazonTop100BSRSpider" or spider.name == "AmazonSearchListSpider" or spider.name == "AmazonBrandSearchListSpider":
            if isinstance(item, AmazonSearchProductList):
                present = 0
                not_present = 0
                for product in item['products']:
                    existing_item = self.db[self.collection_name].find_one(
                        {"product_asin": product["product_asin"]}
                    )
                    # print("*****\nITEM:", item)
                    # print(product, "Not Present" if existing_item is None else "Present")
                    if existing_item is None:
                        not_present += 1
                    else:
                        present += 1
                    self.db[self.collection_name].find_one_and_update(
                        {"product_asin": product['product_asin']},
                        {
                            "$set": {
                                "product_url": product['product_url'],
                            }
                        },
                        upsert=True
                    )
                    client_added = self.db[self.collection_name].find_one(
                        {"product_asin": product["product_asin"], "clients": self.company_client}
                    )
                    if not client_added:
                        self.db[self.collection_name].find_one_and_update(
                        {"product_asin": product['product_asin']},
                        {
                            "$push": {
                                "clients": self.company_client,
                            }
                        }
                    )
                print("New Added: {}, Hit: {}".format(not_present, present))
                spider.success_counts['new'] += not_present
                spider.success_counts['existing'] += present
        return item

class AmazonProductInfoToMongoPipeline:
    
    input_collection_name = "product_list"
    output_collection_name = "product_data"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI")
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nProduct Info Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0}))
            present_prods = set(map(lambda x: x['product_asin'], list(self.db[self.output_collection_name].find({}, {"_id": 0, "product_asin": 1}))))
            # urls = {}
            # spider.urls = []
            # print(present_prods)
            # print(len(present_prods))
            print("*****\nTo Add:")
            for prod in input_prods:
                if prod['product_asin'] not in present_prods:
                    print(prod['product_asin'])
                    spider.urls.append(prod['product_url'])
                    # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote(prod['product_url'].encode('utf-8'))))
            print("END\n*****")


    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "AmazonProductInfoSpider":
            spider.success_counts['new'] += 1
            if isinstance(item, AmazonProductInfoItem):
                # existing_item = self.db[self.collection_name].find_one(
                #     {"product_asin": item["product_asin"]}
                # )
                # print(item)
                spider.success_counts['added'] += 1
                self.db[self.output_collection_name].insert_one(ItemAdapter(item).asdict())
        
        return item

class AmazonProductDailyMovementToMongoPipeline:
    
    input_collection_name = "product_list"
    output_collection_name = "product_data"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nProduct Daily Movement Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0, "product_asin": 0}))
            # spider.urls = []
            for prod in input_prods:
                spider.urls.append(prod['product_url'])
                # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote(prod['product_url'].encode('utf-8'))))
        

    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "AmazonProductSalePriceBSRSpider":
            spider.success_counts['new'] += 1
            if isinstance(item, AmazonProductDailyMovementItem):
                existing_item = self.db[self.output_collection_name].find_one(
                    {"product_asin": item["product_asin"]}
                )
                if (
                    existing_item
                    and item["product_asin"] != "NA"
                ):
                    spider.success_counts['added'] += 1
                    # print("****ITEM:\n", item)
                    self.db[self.output_collection_name].find_one_and_update(
                        {"product_asin": item["product_asin"]},
                        {
                            "$push": {
                                "product_sale_price": item["product_sale_price"],
                                "product_best_seller_rank": item[
                                    "product_best_seller_rank"
                                ],
                                "product_fullfilled": item["product_fullfilled"],
                                "product_availability": item["product_availability"],
                                "product_subscription_discount": item[
                                    "product_subscription_discount"
                                ],
                                "product_rating": item["product_rating"],
                                "product_total_reviews" : item["product_total_reviews"],

                            }
                        },
                        upsert=True,
                    )
        return item

class ShareOfSearchPipeline:
    
    list_collection_name = "share_of_search"
    data_collection_name = "sos_data"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db
        self.company_client = spider.company_client

        print("********\nShare of Search Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        spider.present_check_func = self.present_check
        if spider.cold_run:
            for keyword in spider.keywords:
                spider.urls.append("https://www.amazon.in/s?k={}".format(quote(keyword).replace("%20", "+")))
                
    def present_check(self, filter):
        print(filter)
        print(self.db[self.data_collection_name].find_one(filter) is not None)
        return self.db[self.data_collection_name].find_one(filter) is not None


    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "AmazonShareOfSearchSpider":
            if isinstance(item, AmazonShareOfSearchRanksItem):
                for prod in item['product_ranks']:
                    spider.success_counts['ranked'] += 1
                    self.db[self.list_collection_name].find_one_and_update(
                        {
                            "time": spider.time,
                            "keyword": prod['keyword'],
                            "clients": self.company_client
                        },
                        {
                            "$push": {
                                "product_order": {
                                    "product_asin": prod['product_asin'],
                                    "product_rank": prod['product_rank'],
                                    "sponsored": prod['sponsored']
                                }
                            }
                        },
                        upsert = True
                    )
            elif isinstance(item, AmazonShareOfSearchItem):
                    spider.success_counts['added'] += 1
                    print(str(ItemAdapter(item).asdict()).encode('utf-8'))
                    self.db[self.data_collection_name].find_one_and_update(
                        {
                            "product_asin": item['product_asin']
                        },
                        {
                            "$set": ItemAdapter(item).asdict(),
                        },
                        upsert=True
                    )
        return item

class FlipkartNewListingProductURLToMongoPipeline:
    
    collection_name = "product_list"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nNew Listing URL Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        if spider.name == "FlipkartSearchListSpider":
            if isinstance(item, FlipkartSearchProductList):
                present = 0
                not_present = 0
                for product in item['products']:
                    existing_item = self.db[self.collection_name].find_one(
                        {
                            "product_pid": product["product_pid"],
                            # "product_lid": product["product_lid"],
                            "marketplace": product["marketplace"]
                        },
                    )
                    # print("*****\nITEM:", item)
                    # print(product, "Not Present" if existing_item is None else "Present")
                    if existing_item is None:
                        not_present += 1
                    else:
                        present += 1
                    self.db[self.collection_name].find_one_and_update(
                        {
                            "product_pid": product["product_pid"],
                            "marketplace": product["marketplace"]
                        },
                        {
                            "$set": {
                                "product_lid": product["product_lid"],
                                "product_url": product["product_url"]
                            }
                        },
                        upsert=True
                    )
                print("New Added: {}, Hit: {}".format(not_present, present))
                spider.success_counts['new'] += not_present
                spider.success_counts['existing'] += present
        return item

class FlipkartProductInfoToMongoPipeline:
    
    input_collection_name = "product_list"
    output_collection_name = "product_data"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI")
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """
        def hash(pid, marketplace):
            return pid + "--" + marketplace

        self.mongo_db = spider.mongo_db

        print("*******\nProduct Info Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0}))
            present_prods = set()
            for p in list(self.db[self.output_collection_name].find({}, {"_id": 0, "product_pid": 1, "marketplace": 1, "scraped_on": 1})):
                if 'scraped_on' in p.keys():
                    present_prods.add(hash(p['product_pid'], p['marketplace']))
            # print(presents)
            # present_prods = set(map(lambda x: hash(x['product_pid'], x['marketplace']), list(self.db[self.output_collection_name].find({}, {"_id": 0, "product_pid": 1, "product_lid": 1, "marketplace": 1, "scraped_on": 1}))))
            # urls = {}
            # spider.urls = []
            # print(present_prods)
            print(len(present_prods))
            print("*****\nTo Add:")
            i = 0
            for prod in input_prods:
                if hash(prod['product_pid'], prod['marketplace']) not in present_prods:
                    i += 1
                    print(i, prod['product_pid'])
                    # spider.urls.append(prod['product_url'])
                    # spider.urls.append('{}?pid={}&marketplace={}'.format(prod['product_url'].split('?')[0], prod['product_pid'], prod['marketplace']))
                    spider.urls.append({'url': '{}?pid={}&marketplace={}'.format(prod['product_url'].split('?')[0], prod['product_pid'], "FLIPKART"), 'marketplace': prod['marketplace']})
                    print(spider.urls[-1])
                    # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote(prod['product_url'].encode('utf-8'))))
            print("END\n*****")
            
    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "FlipkartProductInfoSpider":
            spider.success_counts['new'] += 1
            if isinstance(item, FilpkartProductInfoItem):
                # existing_item = self.db[self.collection_name].find_one(
                #     {"product_asin": item["product_asin"]}
                # )
                # print(item)
                spider.success_counts['added'] += 1
                # self.db[self.output_collection_name].insert_one(ItemAdapter(item).asdict())
                self.db[self.output_collection_name].find_one_and_update(
                    {
                        "product_pid": item["product_pid"],
                        # "product_lid": item["product_lid"],
                        "marketplace": item["marketplace"]
                    },
                    {
                        "$set": ItemAdapter(item).asdict()
                    },
                    upsert=True
                )
        
        return item


class FlipkartProductDailyMovementToMongoPipeline:
    
    input_collection_name = "product_list"
    output_collection_name = "product_data"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nProduct Daily Movement Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0}))
            spider.urls = []
            for prod in input_prods:
                # spider.urls.append(prod['product_url'])
                # spider.urls.append('{}?pid={}&marketplace={}'.format(prod['product_url'].split('?')[0], prod['product_pid'], prod['marketplace']))
                spider.urls.append({'url': '{}?pid={}&marketplace={}'.format(prod['product_url'].split('?')[0], prod['product_pid'], "FLIPKART"), 'marketplace': prod['marketplace']})

                # print(spider.urls[-1])
                # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote(prod['product_url'].encode('utf-8'))))
        

    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "FlipkartProductSalePriceSpider":
            spider.success_counts['new'] += 1
            if isinstance(item, FlipkartProductDailyMovementItem):
                existing_item = self.db[self.output_collection_name].find_one(
                    {
                        "product_pid": item["product_pid"],
                        # "product_lid": item["product_lid"],
                        "marketplace": item["marketplace"]
                    },
                )
                if (
                    existing_item
                    and item["product_pid"] != "NA"
                ):
                    spider.success_counts['added'] += 1
                    # print("****ITEM:\n", item)
                    self.db[self.output_collection_name].find_one_and_update(
                        {
                            "product_pid": item["product_pid"],
                            # "product_lid": item["product_lid"],
                            "marketplace": item["marketplace"]
                        },
                        {
                            "$push": {
                                "product_sale_price": item["product_sale_price"],
                                "product_availability": item["product_availability"],
                                "product_rating": item["product_rating"],
                                "product_total_reviews" : item["product_total_reviews"],
                            }
                        },
                        upsert=True,
                    )
        return item

class FlipkartShareOfSearchPipeline:
    
    collection_name = "share_of_search"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("********\nShare of Search Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            for keyword in spider.keywords:
                spider.urls.append("https://www.flipkart.com/search?q={}".format(quote(keyword)))
                

    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "FlipkartShareOfSearchSpider":
            if isinstance(item, FlipkartShareOfSearchItem):
                    spider.success_counts['added'] += 1
                    self.db[self.collection_name].find_one_and_update(
                        {
                            "time": spider.time,
                            "keyword": item['keyword']
                        },
                        {
                            "$push": {
                                "product_order": {
                                    "product_pid": item["product_pid"],
                                    "product_lid": item["product_lid"],
                                    "marketplace": item["marketplace"],
                                    "product_url": item["product_url"],
                                    "product_title": item["product_title"],
                                    "product_brand": item["product_brand"],
                                    "product_rank": item["product_rank"],
                                    "product_original_price": item["product_original_price"],
                                    "product_sale_price": item["product_sale_price"]
                                }
                            }
                        },
                        upsert=True
                    )
        return item

class FlipkartProductRankPipeline:
    
    list_collection_name = "product_list"
    data_collection_name = "product_data"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nFlipkart Product Rank Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        

    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        
        if spider.name == "FlipkartProductRankSpider":
            if isinstance(item, FlipkartRankItem):
                found = 0
                present = 0
                not_present = 0
                for product in item['product_ranks']:
                    if product["product_pid"] != "NA":
                        found += 1
                        if product["add"] == "push":
                            self.db[self.data_collection_name].find_one_and_update(
                                {
                                    "product_pid": product["product_pid"],
                                    # "product_lid": product["product_lid"],
                                    "marketplace": product["marketplace"]
                                },
                                {   
                                    "$push": {
                                        "product_rank": product["product_rank"],
                                    }
                                },
                                upsert=True,
                            )
                        elif product["add"] == "reset":
                            self.db[self.data_collection_name].find_one_and_update(
                                {
                                    "product_pid": product["product_pid"],
                                    # "product_lid": product["product_lid"],
                                    "marketplace": product["marketplace"],
                                    "product_rank.time": product["product_rank"]["time"]
                                },
                                {   
                                    "$set": {
                                        "product_rank.$.value": product["product_rank"]["value"],
                                    }
                                },
                                upsert=True,
                            )
                        existing_item = self.db[self.list_collection_name].find_one(
                            {
                                "product_pid": product["product_pid"],
                                # "product_lid": product["product_lid"],
                                "marketplace": product["marketplace"]
                            }
                        )
                        if existing_item is None:
                            not_present += 1
                            self.db[self.list_collection_name].find_one_and_update(
                                {
                                    "product_pid": product["product_pid"],
                                    # "product_lid": product["product_lid"],
                                    "marketplace": product["marketplace"]
                                },
                                {
                                    "$set": {
                                        "product_lid": product["product_lid"],
                                        "product_url": product['product_url']
                                    }
                                },
                                upsert=True
                            )
                        else:
                            present += 1
                spider.success_counts['found'] += found
                spider.success_counts['new'] += not_present
                spider.success_counts['added'] += present + not_present

        return item


# https://www.flipkart.com/head-shoulders-anti-hair-fall-shampoo-360ml/p/itmffvtwmtfmrpby?pid=SMPFFVGSCZ9JMU8B&lid=LSTSMPFFVGSCZ9JMU8B92Q2F4&marketplace=FLIPKART&q=shampoo&store=g9b%2Flcf%2Fqqm%2Ft36&srno=s_3_100&otracker=search&otracker1=search&fm=organic&iid=2d720238-1e7e-474a-a637-aa1d85a5c8ef.SMPFFVGSCZ9JMU8B.SEARCH&ppt=None&ppn=None&ssid=718tat5h9s0000001641302776577&qH=186764a607df448c
# https://www.flipkart.com/head-shoulders-anti-hair-fall-shampoo-360ml/p/itmffvtwmtfmrpby?pid=SMPFFVGSCZ9JMU8B&lid=LSTSMPFFVGSCZ9JMU8B92Q2F4&marketplace=FLIPKART&q=shampoo&store=g9b%2Flcf%2Fqqm%2Ft36&srno=s_3_110&otracker=search&otracker1=search&fm=organic&iid=21a1d23d-a8bd-4b07-8b43-a5b50865a325.SMPFFVGSCZ9JMU8B.SEARCH&ppt=None&ppn=None&ssid=5ibti7unr40000001641364501870&qH=186764a607df448c

class FlipkartCommentsToMongoPipeline:
    """
    A class used to save the scraped item in MongoDB.

    Attributes
    ----------
    collection_name : str
        MongoDB collection name
    mongo_uri : str
        MongoDB address
    mongo_db : str
        MongoDB database name
    """
    input_collection_name = "product_list"
    output_collection_name = "product_comments2"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.mongo_db = spider.mongo_db

        print("*******\nComments Pipeline Started : {}\n********".format(self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0}))
            # spider.urls = []
            for prod in input_prods:
                # spider.urls.append(prod['product_url'])
                if spider.count > 0:
                    # for i in range(1, 1+math.ceil(spider.count/10)):
                    i = 1
                    spider.urls.append({'url': "https://www.flipkart.com/head-shoulders-smooth-silky-anti-dandruff-shampoo/product-reviews/itmc8a771e408aac?pid={}&marketplace={}&sortOrder=MOST_RECENT&page={}".format(prod['product_pid'], "FLIPKART", i), 'marketplace': prod['marketplace']})
                else:
                    spider.urls.append({'url': "https://www.flipkart.com/head-shoulders-smooth-silky-anti-dandruff-shampoo/product-reviews/itmc8a771e408aac?pid={}&marketplace={}&sortOrder=MOST_RECENT&page={}".format(prod['product_pid'], "FLIPKART", 1), 'marketplace': prod['marketplace']})


    def close_spider(self, spider):
        """
        This class method is called when the spider is closed.

        Parameters
        ----------
        spider : object
            the spider which was closed
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        This class method is called for every item pipeline component.

        Parameters
        ----------
        item : item object
            the scraped item
        spider : object
            the spider which scraped the item
        """
        if spider.name == "FlipkartProductCommentsSpider" and isinstance(item, FlipkartProductCommentsItem):
            # existing_item = self.db[self.collection_name_comments].find_one(
            #     {"product_asin": item["product_asin"]}
            # )
            # print("****ITEM:\n", item)
            print(len(item['product_comments']))
            spider.success_counts['prods_checked'] += 1
            spider.success_counts['prods_with_new_comms'] += 1 if len(item['product_comments']) > 0 else 0
            spider.success_counts['new_comments'] += len(item['product_comments'])

            for comment in item["product_comments"]:
                comment["date"] = comment["date"].strftime("%Y-%m-%d %H:%M:%S")
                self.db[self.output_collection_name].find_one_and_update(
                    {
                        "product_asin": item["product_pid"],
                        "marketplace": item["marketplace"],
                    },
                    {
                        "$set": {
                            "scraped_on": item["scraped_on"]
                    },
                        "$push": {
                            "comments": comment,
                        }
                    },
                    upsert=True,
                )
            return item
