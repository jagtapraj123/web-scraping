# web-scraping
## What is Scrapy?
Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.
## How to install requirement libraries?
The `requirements.txt` file has list of all Python libraries which are required for scrapy project, and they will be installed using the following command:<br/>
> `pip install -r requirements.txt` 
## How to create a new scrapy project?
Enter a directory where you’d like to store your code and run:
> `scrapy startproject amazon_product_scraping`
This will create a directory with the name of amazon_product_scraping in the same directory with following contents:
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
