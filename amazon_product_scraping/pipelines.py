# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo
from itemadapter import ItemAdapter
from datetime import datetime
from pymongo import ReturnDocument


class MongoDBPipeline:
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

    collection_name = "product_data"

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

        if spider.name == "AmazonProductSpider":
            existing_item = self.db[self.collection_name].find_one(
                {"product_asin": item["product_asin"]}
            )
            if (
                existing_item
                and item["product_details"] != {}
                and item["product_asin"] != "NA"
            ):
                # self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
                self.db[self.collection_name].find_one_and_update(
                    {"product_asin": item["product_asin"]},
                    {
                        "$set": {
                            "product_name": item["product_name"],
                            "product_brand": item["product_brand"],
                            "product_offers": item["product_offers"],
                            "product_original_price": item["product_original_price"],
                            "product_fullfilled": item["product_fullfilled"],
                            "product_rating": item["product_rating"],
                            "product_total_reviews": item["product_total_reviews"],
                            "product_availability": item["product_availability"],
                            "product_category": item["product_category"],
                            "product_icons": item["product_icons"],
                            "product_details": item["product_details"],
                            "product_important_information": item["product_important_information"],
                            "product_description": item["product_description"],
                            "product_bought_together": item["product_bought_together"],
                            "product_subscription_discount": item["product_subscription_discount"],
                            "product_variations": item["product_variations"]
                        }
                    },
                    upsert=True,
                )
            return item

        if spider.name == "AmazonProductSalePriceBSRSpider":
            existing_item = self.db[self.collection_name].find_one(
                {"product_asin": item["product_asin"]}
            )
            if (
                existing_item
                and item["product_details"] != {}
                and item["product_asin"] != "NA"
            ):
                self.db[self.collection_name].find_one_and_update(
                    {"product_asin": item["product_asin"]},
                    {
                        "$push": {
                            "product_sale_price": item["product_sale_price"][0],
                            "product_best_seller_rank": item[
                                "product_best_seller_rank"
                            ][0],
                        }
                    },
                    upsert=True,
                )
            return item

        if spider.name == "AmazonProductBSRSpider":
            for i, j in zip(item["asin"], item["bsr"]):
                existing_item = self.db[self.collection_name].find_one(
                    {"product_asin": i}
                )
                if existing_item:
                    now = datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    best_seller_rank = {}
                    best_seller_rank["time"] = current_time
                    best_seller_rank["value"] = j
                    self.db[self.collection_name].find_one_and_update(
                        {"product_asin": i},
                        {
                            "$push": {
                                "product_best_seller_rank": best_seller_rank,
                            }
                        },
                        upsert=True,
                    )

            return item
