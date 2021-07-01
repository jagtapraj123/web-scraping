# web-scraping
## What is Scrapy?
Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.
## How to install requirement libraries?
The `requirements.txt` file has list of all Python libraries which are required for a scrapy project, and they will be installed using the following command:<br/>
> `pip install -r requirements.txt` 
## How to create a new scrapy project?
Enter a directory where you’d like to store your code and run:
> `scrapy startproject amazon_product_scraping`

Where **amazon_product_scraping** is the scrapy project name. This will create a directory with the name of amazon_product_scraping in the same directory with the following contents:
```
amazon_product_scraping/
    scrapy.cfg
    amazon_product_scraping/
        __init__.py
        itmes.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
```
The project structure which scrapy creates for a user has,
* **scrapy.cfg:** It is a project configuration file which contains information for setting module for the project along with its deployment information.
* **amazon_product_scraping:** It is an application directory with many different files that are actually responsible for running and scraping data from web URLs.
* **items.py:** Includes container that will be loaded along with scraped data.
* **middlewares.py:** It contains Spider’s processing mechanism to handle requests and responses.
* **pipelines.py:** It contains a set of Python classes to process scraped data further.
* **settings.py:** Any customized settings can be added to this file.
* **spiders:**  This directory contains all the spiders in the form of a python class. Whenever Scrapy is requested to run, it will be searched in this folder.
## How to create a spider?
Now to create spider, we have two different options.

1) We can create a simple Python class in the spiders directory and import essential modules to it.

2) We can use the default utility which is provided by the scrapy framework itself.

If you want to use the default utility called genspider to create spider in the framework. It will automatically create a class with a default template in the spiders directory. In order to create a spider, we can use the command below.
> scrapy genspider AmazonProductSpider amazon.in

Where **AmazonProductSpider** is the spider name and **amazon.in** is the URL of the site or domain that we are going to scrape data from. We will extract product data for shampoo category from amazon.in. 

The python file `AmazonProductSpider.py` will save under the **amazon_product_scraping/spiders** directory in your project. 

In the created **AmazonProductSpider**, we need to define its name and **allowed_domains** & **start_urls** are created based on the link we provided when we created the spider.
The logic for extracting our data have written in the different functions. We also need to implement a parse method. In the parse method, an item object is defined and is filled with required information.
## How to run spider?
Before running the spider we need to add **ITEM_PIPELINES = {"amazon_product_scraping.pipelines.AmazonProductScrapingPipeline": 300,}** in the python file `settings.py`.

Go to the project's directory and run the following command:
> scrapy crawl AmazonProductSpider

This command runs the spider with name **AmazonProductSpider**.
