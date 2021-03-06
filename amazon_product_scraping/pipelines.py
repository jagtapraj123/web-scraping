# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo
from itemadapter import ItemAdapter


class MongoDBPipeline:
    collection_name = "product_data"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == "AmazonProductSpider":
            existing_item = self.db[self.collection_name].find_one(
                {"product_asin": item["product_asin"]})
            if not existing_item:
                self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
                return item
            return item

        if spider.name == "AmazonProductSalePriceBSRSpider":
            self.db[self.collection_name].find_one_and_update(
                {"product_asin": item["product_asin"]},
                {
                    "$push": {
                        "product_sale_price": item["product_sale_price"][0],
                        "product_best_seller_rank": item["product_best_seller_rank"][0],
                    }
                },
                upsert=True,
            )
            return item
