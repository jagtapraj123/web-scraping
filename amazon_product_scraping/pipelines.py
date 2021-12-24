# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from urllib.parse import quote
import pymongo
from itemadapter import ItemAdapter
from amazon_product_scraping.items import AmazonSearchProductList, AmazonProductInfoItem, AmazonProductDailyMovementItem, AmazonShareOfSearchItem, AmazonProductCommentsItem

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
        if spider.name == "AmazonTop100BSRSpider" or spider.name == "AmazonSearchListSpider":
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
                                "product_url": product['product_url']
                            }
                        },
                        upsert=True
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
                spider.urls.append("https://www.amazon.in/s?k={}".format(quote(keyword).replace("%20", "+")))
                

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
            if isinstance(item, AmazonShareOfSearchItem):
                    spider.success_counts['added'] += 1
                    self.db[self.collection_name].find_one_and_update(
                        {
                            "time": spider.time,
                            "keyword": item['keyword']
                        },
                        {
                            "$push": {
                                "product_order": {
                                    "product_asin": item["product_asin"],
                                    "product_title": item["product_title"],
                                    "product_brand": item["product_brand"],
                                    "product_rank": item["product_rank"],
                                    "product_original_price": item["product_original_price"],
                                    "product_sale_price": item["product_sale_price"],
                                    "product_fullfilled": item["product_fullfilled"],
                                    "sponsored": item['sponsored']
                                }
                            }
                        },
                        upsert=True
                    )
        return item
