import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient()
DB = client["amazon_product_data"]
collection = DB["product_data"]
url = "http://www.amazon.in"
HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'})

webpage = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")

for element in soup.find_all(['a','link']):
    link = element.get('href')
    db.collection.insertOne({'link':link})
    print(link)