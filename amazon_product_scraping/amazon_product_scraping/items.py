# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonProductScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_brand = scrapy.Field()
    product_sale_price = scrapy.Field()
    product_offers_count = scrapy.Field()
    product_original_price = scrapy.Field()
    product_fullfilled = scrapy.Field()
    product_rating = scrapy.Field()
    product_total_reviews = scrapy.Field() 
    product_availability = scrapy.Field() 
    product_category = scrapy.Field()
    #product_icon_list = scrapy.Field()
    product_details = scrapy.Field()
    product_important_information = scrapy.Field()
    product_subscription_discount = scrapy.Field()
    #product_asin = scrapy.Field()
    #product_seller_rank = scrapy.Field()
