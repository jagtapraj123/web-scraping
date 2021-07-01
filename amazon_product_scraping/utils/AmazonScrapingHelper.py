from datetime import datetime
import scrapy
import re


class AmazonScrapingHelper:
    def get_title(self, response):
        title_xpath_text = response.xpath(
            '//h1[@id="title"]//span/text()'
        ).extract_first()
        title = "".join(title_xpath_text).strip()
        return title

    def get_brand(self, response):
        brand = (
            response.xpath(
                '//td[@class="a-span9"]//span[@class="a-size-base"]/text()'
            ).extract_first()
            or "NA"
        )
        return brand

    def get_sale_price(self, response):
        sale_price_xpath_text = (
            response.xpath(
                '//span[contains(@id,"priceblock_dealprice") or contains(@id,"priceblock_ourprice")]/text()'
            ).extract()
            or "NA"
        )
        sale_price_strip = (
            ("".join(sale_price_xpath_text).strip())
            .replace("\xa0", "")
            .replace("\u20b9", "")
        )
        sale_price = []
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        sale_price_dict = {}
        sale_price_dict["time"] = current_time
        sale_price_dict["value"] = sale_price_strip
        sale_price.append(sale_price_dict)
        return sale_price

    def get_offers(self, response):
        offers_xpath_text = response.xpath(
            '//span[@class="saving-prompt"]/text()'
        ).extract()
        if offers_xpath_text:
            offers_strip = "".join(offers_xpath_text).strip()
            offers = str(int(re.search(r"\d+", offers_strip).group()))
            return offers
        else:
            return "NA"

    def get_original_price(self, response):
        original_price_xpath_text = (
            response.xpath(
                '//span[@class="priceBlockStrikePriceString a-text-strike"]/text()'
            ).extract()
            or "NA"
        )
        original_price = (
            ("".join(original_price_xpath_text).strip())
            .replace("\xa0", "")
            .replace("\u20b9", "")
        )
        return original_price

    def get_fullfilled(self, response):
        if response.xpath('//span[@class="a-icon-text-fba"]/text()').extract_first():
            fullfilled = response.xpath(
                '//span[@class="a-icon-text-fba"]/text()'
            ).extract_first()
            return fullfilled
        elif (
            "Fulfilled by Amazon"
            in response.xpath('//div[@id="merchant-info"]//a/text()').extract()
        ):
            return "Fulfilled"
        elif (
            "fulfilled"
            in response.xpath('//div[@id="merchant-info"]/text()').extract_first()
        ):
            return "Fulfilled"
        else:
            return "NA"

    def get_rating(self, response):
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first() or "NA"
        return rating

    def get_total_reviews(self, response):
        total_reviews = (
            response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
            or "NA"
        )
        return total_reviews

    def get_availability(self, response):
        availability_xpath_text = (
            response.xpath('//div[@id="availability"]//text()').extract() or "NA"
        )
        availability = (
            ("".join(availability_xpath_text).strip()).replace("\n", "")
        ).split(".")[0]
        return availability

    def get_category(self, response):
        category_xpath_text = response.xpath(
            '//a[@class="a-link-normal a-color-tertiary"]/text()'
        ).extract()
        category = [i.strip() for i in category_xpath_text]
        return category

    def get_icons(self, response):
        icons_xpath_text = response.xpath(
            '//a[@class="a-size-small a-link-normal a-text-normal"]/text()'
        ).extract()
        icons = []
        for i in icons_xpath_text:
            icons.append(i.strip())
        return icons

    def get_best_seller_rank(self, response):
        product_details_xpath_text = response.xpath(
            '//div[@id="detailBullets_feature_div"]//span/text()'
        ).getall()
        if product_details_xpath_text:
            product_details_strip = [
                i.strip().replace("\n", "") for i in product_details_xpath_text
            ]
            product_details = [
                i.replace("\u200f", "").replace("\u200e", "")
                for i in product_details_strip
                if i != ""
            ]
            if "Best Sellers Rank:" in product_details:
                seller_rank_1_xpath_text = response.xpath(
                    '//div[@id="detailBullets_feature_div"]//span[@class="a-list-item"]/text()'
                ).getall()
                seller_rank_2_xpath_text = response.xpath(
                    '//div[@id="detailBullets_feature_div"]//span[@class="a-list-item"]//a/text()'
                ).getall()
                seller_rank_1_strip = [
                    i.strip().replace("\n", "").replace("(", "").replace(")", "")
                    for i in seller_rank_1_xpath_text
                ]
                seller_rank_1 = [i for i in seller_rank_1_strip if i != ""]
                seller_rank_2_strip = [
                    i.strip().replace("\n", "") for i in seller_rank_2_xpath_text
                ]
                seller_rank_2 = [i for i in seller_rank_2_strip if i != ""]
                first_element_seller_rank = ["(", seller_rank_2[0], ")"]
                seller_rank_2[0] = "".join(first_element_seller_rank)
                seller_rank_list = []
                for i, j in zip(seller_rank_1, seller_rank_2):
                    seller_rank_list.append(i)
                    seller_rank_list.append(j)
                seller_rank = " ".join(seller_rank_list)
                best_seller_rank = []
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                best_seller_rank_dict = {}
                best_seller_rank_dict["time"] = current_time
                best_seller_rank_dict["value"] = seller_rank
                best_seller_rank.append(best_seller_rank_dict)
                return best_seller_rank
            else:
                seller_rank = "NA"
                best_seller_rank = []
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                best_seller_rank_dict = {}
                best_seller_rank_dict["time"] = current_time
                best_seller_rank_dict["value"] = seller_rank
                best_seller_rank.append(best_seller_rank_dict)
                return best_seller_rank
        else:
            seller_rank = "NA"
            best_seller_rank = []
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            best_seller_rank_dict = {}
            best_seller_rank_dict["time"] = current_time
            best_seller_rank_dict["value"] = seller_rank
            best_seller_rank.append(best_seller_rank_dict)
            return best_seller_rank

    def get_product_details(self, response):
        product_details_xpath_text = response.xpath(
            '//div[@id="detailBullets_feature_div"]//span/text()'
        ).getall()
        if product_details_xpath_text:
            product_details_strip = [
                i.strip().replace("\n", "") for i in product_details_xpath_text
            ]
            product_details = [
                i.replace("\u200f", "").replace("\u200e", "")
                for i in product_details_strip
                if i != ""
            ]
            if "Best Sellers Rank:" in product_details:
                index_best_seller_rank = product_details.index("Best Sellers Rank:")
                product_details = product_details[0:index_best_seller_rank]
            else:
                if "Customer Reviews:" in product_details:
                    index_best_seller_rank = product_details.index("Customer Reviews:")
                    product_details = product_details[0:index_best_seller_rank]
            details = {}
            i = 0
            while i < len(product_details):
                details[product_details[i].replace(":", "")] = product_details[i + 1]
                i += 2
            if self.get_best_seller_rank(response)[0]["value"] != "NA":
                details["Best Sellers Rank"] = self.get_best_seller_rank(response)[0][
                    "value"
                ]
            if (
                self.get_rating(response) != "NA"
                and self.get_total_reviews(response) != "NA"
            ):
                details["Customer Reviews"] = " ".join(
                    [self.get_rating(response), self.get_total_reviews(response)]
                )
            return details
        return {}

    def get_asin(self, response):
        asin = response.xpath("//*[@data-asin]").xpath("@data-asin").extract_first()
        return asin

    def get_important_information(self, response):
        important_information_xpath_text = (
            response.xpath(
                '//div[@id="important-information"]//div[@class="a-section content"]//p/text()'
            ).extract()
            or "NA"
        )
        important_information = "".join(important_information_xpath_text)
        return important_information

    def get_product_description(self, response):
        product_description_xpath_text = (
            response.xpath('//div[@id="productDescription"]//p/text()').extract()
            or "NA"
        )
        product_description = "".join(product_description_xpath_text).strip()
        return product_description

    def get_bought_together(self, response):
        bought_together_xpath_text = response.xpath(
            '//div[@aria-hidden="true"]/text()'
        ).extract()
        bought_together_strip = [
            i.strip().replace("\n", "") for i in bought_together_xpath_text
        ]
        bought_together = [i for i in bought_together_strip if i != ""]
        return bought_together

    def get_subscription_discount(self, response):
        subscription_discount_xpath_text = response.xpath(
            '//tr[contains(@id,"regularprice_savings") or contains(@id,"dealprice_savings")]//td[@class="a-span12 a-color-price a-size-base priceBlockSavingsString"]/text()'
        ).extract_first()
        if subscription_discount_xpath_text:
            if len((subscription_discount_xpath_text.strip()).split("(")) != 1:
                subscription_discount = (
                    (subscription_discount_xpath_text.strip()).split("(")[1]
                ).split(")")[0]
                return subscription_discount
        return "NA"

    def get_variations(self, response):
        variations = (
            response.xpath(
                '//div[@id="variation_pattern_name"]//img[@class="imgSwatch"]'
            )
            .xpath("@alt")
            .getall()
        )
        return variations
