# web-scraping
## requirements.txt
The `requirements.txt` file has list of all Python libraries which are required for a scrapy project, and they will be installed using the following command:<br/>
> `pip install -r requirements.txt` 
## Create a Scrapy Project
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
## Create a Spider
Now to create spider, we have two different options.

1) We can create a simple Python class in the spiders directory and import essential modules to it.

2) We can use the default utility which is provided by the scrapy framework itself.

If you want to use the default utility called genspider to create spider in the framework. It will automatically create a class with a default template in the spiders directory. In order to create a spider, we can use the command below.
> `scrapy genspider AmazonProductSpider amazon.in`

Where **AmazonProductSpider** is the spider name and **amazon.in** is the URL of the site or domain that we are going to scrape data from. We will extract product data for shampoo category from amazon.in. 

The python file `AmazonProductSpider.py` will save under the **amazon_product_scraping/spiders** directory in your project. 

In the created **AmazonProductSpider**, we need to define its name and **allowed_domains** & **start_urls** are created based on the link we provided when we created the spider. We also need to implement a parse method. In the parse method, an item object is defined and is filled with required information.
## data
The `amazon_product_scraping/data` folder have two folders `InputData` and `OutputData`. The folder `InputData` have two csv files `amazon_product_data.csv` and `recurrent_saleprice_bsr.csv`. The csv file `amazon_product_data.csv` has a column `URL` with new URLs of amazon product and the csv file `recurrent_saleprice_bsr.csv` has a column `URL` with old URLs of amazon product. The folder `OutputData` has a json file which have data of amazon product.
## configuration_file
The `amazon_product_scraping/configuration_file` folder has a file `config.json`. This file have two relative path of both csv files in the `amazon_product_scraping/data/InputData` folder.
## utils
The `amazon_product_scraping/utils` folder have two python files `AmazonScrapingHelper.py` and `FileHelper.py`. The python file `AmazonScrapingHelper.py` has a class with different functions. The logic for extracting the product data from `amazon.in` have written in these different functions, for example: product title, product brand, product sale price etc. The python file `FileHelper.py` has a class with a function. This function read a csv file which has a column `URL` with URLs of amazon product and return a list of these URLs.
## spiders
The `amazon_product_scraping/spiders` folder have two spiders `AmazonProductSpider.py` and `AmazonProductSalePriceBSRSpider.py`. The spider `AmazonProductSpider.py` extract all data of amazon product like product title, product brand, product sale price etc. and the spider `AmazonProductSalePriceBSRSpider.py` extract only product sale price, product best seller rank, product asin with using of the class of python file `amazon_product_scraping/utils/AmazonScrapingHelper.py`. 
## Run a Spider in the terminal
Before running the spider we need to add **ITEM_PIPELINES = {"amazon_product_scraping.pipelines.AmazonProductScrapingPipeline": 300,}** in the python file `settings.py`.

Go to the project's directory and run the following command:
> `scrapy crawl amazon_product_data`

This command runs the spider with name **amazon_product_data**.
## Installation of Scrapyd
To install `scrapyd` using the following command:
> `pip install scrapyd`

after installing to start `scrapyd` using the following command:
> `scrapyd`
## Deploying a project
### Scrapyd-client
Open an another terminal and install `scrapyd-client` using the following command:
> `pip install git+https://github.com/scrapy/scrapyd-client.git`
### Deploy
To deploy the project using the following command:
> scrapyd-deploy default
### List of Spiders
To get list of spiders using the following command:
> `curl http://localhost:6800/listspiders.json?project=amazon_product_scraping`
### Run a Spider in the Scrapyd
To run a spider using the following command:
> `curl http://localhost:6800/schedule.json -d project=amazon_product_scraping -d spider=amazon_product_data`
