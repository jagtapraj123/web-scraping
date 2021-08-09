# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonProductScrapingItem(scrapy.Item):
    """
    A class used to define the fields for the item.
    """

    product_name = scrapy.Field()
    product_brand = scrapy.Field()
    product_sale_price = scrapy.Field()
    product_offers = scrapy.Field()
    product_original_price = scrapy.Field()
    product_fullfilled = scrapy.Field()
    product_rating = scrapy.Field()
    product_total_reviews = scrapy.Field()
    product_availability = scrapy.Field()
    product_category = scrapy.Field()
    product_icons = scrapy.Field()
    product_best_seller_rank = scrapy.Field()
    product_details = scrapy.Field()
    product_asin = scrapy.Field()
    product_important_information = scrapy.Field()
    product_description = scrapy.Field()
    product_bought_together = scrapy.Field()
    product_subscription_discount = scrapy.Field()
    product_variations = scrapy.Field()
    links = scrapy.Field()
    asin = scrapy.Field()
    bsr = scrapy.Field()
