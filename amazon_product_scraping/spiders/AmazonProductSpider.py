import scrapy
import re
import json
from amazon_product_scraping.items import AmazonProductScrapingItem
from datetime import datetime
from amazon_product_scraping.utils.AmazonScrapingHelper import AmazonScrapingHelper
from amazon_product_scraping.utils.FileHelper import FileHelper


class AmazonProductSpider(scrapy.Spider):

    handle_httpstatus_all = True
    name = "AmazonProductSpider"
    rotate_user_agent = True
    allowed_domains = ["amazon.in"]
    with open("amazon_product_scraping/configuration_file/config.json") as file:
    	input_data = json.load(file)
    start_urls = FileHelper.get_urls(input_data['product_data']['new_data_file_path'])
    # print(len(start_urls))
    # start_urls = ['http://amazon.in/dp/B08T2Y2Q4T', 'http://amazon.in/dp/B008KH5U28', 'http://amazon.in/dp/B006LXAG4K', 'http://amazon.in/dp/B00IF3W4DK']
    
    def parse(self, response):
        helper = AmazonScrapingHelper()
        items = AmazonProductScrapingItem()
        title = helper.get_title(response)
        brand = helper.get_brand(response)
        sale_price = helper.get_sale_price(response)
        offers = helper.get_offers(response)
        original_price = helper.get_original_price(response)
        fullfilled = helper.get_fullfilled(response)
        rating = helper.get_rating(response)
        total_reviews = helper.get_total_reviews(response)
        availability = helper.get_availability(response)
        category = helper.get_category(response)
        icons = helper.get_icons(response)
        best_seller_rank = helper.get_best_seller_rank(response)
        product_details = helper.get_product_details(response)
        asin = helper.get_asin(response)
        important_information = helper.get_important_information(response)
        product_description = helper.get_product_description(response)
        bought_together = helper.get_bought_together(response)
        subscription_discount = helper.get_subscription_discount(response)
        variations = helper.get_variations(response)

        items["product_name"] = title
        items["product_brand"] = brand
        items["product_sale_price"] = sale_price
        items["product_offers"] = offers
        items["product_original_price"] = original_price
        items["product_fullfilled"] = fullfilled
        items["product_rating"] = rating
        items["product_total_reviews"] = total_reviews
        items["product_availability"] = availability
        items["product_category"] = category
        items["product_icons"] = icons
        items["product_best_seller_rank"] = best_seller_rank
        items["product_details"] = product_details
        items["product_asin"] = asin
        items["product_important_information"] = important_information
        items["product_description"] = product_description
        items["product_bought_together"] = bought_together
        items["product_subscription_discount"] = subscription_discount
        items["product_variations"] = variations
        yield items
