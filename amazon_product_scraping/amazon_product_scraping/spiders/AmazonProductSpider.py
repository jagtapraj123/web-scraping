import scrapy
from amazon_product_scraping.amazon_product_scraping.items import AmazonProductScrapingItem

class AmazonProductSpider(scrapy.Spider):
    name = 'AmazonProductSpider'
    allowed_domains = ['amazon.in']
    start_urls = ['http://amazon.in/dp/B00CQ41JE4']

    def parse(self, response):
        items = AmazonProductScrapingItem()
        title = response.xpath('//h1[@id="title"]/span/text()').extract_first()
        #asin = response.xpath('//span[@class="a-text-bold"]/text()="ASIN &rlm; : &lrm;"//span').extract() or "NA"
        #asin = response.xpath('//*[text()="ASIN &rlm; : &lrm;"]/parent::*//text()[not(parent::style)]').extract()
        #asin = response.meta['asin']
        brand = response.xpath('//td[@class="a-span9"]//span[@class="a-size-base"]/text()').extract_first() or "NA"
        sale_price = response.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()').extract() or "NA"
        #sale_price = response.xpath('//span[contains(@id,"priceblock_ourprice") or contains(@id,"priceblock_dealprice")]/text()').extract() or "NA"
        offers = response.xpath('//span[@class="saving-prompt"]/text()').extract() or "NA"
        original_price = response.xpath('//span[@class="priceBlockStrikePriceString a-text-strike"]/text()').extract() or "NA"
        fullfilled = response.xpath('//span[@class="a-icon-text-fba"]/text()').extract_first() or "NA"
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first() or "NA"
        total_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first() or "NA"
        availability = response.xpath('//div[@id="availability"]//text()').extract() or "NA"
        category = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
        #icons = response.xpath('//div[@class="a-row icon-farm-wrapper"]/text()').extract_first()
        details = response.xpath('//div[@id="detailBullets_feature_div"]//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]/text()').extract()
        #product_details = response.xpath('//div[@id="detailBullets_feature_div"]//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]/text()').getall()
        #details = []
        #for i in product_details:
        #    details.append(i.strip())
        #product_details = response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tr/*/text()').re('(\w+[^\n]+)')
        important_information = response.xpath('//div[@id="important-information"]//div[@class="a-section content"]//p/text()').extract() or "NA"
        subscription_discount = response.xpath('//tr[@id="regularprice_savings"]//td[@class="a-span12 a-color-price a-size-base priceBlockSavingsString"]/text()').extract_first() or "NA"
        #seller_rank = response.xpath('//*[text()="Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        items['product_name'] = ''.join(title).strip()
        #items['product_asin'] = asin
        items['product_brand'] = brand
        items['product_sale_price'] = [''.join(sale_price).strip()]
        items['product_offers_count'] = ''.join(offers).strip()[5]
        items['product_original_price'] = ''.join(original_price).strip()
        items['product_fullfilled'] = fullfilled
        items['product_rating'] = rating
        items['product_total_reviews'] = total_reviews
        items['product_availability'] = ''.join(availability).strip()
        items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
        #items['product_icon_list'] = ''.join(icons).strip()
        items['product_details'] = details
        items['product_important_information'] = important_information
        items['product_subscription_discount'] = subscription_discount.strip()[9:12]
        #items['product_seller_rank] = seller_rank
        yield items
