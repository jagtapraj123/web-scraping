from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')


collec = client['amazon_marketplace_scraping_havells']['product_list']

asins = [
    'B01N3TH1Q3', 'B01LHAZMLS', 'B00QLX3UZC', 'B09G6SFFSV', 'B078GSXY26', 'B0828WX669', 'B07HW3YZGW', 'B07H5CWR2B', 'B08P23YS34', 'B09MTT2WS7', 'B07Y919DML', 'B09MTP9SGP', 'B07YY6LH8C', 'B098L6HG12', 'B0864DNLCP', 'B09DM7YH79', 'B09BWN47S1', 'B01N3PB0E6', 'B09MTQQ8D7', 'B07YCY8D69', 'B09DMC1DS2', 'B098L55BXG', 'B08BRZ2M4Q', 'B00FWK50GC', 'B01J5JQ6F4', 'B07HQ75QQM', 'B01MY9XTEO', 'B07HM33Y8S', 'B072HCVMMY', 'B07YCYTNCB', 'B07HMBDKCH', 'B00TTULINA', 'B00TTUAQDS', 'B00TTUPQ38', 'B00TTTTYVO', 'B07Y91TPGK', 'B071J3YJ73', 'B07YCXRZWM',
    'B00RGPO1LG', 'B0986W69TG', 'B07JM1PJ3H', 'B085MMXTWN', 'B07TXTCFB5', 'B099FB78WM', 'B075SBM51N', 'B07DG1357W', 'B075SCBTGW', 'B07WRCRFBN', 'B08RBN7CYS', 'B08BXG8RZJ', 'B08RBPW7CX', 'B08RBND41W', 'B098L3P618', 'B084XK36CJ', 'B01ID50B1Q', 'B098L475JF', 'B084XJTRVG', 'B083F8HSQD', 'B084XJX1RY', 'B084XJX1QW', 'B078K5CBX7', 'B07HCQYSB6', 'B07VJGTGL7', 'B0183I7K1W', 'B08BXH1QNL', 'B019VXS86E', 'B09375WW7R', 'B00VT8CUHS', 'B084XK2NHG', 'B084XJTKQD', 'B08SX6H41Z', 'B08BXFZ4M7', 'B01NBDSYIX', 'B00VT8D5OK', 'B093798DWM', 'B01M1RGCNV', 'B097RRMTKS', 'B084XK2994', 'B07JLBFYX7', 'B07VLZ7HKP', 'B07WTHPDKY', 'B00RGPNOEQ', 'B085MN1V6P',
]

products = []
for asin in asins:
    products.append({'product_asin': asin, 'product_url': 'https://www.amazon.in/dp/{}'.format(asin)})

present = 0
added = 0

for product in products:
    existing_item = collec.find_one(
        {"product_asin": product["product_asin"]}
    )
    if existing_item is None:
        added += 1
    else:
        present += 1
    collec.find_one_and_update(
        {"product_asin": product['product_asin']},
        {
            "$set": {
                "product_url": product['product_url'],
            }
        },
        upsert=True
    )
    client_added = collec.find_one(
        {"product_asin": product["product_asin"], "clients": "Havells"}
    )
    if not client_added:
        collec.find_one_and_update(
        {"product_asin": product['product_asin']},
        {
            "$push": {
                "clients": "Havells",
            }
        }
    )

print(present, added)