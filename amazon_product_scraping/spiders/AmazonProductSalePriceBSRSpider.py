import scrapy
import re
import json
from amazon_product_scraping.items import AmazonProductScrapingItem
from datetime import datetime
from amazon_product_scraping.utils.AmazonScrapingHelper import AmazonScrapingHelper
from amazon_product_scraping.utils.FileHelper import FileHelper

class AmazonProductSalePriceBSRSpider(scrapy.Spider):
    handle_httpstatus_all = True
    name = "AmazonProductSalePriceBSRSpider"
    rotate_user_agent = True
    allowed_domains = ["amazon.in"]
    with open("amazon_product_scraping/configuration_file/config.json") as file:
    	input_data = json.load(file)
    start_urls = FileHelper.get_urls(input_data['product_data']['old_data_file_path'])
    # start_urls = ['http://amazon.in/dp/B08T3325CD', 'http://amazon.in/dp/B08CSHBPD5', 'http://amazon.in/dp/B08T2Y2Q4T']
    
    def parse(self, response):
        items = AmazonProductScrapingItem()
        helper = AmazonScrapingHelper()

        title = helper.get_title(response)
        sale_price = helper.get_sale_price(response)
        original_price = helper.get_original_price(response)
        best_seller_rank = helper.get_best_seller_rank(response)
        asin = helper.get_asin(response)
        subscription_discount = helper.get_subscription_discount(response)

        items["product_name"] = title
        items["product_sale_price"] = sale_price
        items["product_original_price"] = original_price
        items["product_best_seller_rank"] = best_seller_rank
        items["product_asin"] = asin
        items["product_subscription_discount"] = subscription_discount

        yield items
