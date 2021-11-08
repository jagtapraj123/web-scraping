# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from urllib.parse import quote
import pymongo
from itemadapter import ItemAdapter
from datetime import datetime
from pymongo import ReturnDocument
import pandas as pd
from csv import writer
import math

from scrapy import crawler
from amazon_product_scraping.items import AmazonSearchCount, AmazonSearchProductList, AmazonProductInfoItem, AmazonProductDailyMovementItem, AmazonShareOfSearchItem


# class MongoDBPipeline:
#     """
#     A class used to save the scraped item in MongoDB.

#     Attributes
#     ----------
#     collection_name : str
#         MongoDB collection name
#     mongo_uri : str
#         MongoDB address
#     mongo_db : str
#         MongoDB database name
#     """

#     collection_name = "product_data"
#     collection_name_comments = "product_comments"

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         """
#         A class method used to pull in information from settings.py.
#         """

#         return cls(
#             mongo_uri=crawler.settings.get("MONGO_URI"),
#             mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
#         )

#     def open_spider(self, spider):
#         """
#         This class method is called when initializing spider and opening MongoDB connection.

#         Parameters
#         ----------
#         spider : object
#             the spider which was opened
#         """

#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         print("*******\nStarted\n********")

#     def close_spider(self, spider):
#         """
#         This class method is called when the spider is closed.

#         Parameters
#         ----------
#         spider : object
#             the spider which was closed
#         """

#         self.client.close()

#     def process_item(self, item, spider):
#         """
#         This class method is called for every item pipeline component.

#         Parameters
#         ----------
#         item : item object
#             the scraped item
#         spider : object
#             the spider which scraped the item
#         """

#         if spider.name == "AmazonProductInfoSpider":
#             existing_item = self.db[self.collection_name].find_one(
#                 {"product_asin": item["product_asin"]}
#             )
#             if (
#                 not existing_item
#                 and item["product_details"] != {}
#                 and item["product_asin"] != "NA"
#             ):
#                 self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
#                 # self.db[self.collection_name].find_one_and_update(
#                 #     {"product_asin": item["product_asin"]},
#                 #     {
#                 #         "$set": {
#                 #             "product_name": item["product_name"],
#                 #             "product_brand": item["product_brand"],
#                 #             "product_offers": item["product_offers"],
#                 #             "product_original_price": item["product_original_price"],
#                 #             # "product_fullfilled": item["product_fullfilled"],
#                 #             "product_rating": item["product_rating"],
#                 #             "product_total_reviews": item["product_total_reviews"],
#                 #             # "product_availability": item["product_availability"],
#                 #             "product_category": item["product_category"],
#                 #             "product_icons": item["product_icons"],
#                 #             "product_details": item["product_details"],
#                 #             "product_important_information": item["product_important_information"],
#                 #             "product_description": item["product_description"],
#                 #             "product_bought_together": item["product_bought_together"],
#                 #             # "product_subscription_discount": item[
#                 #                 # "product_subscription_discount"
#                 #             # ],
#                 #             "product_variations": item["product_variations"]
#                 #         }
#                 #     },
#                 #     upsert=True,
#                 # )
#             return item

#         if spider.name == "AmazonProductSalePriceBSRSpider":
#             existing_item = self.db[self.collection_name].find_one(
#                 {"product_asin": item["product_asin"]}
#             )
#             if (
#                 existing_item
#                 and item["product_details"] != {}
#                 and item["product_asin"] != "NA"
#             ):
#                 self.db[self.collection_name].find_one_and_update(
#                     {"product_asin": item["product_asin"]},
#                     {
#                         "$push": {
#                             "product_sale_price": item["product_sale_price"][0],
#                             "product_best_seller_rank": item[
#                                 "product_best_seller_rank"
#                             ][0],
#                             "product_fullfilled": item["product_fullfilled"][0],
#                             "product_availability": item["product_availability"][0],
#                             "product_subscription_discount": item[
#                                 "product_subscription_discount"
#                             ][0],
#                         }
#                     },
#                     upsert=True,
#                 )
#             return item

#         if spider.name == "AmazonTop100BSRSpider":
#             for i, j in zip(item["asin"], item["bsr"]):
#                 existing_item = self.db[self.collection_name].find_one(
#                     {"product_asin": i}
#                 )
#                 if existing_item:
#                     now = datetime.now()
#                     current_time = now.strftime("%Y-%m-%d %H:%M:%S")
#                     best_seller_rank = {}
#                     best_seller_rank["time"] = current_time
#                     best_seller_rank["value"] = j
#                     self.db[self.collection_name].find_one_and_update(
#                         {"product_asin": i},
#                         {
#                             "$push": {
#                                 "product_best_seller_rank": best_seller_rank,
#                             }
#                         },
#                         upsert=True,
#                     )
#             return item

#         if spider.name == "AmazonProductDuplicateBSRSpider":
#             urls = []
#             for i, j in zip(item["asin"], item["bsr"]):
#                 existing_item = self.db[self.collection_name].find_one(
#                     {"product_asin": i}
#                 )
#                 if not existing_item:
#                     urls.append("http://amazon.in/dp/" + i)

#             dict = {"URL": urls}
#             df = pd.DataFrame(dict)
#             df.drop(df.tail(1).index, inplace=True)
#             df.to_csv(
#                 "amazon_product_scraping/data/InputData/amazon_new_data.csv",
#                 index=False,
#             )

#             df1 = pd.read_csv(
#                 "amazon_product_scraping/data/InputData/amazon_product_data.csv"
#             )
#             combined = df1.append(df)
#             with open(
#                 "amazon_product_scraping/data/InputData/amazon_product_data.csv",
#                 "w",
#                 encoding="utf-8",
#                 newline="",
#             ) as file:
#                 combined.to_csv(file, index=False)

#             return item

#         # if spider.name == "AmazonProductCommentsSpider":
#         #     print("*****************\nRunning Here\n\n")
#         #     existing_item = self.db[self.collection_name_comments].find_one(
#         #         {"product_asin": item["product_asin"]}
#         #     )
#         #     for comment in item["product_comments"]:
#         #         self.db[self.collection_name_comments].find_one_and_update(
#         #             {"product_asin": item["product_asin"]},
#         #             {
#         #                 "$push": {
#         #                     "comments": comment,
#         #                 }
#         #             },
#         #             upsert=True,
#         #         )
#         #     return item

#         if spider.name == "AmazonSearchListSpider":
#             if isinstance(item, AmazonSearchCount):
#                 pass
#             if isinstance(item, AmazonSearchProductList):
#                 # TODO
#                 pass

#             return item

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

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

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
        #                 
        else:
            spider.urls = spider.failed_urls.copy()
            spider.failed_urls.clear()

        # print("******\n", spider.urls)
        
        print("*******\nComments Pipeline Started\n********")

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
        if spider.name == "AmazonProductCommentsSpider":
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

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # TODO Add URL selecting code
        if spider.cold_run:
            pass
        else:
            spider.urls = spider.failed_urls.copy()
            spider.failed_urls.clear()

        print("*******\nNew Listing URL Pipeline Started\n********")

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
        if isinstance(item, AmazonSearchProductList):
            if spider.name == "AmazonTop100BSRSpider" or spider.name == "AmazonSearchListSpider":
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

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0}))
            present_prods = set(map(lambda x: x['product_asin'], list(self.db[self.output_collection_name].find({}, {"_id": 0, "product_asin": 1}))))
            # urls = {}
            # spider.urls = []
            for prod in input_prods:
                if prod['product_asin'] not in present_prods:
                    spider.urls.append(prod['product_url'])
                    # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote(prod['product_url'].encode('utf-8'))))
        else:
            spider.urls = spider.failed_urls.copy()
            spider.failed_urls.clear()

        print("******\n", spider.urls)
        
        print("*******\nProduct Info Pipeline Started\n********")

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
                if (
                    item["product_details"] != {}
                    and item["product_asin"] != "NA"
                ):
                    # print(item)
                    spider.success_counts['added'] += 1
                    self.db[self.output_collection_name].insert_one(ItemAdapter(item).asdict())
        
        return item

class AmazonProductDailyMovementToMongoPipeline:
    
    input_collection_name = "product_list"
    output_collection_name = "product_data"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            input_prods = list(self.db[self.input_collection_name].find({}, {"_id": 0, "product_asin": 0}))
            # spider.urls = []
            for prod in input_prods:
                spider.urls.append(prod['product_url'])
                # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote(prod['product_url'].encode('utf-8'))))
        else:
            spider.urls = spider.failed_urls.copy()
            spider.failed_urls.clear()

        # print("******\n", spider.urls)
        
        print("*******\nProduct Daily Movement Pipeline Started\n********")

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

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        # self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_crawler(cls, crawler):
        """
        A class method used to pull in information from settings.py.
        """

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        """
        This class method is called when initializing spider and opening MongoDB connection.

        Parameters
        ----------
        spider : object
            the spider which was opened
        """

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.cold_run:
            for keyword in spider.keywords:
                for page in range(spider.pages):
                    # TODO add correct format
                    # spider.urls.append("https://www.amazon.in/s?k={}&page={}".format('+'.join(keyword.split()), page+1))
                    spider.urls.append("https://www.amazon.in/s?k={}&page={}".format(quote(keyword).replace("%20", "+"), page+1))
                    # spider.urls.append("http://api.proxiesapi.com/?auth_key={}&url={}".format("b433886e7d6c73d3c24eeb0d9244f5c6_sr98766_ooPq87", quote("https://www.amazon.in/s?k={}&page={}".format('+'.join(keyword.split()), page+1).encode('utf-8'))))
        else:
            spider.urls = spider.failed_urls.copy()
            spider.failed_urls.clear()

        # print(spider.urls)
        print("********\nShare of Search Pipeline Started\n********")

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
                # for product in item['products']:
                    # existing_item = self.db[self.collection_name].find_one(
                    #     {"product_asin": product["product_asin"]}
                    # )
                    # print("*****\nITEM:", item)
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
                                    "product_fullfilled": item["product_fullfilled"]
                                }
                            }
                        },
                        upsert=True
                    )
        return item
