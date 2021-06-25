# web-scraping
## What is Scrapy?
Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.
## How to install requirement libraries?
The `requirements.txt` file has list of all Python libraries which are required for a scrapy project, and they will be installed using the following command:<br/>
> `pip install -r requirements.txt` 
## How to create a new scrapy project?
Enter a directory where you’d like to store your code and run:
> `scrapy startproject amazon_product_scraping`

This will create a directory with the name of amazon_product_scraping in the same directory with the following contents:
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
* **items.py:** Items are containers that will be loaded with the scraped data; they work like simple Python dicts. They are declared by creating a **scrapy.Item** class and defining its attributes as **scrapy.Field** objects.
* **pipelines.py:** After an item has been scraped by a spider, it is sent to the Item Pipeline which processes it through several components that are executed sequentially. Each item pipeline component is a Python class that has to implement a method called **process_item** to process scraped items. It receives an item and performs an action on it, also decides if the item should continue through the pipeline or should be dropped and not processed any longer. If it wants to drop an item then it raises **DropItem** exception to drop it.
* **settings.py:** It allows one to customize the behavior of all Scrapy components, including the core, extensions, pipelines, and spiders themselves. It provides a global namespace of key-value mappings that the code can use to pull configuration values from.
* **spiders:**  Spiders is a directory which contains all **spiders** as Python classes. Whenever one runs any spider then scrapy looks into this directory and tries to find the spider with its name provided by the user. Spiders define how a certain site or a group of sites will be scraped, including how to perform the crawl and how to extract data from their pages. 

Spiders have to define three major attributes i.e start_urls which tells which URLs are to be scrapped, allowed_domains which defines only those domain names which need to scrape and parse is a method which is called when any response comes from lodged requests. These attributes are important because these constitute the base of Spider definitions.
