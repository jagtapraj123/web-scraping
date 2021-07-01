import scrapy
import re
from amazon_product_scraping.items import AmazonProductScrapingItem
from datetime import datetime


class AmazonProductSpider(scrapy.Spider):
    handle_httpstatus_all = True
    name = "AmazonProductSpider"
    rotate_user_agent = True
    allowed_domains = ["amazon.in"]
    # start_urls = ['http://amazon.in/dp/B08T3325CD', 'http://amazon.in/dp/B08CSHBPD5', 'http://amazon.in/dp/B08T2Y2Q4T', 'http://amazon.in/dp/B008KH5U28', 'http://amazon.in/dp/B006LXAG4K', 'http://amazon.in/dp/B00IF3W4DK', 'http://amazon.in/dp/B074VG8ZH8', 'http://amazon.in/dp/B08HJC7GXS', 'http://amazon.in/dp/B08HH3YLGZ', 'http://amazon.in/dp/B08K3HQ4M4', 'http://amazon.in/dp/B004R6HWB8', 'http://amazon.in/dp/B01N1KE7D5', 'http://amazon.in/dp/B07MNZTKBS', 'http://amazon.in/dp/B01KC4BWN2', 'http://amazon.in/dp/B08QV7QXF2', 'http://amazon.in/dp/B08QTQZZFH', 'http://amazon.in/dp/B01HBA74PU', 'http://amazon.in/dp/B01IOPY3G4', 'http://amazon.in/dp/B01M3PPPBU', 'http://amazon.in/dp/B08LGZM288', 'http://amazon.in/dp/B07QXTBSMQ', 'http://amazon.in/dp/B07BMZD88Q', 'http://amazon.in/dp/B01M0OX5NU', 'http://amazon.in/dp/B00L322HT6', 'http://amazon.in/dp/B08QV4BHK4', 'http://amazon.in/dp/B07FLB3Z66', 'http://amazon.in/dp/B07MRHZQVB', 'http://amazon.in/dp/B08LGZWBPT', 'http://amazon.in/dp/B08K3GSYTY', 'http://amazon.in/dp/B08LH1MD56', 'http://amazon.in/dp/B077PT2S31', 'http://amazon.in/dp/B01M6BLCES', 'http://amazon.in/dp/B08LGQ582N', 'http://amazon.in/dp/B08LGZSXGH', 'http://amazon.in/dp/B004XADCA8', 'http://amazon.in/dp/B001RYOOUK', 'http://amazon.in/dp/B01MG81SLM', 'http://amazon.in/dp/B08LH19Y3Y', 'http://amazon.in/dp/B086XP97N8', 'http://amazon.in/dp/B0854B9FPK', 'http://amazon.in/dp/B08PDB8CMT', 'http://amazon.in/dp/B01M1O4JAA', 'http://amazon.in/dp/B00YBTAOPM', 'http://amazon.in/dp/B08LGYCF36', 'http://amazon.in/dp/B073JMX9X6', 'http://amazon.in/dp/B001P1ZC9M', 'http://amazon.in/dp/B000UULQMQ', 'http://amazon.in/dp/B08J3T8TY1', 'http://amazon.in/dp/B01M01MNXI', 'http://amazon.in/dp/B06Y3QZ895', 'http://amazon.in/dp/B00144PBQE', 'http://amazon.in/dp/B00AREI3S0', 'http://amazon.in/dp/B073JPPRXS', 'http://amazon.in/dp/B01LX41KJW', 'http://amazon.in/dp/B0046HBPV6', 'http://amazon.in/dp/B00923XTFY', 'http://amazon.in/dp/B001P1ZELS', 'http://amazon.in/dp/B00N1T66U0', 'http://amazon.in/dp/B01N45HDW8', 'http://amazon.in/dp/B07GK1R981', 'http://amazon.in/dp/B0948B9L8H', 'http://amazon.in/dp/B006DQWRV0', 'http://amazon.in/dp/B07WX4YDRN', 'http://amazon.in/dp/B0031TSC34', 'http://amazon.in/dp/B01LX41O04', 'http://amazon.in/dp/B07C65Y91Y', 'http://amazon.in/dp/B073JPXMF6', 'http://amazon.in/dp/B01MG7T1P7', 'http://amazon.in/dp/B08LH1FW8F', 'http://amazon.in/dp/B07G81NF68', 'http://amazon.in/dp/B07WMWP6Z5', 'http://amazon.in/dp/B01M112TLH', 'http://amazon.in/dp/B01M0MI70A', 'http://amazon.in/dp/B07WXZ8ZZX', 'http://amazon.in/dp/B073JPVB7D', 'http://amazon.in/dp/B07VM7XZJC', 'http://amazon.in/dp/B07FCH2WX1', 'http://amazon.in/dp/B00DZHYA24', 'http://amazon.in/dp/B001TH8Y4C', 'http://amazon.in/dp/B08PD8RDRD', 'http://amazon.in/dp/B08PDB1J26', 'http://amazon.in/dp/B07J3LG4ZZ', 'http://amazon.in/dp/B001VD3L8I', 'http://amazon.in/dp/B076DC9Z6Z', 'http://amazon.in/dp/B0948992RV', 'http://amazon.in/dp/B07FNSLG9D', 'http://amazon.in/dp/B01M01MQPB', 'http://amazon.in/dp/B08LH1SL4L', 'http://amazon.in/dp/B08PD9WXK1', 'http://amazon.in/dp/B08PD9ZXSP', 'http://amazon.in/dp/B01GHKXMGU', 'http://amazon.in/dp/B08LH1FVPQ', 'http://amazon.in/dp/B076DGQYHQ', 'http://amazon.in/dp/B07FNWJ1JF', 'http://amazon.in/dp/B081BBXLKJ', 'http://amazon.in/dp/B08PDD5WKY', 'http://amazon.in/dp/B06Y69MMT4', 'http://amazon.in/dp/B015Z96HQ6', 'http://amazon.in/dp/B07P8N15VM', 'http://amazon.in/dp/B00KCKZPX0', 'http://amazon.in/dp/B08K3KNNW3', 'http://amazon.in/dp/B07P8MZ67Q', 'http://amazon.in/dp/B073JPGKLX', 'http://amazon.in/dp/B08LH36Z9Q', 'http://amazon.in/dp/B08LH1H3M7', 'http://amazon.in/dp/B08PDC3TNC', 'http://amazon.in/dp/B073JPR2TJ', 'http://amazon.in/dp/B01LY3NCGX', 'http://amazon.in/dp/B08PD6R8DX', 'http://amazon.in/dp/B08JWR5PH7', 'http://amazon.in/dp/B078M1JM3D', 'http://amazon.in/dp/B08PDB23X8', 'http://amazon.in/dp/B008UTZV70', 'http://amazon.in/dp/B08K3FJL3C', 'http://amazon.in/dp/B08JDLNVDR', 'http://amazon.in/dp/B089FS65DP', 'http://amazon.in/dp/B07DFYNW7B', 'http://amazon.in/dp/B08PD8Y4SN', 'http://amazon.in/dp/B08LH1N4TM', 'http://amazon.in/dp/B07WF1QQHF', 'http://amazon.in/dp/B07P7HMW8P', 'http://amazon.in/dp/B00KCKZSN2', 'http://amazon.in/dp/B076Y3YP9T', 'http://amazon.in/dp/B007IX0CM8', 'http://amazon.in/dp/B08PD9JN72', 'http://amazon.in/dp/B08LGRJXP6', 'http://amazon.in/dp/B08K3JLNP7', 'http://amazon.in/dp/B08LGRJYZN', 'http://amazon.in/dp/B01M0OX4L7', 'http://amazon.in/dp/B08LGPJHF2', 'http://amazon.in/dp/B07FR9NVGV', 'http://amazon.in/dp/B00SLIL9GM', 'http://amazon.in/dp/B005HIH24W', 'http://amazon.in/dp/B01A6ADLTK', 'http://amazon.in/dp/B0752FXRQJ', 'http://amazon.in/dp/B06X3SXGVF', 'http://amazon.in/dp/B0752HG1ZY', 'http://amazon.in/dp/B00HX5PYTM', 'http://amazon.in/dp/B00AREI3BC', 'http://amazon.in/dp/B000NPVDB2', 'http://amazon.in/dp/B00AREI5KG', 'http://amazon.in/dp/B08LGXB2CW', 'http://amazon.in/dp/B08PD9WXH5', 'http://amazon.in/dp/B00ID0WYHQ', 'http://amazon.in/dp/B002PBJLMU', 'http://amazon.in/dp/B00SZ7QHGG', 'http://amazon.in/dp/B00AF9DJ0Y', 'http://amazon.in/dp/B00OO18UJE', 'http://amazon.in/dp/B01MS3DF6F', 'http://amazon.in/dp/B06Y42BWNP', 'http://amazon.in/dp/B01A69YCEO', 'http://amazon.in/dp/B00EWA3X62', 'http://amazon.in/dp/B005HIH67A', 'http://amazon.in/dp/B08JWKJB9R', 'http://amazon.in/dp/B07VJNNV7D', 'http://amazon.in/dp/B07J57F3RM', 'http://amazon.in/dp/B073JNWHBT', 'http://amazon.in/dp/B08KHHJGY4', 'http://amazon.in/dp/B01N6MUC0S', 'http://amazon.in/dp/B08LH1MQ2T', 'http://amazon.in/dp/B08LH17HK8', 'http://amazon.in/dp/B08PDB3N9F', 'http://amazon.in/dp/B073BDP9VM', 'http://amazon.in/dp/B08LH2YM2G', 'http://amazon.in/dp/B08LH1V8MK', 'http://amazon.in/dp/B08LGZWDJH', 'http://amazon.in/dp/B08LGZTKCZ', 'http://amazon.in/dp/B08LH2YM3R', 'http://amazon.in/dp/B076Y229S1', 'http://amazon.in/dp/B017LTGG2S', 'http://amazon.in/dp/B07DFRLCVS', 'http://amazon.in/dp/B07DFSGXDG', 'http://amazon.in/dp/B00G9Z3HGE', 'http://amazon.in/dp/B00ENZRCBI', 'http://amazon.in/dp/B0764M9QVV', 'http://amazon.in/dp/B0764MLHRM', 'http://amazon.in/dp/B077P87ZB4', 'http://amazon.in/dp/B00ENZRLRS', 'http://amazon.in/dp/B077P1B5X4', 'http://amazon.in/dp/B08KHZH344', 'http://amazon.in/dp/B08194PS69', 'http://amazon.in/dp/B077P88293', 'http://amazon.in/dp/B01EJIEC8O', 'http://amazon.in/dp/B08KGR2MZ1', 'http://amazon.in/dp/B08KHZD46M', 'http://amazon.in/dp/B07P21CHH8', 'http://amazon.in/dp/B089DZGNN1', 'http://amazon.in/dp/B0769S19YV', 'http://amazon.in/dp/B01H7BOYNS', 'http://amazon.in/dp/B08194DMZP', 'http://amazon.in/dp/B01HBA4VMY', 'http://amazon.in/dp/B07NZW6WNN', 'http://amazon.in/dp/B077SSHGPM', 'http://amazon.in/dp/B089DZKT4W', 'http://amazon.in/dp/B081BG8LDS', 'http://amazon.in/dp/B08BXJ3WD9', 'http://amazon.in/dp/B08BXLVDF1', 'http://amazon.in/dp/B07P354C4B', 'http://amazon.in/dp/B08QV8TD41', 'http://amazon.in/dp/B07R9KVCJJ', 'http://amazon.in/dp/B012RBB148', 'http://amazon.in/dp/B01IR8NCB0', 'http://amazon.in/dp/B079VQY6VZ', 'http://amazon.in/dp/B01F6XQ9VY', 'http://amazon.in/dp/B00O0RVIJQ', 'http://amazon.in/dp/B00U5ZIYAS', 'http://amazon.in/dp/B015MXZL1W', 'http://amazon.in/dp/B017RCTGEE', 'http://amazon.in/dp/B00G7K6REU', 'http://amazon.in/dp/B01N63ZKX0', 'http://amazon.in/dp/B000GCV43O', 'http://amazon.in/dp/B00O0SA198', 'http://amazon.in/dp/B00O386FKE', 'http://amazon.in/dp/B01IR8NAE4', 'http://amazon.in/dp/B00F3IGSLE', 'http://amazon.in/dp/B01N02QFGC', 'http://amazon.in/dp/B004H6V1QU', 'http://amazon.in/dp/B01MFGTAO5', 'http://amazon.in/dp/B01M3Z247T', 'http://amazon.in/dp/B01M6D5GKX', 'http://amazon.in/dp/B006MRPMVC', 'http://amazon.in/dp/B004H6WFGA', 'http://amazon.in/dp/B0012GS2EC', 'http://amazon.in/dp/B00KIYF8VE', 'http://amazon.in/dp/B004CQ5MVU', 'http://amazon.in/dp/B000GCV49S', 'http://amazon.in/dp/B0193G18LQ', 'http://amazon.in/dp/B01N3PT4GP', 'http://amazon.in/dp/B00OP26PE4', 'http://amazon.in/dp/B000GCXSHO', 'http://amazon.in/dp/B004H6YKPE', 'http://amazon.in/dp/B00OP266NO', 'http://amazon.in/dp/B0014CVO6W', 'http://amazon.in/dp/B00VRAEWD8', 'http://amazon.in/dp/B001F51RCY', 'http://amazon.in/dp/B01MXLFQGB', 'http://amazon.in/dp/B000GCY2ZG', 'http://amazon.in/dp/B0015KO3MU', 'http://amazon.in/dp/B0076ON32U', 'http://amazon.in/dp/B01MQH343X', 'http://amazon.in/dp/B00OP1ZPLE', 'http://amazon.in/dp/B007HKXKQW', 'http://amazon.in/dp/B00OP204EG', 'http://amazon.in/dp/B000GCWPPA', 'http://amazon.in/dp/B019H3PL54', 'http://amazon.in/dp/B00LPTDIRC', 'http://amazon.in/dp/B004CQ7S2G', 'http://amazon.in/dp/B000GCXSGK', 'http://amazon.in/dp/B07YWMQRNJ', 'http://amazon.in/dp/B07YWMQWWK', 'http://amazon.in/dp/B07YWMQHYJ', 'http://amazon.in/dp/B07YWNB9T5', 'http://amazon.in/dp/B00791CQ3W', 'http://amazon.in/dp/B08JR4RHCX', 'http://amazon.in/dp/B00791CW6I', 'http://amazon.in/dp/B07YWNN6PZ', 'http://amazon.in/dp/B07YWMV2SD', 'http://amazon.in/dp/B07YWN1PFV', 'http://amazon.in/dp/B07YWMQRNK', 'http://amazon.in/dp/B07YWMQHYK', 'http://amazon.in/dp/B07YWNQPWM', 'http://amazon.in/dp/B07YWNQPWB', 'http://amazon.in/dp/B07YWNMLWX', 'http://amazon.in/dp/B00791CV8C', 'http://amazon.in/dp/B07YWM9WLX', 'http://amazon.in/dp/B07YWNFJC7', 'http://amazon.in/dp/B008TO71NS', 'http://amazon.in/dp/B007E9JHUO', 'http://amazon.in/dp/B08JR3W9TS', 'http://amazon.in/dp/B08JR5D5CT', 'http://amazon.in/dp/B007E9JLH8', 'http://amazon.in/dp/B08JR4TSZM', 'http://amazon.in/dp/B00791CVYG', 'http://amazon.in/dp/B00MM0AW6S', 'http://amazon.in/dp/B08L7K9D2T', 'http://amazon.in/dp/B07YWMQRPH', 'http://amazon.in/dp/B006W84474', 'http://amazon.in/dp/B07YWMZ8K9', 'http://amazon.in/dp/B01BK7FF24', 'http://amazon.in/dp/B08ZSF67QP', 'http://amazon.in/dp/B00791CV28', 'http://amazon.in/dp/B0948D3ZZX', 'http://amazon.in/dp/B009A3W70O', 'http://amazon.in/dp/B08QTVZ7M6', 'http://amazon.in/dp/B07YWN34P4', 'http://amazon.in/dp/B08QTZY6H1', 'http://amazon.in/dp/B07YWNCF7X', 'http://amazon.in/dp/B00791CQE6', 'http://amazon.in/dp/B08QV2PX5G', 'http://amazon.in/dp/B0948FTYMT', 'http://amazon.in/dp/B07SGQ1BSW', 'http://amazon.in/dp/B0948B6FVR', 'http://amazon.in/dp/B07V2LJGNZ', 'http://amazon.in/dp/B08QTW2BG7', 'http://amazon.in/dp/B00NWHNTVA', 'http://amazon.in/dp/B06XFTXJ63', 'http://amazon.in/dp/B06XFVWNKQ', 'http://amazon.in/dp/B08B3ZYSDT', 'http://amazon.in/dp/B0967S85J7', 'http://amazon.in/dp/B004X35SKM', 'http://amazon.in/dp/B08ZS18PNN', 'http://amazon.in/dp/B08QTXS989', 'http://amazon.in/dp/B0054MS8T4', 'http://amazon.in/dp/B08B1HT4D6', 'http://amazon.in/dp/B01N8VIB3I', 'http://amazon.in/dp/B0057P3PV4', 'http://amazon.in/dp/B08L7KXXRZ', 'http://amazon.in/dp/B08L7KMBYM', 'http://amazon.in/dp/B07K7MBQ6B', 'http://amazon.in/dp/B07FDMD7JM', 'http://amazon.in/dp/B08L7J3LL7', 'http://amazon.in/dp/B09487MH16', 'http://amazon.in/dp/B07MRF1PG9', 'http://amazon.in/dp/B01GE9NMTQ', 'http://amazon.in/dp/B077RSNP4Y', 'http://amazon.in/dp/B08KHHY46V', 'http://amazon.in/dp/B09486WSKH', 'http://amazon.in/dp/B08B1DB5NY', 'http://amazon.in/dp/B08L7JQ8CS', 'http://amazon.in/dp/B07FDJ1KG6', 'http://amazon.in/dp/B08B1JTSTB', 'http://amazon.in/dp/B06XFWBLT1', 'http://amazon.in/dp/B0948PSH2K', 'http://amazon.in/dp/B00UN5U4MG', 'http://amazon.in/dp/B06XYKK5Z8', 'http://amazon.in/dp/B08QVHXC38', 'http://amazon.in/dp/B01H8WYTCW', 'http://amazon.in/dp/B07M6B4V8X', 'http://amazon.in/dp/B06XFNNPNP', 'http://amazon.in/dp/B09486WSKX', 'http://amazon.in/dp/B07BWLLB4D', 'http://amazon.in/dp/B07MH82D47', 'http://amazon.in/dp/B08QV82VC1', 'http://amazon.in/dp/B00UN5X5V8', 'http://amazon.in/dp/B0948F21JZ', 'http://amazon.in/dp/B09488D8CW', 'http://amazon.in/dp/B07MDN5ZPD', 'http://amazon.in/dp/B07SNBRVLZ', 'http://amazon.in/dp/B08QTVDVB2', 'http://amazon.in/dp/B0146R5KIO', 'http://amazon.in/dp/B0948FSVR7', 'http://amazon.in/dp/B0948FFQ2D', 'http://amazon.in/dp/B08QVF68PS', 'http://amazon.in/dp/B08QVDFFGX', 'http://amazon.in/dp/B01N7N4VXN', 'http://amazon.in/dp/B07FDD95CC', 'http://amazon.in/dp/B0948B9L8W', 'http://amazon.in/dp/B08QV1JQJB', 'http://amazon.in/dp/B07RQM2NV6', 'http://amazon.in/dp/B06XFPQJJR', 'http://amazon.in/dp/B08PD6H9BB', 'http://amazon.in/dp/B08QTZY6HZ', 'http://amazon.in/dp/B08L7LS7RB', 'http://amazon.in/dp/B08QVFXKD4', 'http://amazon.in/dp/B08QTXS96W', 'http://amazon.in/dp/B08QTW2BJ1', 'http://amazon.in/dp/B0947XX9QB', 'http://amazon.in/dp/B0948MM1QJ', 'http://amazon.in/dp/B0948H4KRS', 'http://amazon.in/dp/B00MX8NELO', 'http://amazon.in/dp/B08KHHF9HZ', 'http://amazon.in/dp/B093G14ZMN', 'http://amazon.in/dp/B08QTPWHZ4', 'http://amazon.in/dp/B0948H64C5', 'http://amazon.in/dp/B07MRB35WC', 'http://amazon.in/dp/B013UWBE9U', 'http://amazon.in/dp/B07JXL45M3', 'http://amazon.in/dp/B01MSV9O09', 'http://amazon.in/dp/B08KHHP4PG', 'http://amazon.in/dp/B08B1GSXX7', 'http://amazon.in/dp/B0967NTMC1', 'http://amazon.in/dp/B0967SSZ9N', 'http://amazon.in/dp/B0967QHYQG', 'http://amazon.in/dp/B0948B5JH3', 'http://amazon.in/dp/B094848QSZ', 'http://amazon.in/dp/B09482GGZJ', 'http://amazon.in/dp/B07D7V1CD7', 'http://amazon.in/dp/B07TBG6H63', 'http://amazon.in/dp/B07X7P4B18', 'http://amazon.in/dp/B085TW6G85', 'http://amazon.in/dp/B07F2QCLP2', 'http://amazon.in/dp/B07F2Q4C35', 'http://amazon.in/dp/B07F2ZXJN7', 'http://amazon.in/dp/B07L3YNL2V', 'http://amazon.in/dp/B07FHD9Y8M', 'http://amazon.in/dp/B07F31KJXB', 'http://amazon.in/dp/B07L3ZCJ53', 'http://amazon.in/dp/B07FJ7NDGK', 'http://amazon.in/dp/B07M857C6Z', 'http://amazon.in/dp/B088CCYM9D', 'http://amazon.in/dp/B07MQWT396', 'http://amazon.in/dp/B07FHD9PDZ', 'http://amazon.in/dp/B07F7LB4T9', 'http://amazon.in/dp/B074ZCKWSN', 'http://amazon.in/dp/B0811T2HDY', 'http://amazon.in/dp/B08QTWMZPY', 'http://amazon.in/dp/B0811TDGVZ', 'http://amazon.in/dp/B07FJ7W7PH', 'http://amazon.in/dp/B0811TQS47', 'http://amazon.in/dp/B0839HW5GB', 'http://amazon.in/dp/B07H8Z4YRX', 'http://amazon.in/dp/B0749TNSBS', 'http://amazon.in/dp/B089H69JCW', 'http://amazon.in/dp/B0839J7LLB', 'http://amazon.in/dp/B079585Q26', 'http://amazon.in/dp/B06WGLB9FY', 'http://amazon.in/dp/B018U1F668', 'http://amazon.in/dp/B00TBJSS0A', 'http://amazon.in/dp/B0756YSR2R', 'http://amazon.in/dp/B00TBJSJV8', 'http://amazon.in/dp/B07F2RZB46', 'http://amazon.in/dp/B0839JT14H', 'http://amazon.in/dp/B07F2Q47ST', 'http://amazon.in/dp/B0811T924L', 'http://amazon.in/dp/B0839J9QRV', 'http://amazon.in/dp/B00TBJSR1A', 'http://amazon.in/dp/B0839JL9R5', 'http://amazon.in/dp/B06XDLHJFJ', 'http://amazon.in/dp/B07F2RV8BD', 'http://amazon.in/dp/B0811TVR7G', 'http://amazon.in/dp/B07F2RZ8TR', 'http://amazon.in/dp/B07C32SZ8L', 'http://amazon.in/dp/B074Z3CF8S', 'http://amazon.in/dp/B01LZKXTRI', 'http://amazon.in/dp/B01GUZC21S', 'http://amazon.in/dp/B07F344NGC', 'http://amazon.in/dp/B07VJNN2CG', 'http://amazon.in/dp/B078PKR7WF', 'http://amazon.in/dp/B07FKWKQ85', 'http://amazon.in/dp/B07CS3238V', 'http://amazon.in/dp/B07FL4M4HV', 'http://amazon.in/dp/B078GQPL14', 'http://amazon.in/dp/B00TBJSJPO', 'http://amazon.in/dp/B00TBJT3L8', 'http://amazon.in/dp/B0839J3QZT', 'http://amazon.in/dp/B07J5NLHWW', 'http://amazon.in/dp/B078GMZ96P', 'http://amazon.in/dp/B0839JC89K', 'http://amazon.in/dp/B00TBJSJM2', 'http://amazon.in/dp/B01LZWP9Q7', 'http://amazon.in/dp/B0839HQDDV', 'http://amazon.in/dp/B07F2Q4B71', 'http://amazon.in/dp/B00U1CDVT4', 'http://amazon.in/dp/B016FYQ2D8', 'http://amazon.in/dp/B0839JDKMC', 'http://amazon.in/dp/B0142R3PY4', 'http://amazon.in/dp/B0105Y4PCO', 'http://amazon.in/dp/B00YBTE0N4', 'http://amazon.in/dp/B0839HYW7B', 'http://amazon.in/dp/B06Y3QTFK3', 'http://amazon.in/dp/B08QVG8B73', 'http://amazon.in/dp/B0839JC8HR', 'http://amazon.in/dp/B0839HYW4V', 'http://amazon.in/dp/B0839J2BKF', 'http://amazon.in/dp/B00U2PPXC8', 'http://amazon.in/dp/B08PDBQ2RQ', 'http://amazon.in/dp/B01GUYOL5O', 'http://amazon.in/dp/B0839J9QX8', 'http://amazon.in/dp/B0839JBFJY', 'http://amazon.in/dp/B0839J69BR', 'http://amazon.in/dp/B0839JDVVZ', 'http://amazon.in/dp/B00AO4E9E0', 'http://amazon.in/dp/B014C5DYDS', 'http://amazon.in/dp/B0839HNNV8', 'http://amazon.in/dp/B0839J5BFL', 'http://amazon.in/dp/B08QV8JDNL', 'http://amazon.in/dp/B0839J6MNP', 'http://amazon.in/dp/B0839HQ4B3', 'http://amazon.in/dp/B0839HM1BS', 'http://amazon.in/dp/B0839K69SX', 'http://amazon.in/dp/B0839HZ2Y9', 'http://amazon.in/dp/B08KHHT2KZ', 'http://amazon.in/dp/B0839J5JVP', 'http://amazon.in/dp/B012U0UNFO', 'http://amazon.in/dp/B0839J695L', 'http://amazon.in/dp/B0839J25PM', 'http://amazon.in/dp/B0839JHJKT', 'http://amazon.in/dp/B0839JC45K', 'http://amazon.in/dp/B01CUD2U5M', 'http://amazon.in/dp/B014NC3E3A', 'http://amazon.in/dp/B07G4QSGFH', 'http://amazon.in/dp/B001EVUXY2', 'http://amazon.in/dp/B0839HWZWT', 'http://amazon.in/dp/B01HC2BPZM', 'http://amazon.in/dp/B018J0DDOW', 'http://amazon.in/dp/B0839JMCZF', 'http://amazon.in/dp/B00JEOHITE', 'http://amazon.in/dp/B01G5ZLJEE', 'http://amazon.in/dp/B012U0UZDY', 'http://amazon.in/dp/B0839JL9NK', 'http://amazon.in/dp/B00OPNES4W', 'http://amazon.in/dp/B0199WNJE8', 'http://amazon.in/dp/B00D3LJTQE', 'http://amazon.in/dp/B07FTJDF2S', 'http://amazon.in/dp/B01AM5FAHK', 'http://amazon.in/dp/B07662P4NW', 'http://amazon.in/dp/B0839H7Z8S', 'http://amazon.in/dp/B0839HXT98', 'http://amazon.in/dp/B0839JDW6W', 'http://amazon.in/dp/B0839JMD7R', 'http://amazon.in/dp/B016P6GBB4', 'http://amazon.in/dp/B004Q5M7O2', 'http://amazon.in/dp/B00OQ85N8Q', 'http://amazon.in/dp/B00PATJUOS', 'http://amazon.in/dp/B0073SBEPC', 'http://amazon.in/dp/B00I9OIBRS', 'http://amazon.in/dp/B01NBC40S9', 'http://amazon.in/dp/B00I877BJK', 'http://amazon.in/dp/B012U0WEBA', 'http://amazon.in/dp/B004Q5M7L0', 'http://amazon.in/dp/B003VDGE80', 'http://amazon.in/dp/B00GYB1AQM', 'http://amazon.in/dp/B0839J1T81', 'http://amazon.in/dp/B01BX1NLT6', 'http://amazon.in/dp/B0839HV7XD', 'http://amazon.in/dp/B00TBJSRLA', 'http://amazon.in/dp/B0839JSZNL', 'http://amazon.in/dp/B00P7RGSWK', 'http://amazon.in/dp/B00OQ3C8FM', 'http://amazon.in/dp/B00D9R1OY2', 'http://amazon.in/dp/B01CHNX97I', 'http://amazon.in/dp/B00OQ890AI', 'http://amazon.in/dp/B003F184N6', 'http://amazon.in/dp/B00CQ41JE4', 'http://amazon.in/dp/B07HB4FKZS', 'http://amazon.in/dp/B07HB4L36F', 'http://amazon.in/dp/B07H9SV61Y', 'http://amazon.in/dp/B07HLZDR9S', 'http://amazon.in/dp/B07H9X7WT9', 'http://amazon.in/dp/B07H9T25WH', 'http://amazon.in/dp/B07HMCC4RF', 'http://amazon.in/dp/B07H9YBYSK', 'http://amazon.in/dp/B07HB1YHZP', 'http://amazon.in/dp/B085WKPQZ7', 'http://amazon.in/dp/B00QKAQN3M', 'http://amazon.in/dp/B07HLZDKNN', 'http://amazon.in/dp/B085WJY6NH', 'http://amazon.in/dp/B07H9X7WTG', 'http://amazon.in/dp/B07HMCZJ2P', 'http://amazon.in/dp/B018HGSZO6', 'http://amazon.in/dp/B07H9YCB5L', 'http://amazon.in/dp/B00MUYXORA', 'http://amazon.in/dp/B00CQ416YW', 'http://amazon.in/dp/B017BFNGLG', 'http://amazon.in/dp/B0811TYPM5', 'http://amazon.in/dp/B006T8BXF8', 'http://amazon.in/dp/B01CGETA9Y', 'http://amazon.in/dp/B00IOVOFGW', 'http://amazon.in/dp/B07F4551H9', 'http://amazon.in/dp/B07BDP69GH', 'http://amazon.in/dp/B00UFF6NR4', 'http://amazon.in/dp/B01INE0P6I', 'http://amazon.in/dp/B08377XNND', 'http://amazon.in/dp/B078B5LLBV', 'http://amazon.in/dp/B07J314NP8', 'http://amazon.in/dp/B07NWN452X', 'http://amazon.in/dp/B082XLSR2X', 'http://amazon.in/dp/B00GSGO6OQ', 'http://amazon.in/dp/B0811TXJ26', 'http://amazon.in/dp/B0757317HZ', 'http://amazon.in/dp/B06XSC2GYR', 'http://amazon.in/dp/B075766WW1', 'http://amazon.in/dp/B0839PMTP3', 'http://amazon.in/dp/B00UFF6WSY', 'http://amazon.in/dp/B07BDQ5G1L', 'http://amazon.in/dp/B085WKPQZ8', 'http://amazon.in/dp/B06Y5T7TMJ', 'http://amazon.in/dp/B00XHRR3FI', 'http://amazon.in/dp/B06XRX1S56', 'http://amazon.in/dp/B00BU1FYUO', 'http://amazon.in/dp/B01DP01I7A', 'http://amazon.in/dp/B00CQ417NM', 'http://amazon.in/dp/B07XTM81NS', 'http://amazon.in/dp/B095C9DZTG', 'http://amazon.in/dp/B00OJ2B9AU', 'http://amazon.in/dp/B000GCY224', 'http://amazon.in/dp/B071P13PSJ', 'http://amazon.in/dp/B01BGSDWKO', 'http://amazon.in/dp/B01MA6CBRC', 'http://amazon.in/dp/B00Y9M46AA', 'http://amazon.in/dp/B095C8VJZ4', 'http://amazon.in/dp/B0839PY7SR', 'http://amazon.in/dp/B0839HH1NH', 'http://amazon.in/dp/B00LM6ASRQ', 'http://amazon.in/dp/B0839HRX8C', 'http://amazon.in/dp/B075TGTP17', 'http://amazon.in/dp/B01MXX6IC8', 'http://amazon.in/dp/B095C8S456', 'http://amazon.in/dp/B095C8MWRP', 'http://amazon.in/dp/B0839HXSZ8', 'http://amazon.in/dp/B01MRVZQ0F', 'http://amazon.in/dp/B095C95CM6', 'http://amazon.in/dp/B073RHPWF9', 'http://amazon.in/dp/B095C94LKP', 'http://amazon.in/dp/B0811TGMRZ', 'http://amazon.in/dp/B000RK9XLA', 'http://amazon.in/dp/B0839J5JKP', 'http://amazon.in/dp/B08X4TCWJD', 'http://amazon.in/dp/B000JBY3CG', 'http://amazon.in/dp/B071XQ8LR2', 'http://amazon.in/dp/B00JVBGX8C', 'http://amazon.in/dp/B08398V93H', 'http://amazon.in/dp/B0839912XQ', 'http://amazon.in/dp/B00EK0BH9Y', 'http://amazon.in/dp/B07W1RYDDT', 'http://amazon.in/dp/B01N49E07T', 'http://amazon.in/dp/B07BHYB44L', 'http://amazon.in/dp/B0839JL9G6', 'http://amazon.in/dp/B08399PQ3J', 'http://amazon.in/dp/B08399CNJT', 'http://amazon.in/dp/B01N1NRJVZ', 'http://amazon.in/dp/B00OZG2RPG', 'http://amazon.in/dp/B00FQR4JOK', 'http://amazon.in/dp/B08398YNKF', 'http://amazon.in/dp/B000RYYI7K', 'http://amazon.in/dp/B07FKF8J7V', 'http://amazon.in/dp/B0839JHJBW', 'http://amazon.in/dp/B08399NC37', 'http://amazon.in/dp/B00JOLRYXW', 'http://amazon.in/dp/B01MXTOD3A', 'http://amazon.in/dp/B00JGQ2R1Y', 'http://amazon.in/dp/B0839HMC39', 'http://amazon.in/dp/B01MRW052J', 'http://amazon.in/dp/B004DBXKS6', 'http://amazon.in/dp/B083991L8X', 'http://amazon.in/dp/B07G1D17TY', 'http://amazon.in/dp/B01MEENE3N', 'http://amazon.in/dp/B00CHHKN3S', 'http://amazon.in/dp/B00CHHJQOU', 'http://amazon.in/dp/B01BMQ2BLQ', 'http://amazon.in/dp/B00NH74FAE', 'http://amazon.in/dp/B006T8BWUE', 'http://amazon.in/dp/B00JVBJ2EE', 'http://amazon.in/dp/B00AVWJROM', 'http://amazon.in/dp/B00CTSYIWM', 'http://amazon.in/dp/B001ET7ERS', 'http://amazon.in/dp/B06XG4YCK6', 'http://amazon.in/dp/B00JFLDMZU', 'http://amazon.in/dp/B095C7TWZ5', 'http://amazon.in/dp/B0839HLKFN', 'http://amazon.in/dp/B078FBR95Z']
    # start_urls = ['http://amazon.in/dp/B08T3325CD', 'http://amazon.in/dp/B08CSHBPD5', 'http://amazon.in/dp/B08T2Y2Q4T', 'http://amazon.in/dp/B008KH5U28', 'http://amazon.in/dp/B006LXAG4K', 'http://amazon.in/dp/B00IF3W4DK', 'http://amazon.in/dp/B074VG8ZH8', 'http://amazon.in/dp/B08HJC7GXS', 'http://amazon.in/dp/B08HH3YLGZ', 'http://amazon.in/dp/B08K3HQ4M4', 'http://amazon.in/dp/B004R6HWB8', 'http://amazon.in/dp/B01N1KE7D5', 'http://amazon.in/dp/B07MNZTKBS', 'http://amazon.in/dp/B01KC4BWN2', 'http://amazon.in/dp/B08QV7QXF2', 'http://amazon.in/dp/B08QTQZZFH', 'http://amazon.in/dp/B01HBA74PU', 'http://amazon.in/dp/B01IOPY3G4', 'http://amazon.in/dp/B01M3PPPBU', 'http://amazon.in/dp/B08LGZM288', 'http://amazon.in/dp/B07QXTBSMQ', 'http://amazon.in/dp/B07BMZD88Q', 'http://amazon.in/dp/B01M0OX5NU', 'http://amazon.in/dp/B00L322HT6', 'http://amazon.in/dp/B08QV4BHK4', 'http://amazon.in/dp/B07FLB3Z66', 'http://amazon.in/dp/B07MRHZQVB', 'http://amazon.in/dp/B08LGZWBPT', 'http://amazon.in/dp/B08K3GSYTY', 'http://amazon.in/dp/B08LH1MD56', 'http://amazon.in/dp/B077PT2S31', 'http://amazon.in/dp/B01M6BLCES', 'http://amazon.in/dp/B08LGQ582N', 'http://amazon.in/dp/B08LGZSXGH', 'http://amazon.in/dp/B004XADCA8', 'http://amazon.in/dp/B001RYOOUK', 'http://amazon.in/dp/B01MG81SLM', 'http://amazon.in/dp/B08LH19Y3Y', 'http://amazon.in/dp/B086XP97N8', 'http://amazon.in/dp/B0854B9FPK', 'http://amazon.in/dp/B08PDB8CMT', 'http://amazon.in/dp/B01M1O4JAA', 'http://amazon.in/dp/B00YBTAOPM', 'http://amazon.in/dp/B08LGYCF36', 'http://amazon.in/dp/B073JMX9X6', 'http://amazon.in/dp/B001P1ZC9M', 'http://amazon.in/dp/B000UULQMQ', 'http://amazon.in/dp/B08J3T8TY1', 'http://amazon.in/dp/B01M01MNXI', 'http://amazon.in/dp/B06Y3QZ895', 'http://amazon.in/dp/B00144PBQE', 'http://amazon.in/dp/B00AREI3S0', 'http://amazon.in/dp/B073JPPRXS', 'http://amazon.in/dp/B01LX41KJW', 'http://amazon.in/dp/B0046HBPV6', 'http://amazon.in/dp/B00923XTFY', 'http://amazon.in/dp/B001P1ZELS', 'http://amazon.in/dp/B00N1T66U0', 'http://amazon.in/dp/B01N45HDW8', 'http://amazon.in/dp/B07GK1R981', 'http://amazon.in/dp/B0948B9L8H', 'http://amazon.in/dp/B006DQWRV0', 'http://amazon.in/dp/B07WX4YDRN', 'http://amazon.in/dp/B0031TSC34', 'http://amazon.in/dp/B01LX41O04', 'http://amazon.in/dp/B07C65Y91Y', 'http://amazon.in/dp/B073JPXMF6', 'http://amazon.in/dp/B01MG7T1P7', 'http://amazon.in/dp/B08LH1FW8F', 'http://amazon.in/dp/B07G81NF68', 'http://amazon.in/dp/B07WMWP6Z5', 'http://amazon.in/dp/B01M112TLH', 'http://amazon.in/dp/B01M0MI70A', 'http://amazon.in/dp/B07WXZ8ZZX', 'http://amazon.in/dp/B073JPVB7D', 'http://amazon.in/dp/B07VM7XZJC', 'http://amazon.in/dp/B07FCH2WX1', 'http://amazon.in/dp/B00DZHYA24', 'http://amazon.in/dp/B001TH8Y4C', 'http://amazon.in/dp/B08PD8RDRD']
    # start_urls = ['http://amazon.in/dp/B08PDB1J26', 'http://amazon.in/dp/B07J3LG4ZZ', 'http://amazon.in/dp/B001VD3L8I', 'http://amazon.in/dp/B076DC9Z6Z', 'http://amazon.in/dp/B0948992RV', 'http://amazon.in/dp/B07FNSLG9D', 'http://amazon.in/dp/B01M01MQPB', 'http://amazon.in/dp/B08LH1SL4L', 'http://amazon.in/dp/B08PD9WXK1', 'http://amazon.in/dp/B08PD9ZXSP', 'http://amazon.in/dp/B01GHKXMGU', 'http://amazon.in/dp/B08LH1FVPQ', 'http://amazon.in/dp/B076DGQYHQ', 'http://amazon.in/dp/B07FNWJ1JF', 'http://amazon.in/dp/B081BBXLKJ', 'http://amazon.in/dp/B08PDD5WKY', 'http://amazon.in/dp/B06Y69MMT4', 'http://amazon.in/dp/B015Z96HQ6', 'http://amazon.in/dp/B07P8N15VM', 'http://amazon.in/dp/B00KCKZPX0', 'http://amazon.in/dp/B08K3KNNW3', 'http://amazon.in/dp/B07P8MZ67Q', 'http://amazon.in/dp/B073JPGKLX', 'http://amazon.in/dp/B08LH36Z9Q', 'http://amazon.in/dp/B08LH1H3M7', 'http://amazon.in/dp/B08PDC3TNC', 'http://amazon.in/dp/B073JPR2TJ', 'http://amazon.in/dp/B01LY3NCGX', 'http://amazon.in/dp/B08PD6R8DX', 'http://amazon.in/dp/B08JWR5PH7', 'http://amazon.in/dp/B078M1JM3D', 'http://amazon.in/dp/B08PDB23X8', 'http://amazon.in/dp/B008UTZV70', 'http://amazon.in/dp/B08K3FJL3C', 'http://amazon.in/dp/B08JDLNVDR', 'http://amazon.in/dp/B089FS65DP', 'http://amazon.in/dp/B07DFYNW7B', 'http://amazon.in/dp/B08PD8Y4SN', 'http://amazon.in/dp/B08LH1N4TM', 'http://amazon.in/dp/B07WF1QQHF', 'http://amazon.in/dp/B07P7HMW8P', 'http://amazon.in/dp/B00KCKZSN2', 'http://amazon.in/dp/B076Y3YP9T', 'http://amazon.in/dp/B007IX0CM8', 'http://amazon.in/dp/B08PD9JN72', 'http://amazon.in/dp/B08LGRJXP6', 'http://amazon.in/dp/B08K3JLNP7', 'http://amazon.in/dp/B08LGRJYZN', 'http://amazon.in/dp/B01M0OX4L7', 'http://amazon.in/dp/B08LGPJHF2', 'http://amazon.in/dp/B07FR9NVGV', 'http://amazon.in/dp/B00SLIL9GM', 'http://amazon.in/dp/B005HIH24W', 'http://amazon.in/dp/B01A6ADLTK', 'http://amazon.in/dp/B0752FXRQJ', 'http://amazon.in/dp/B06X3SXGVF', 'http://amazon.in/dp/B0752HG1ZY', 'http://amazon.in/dp/B00HX5PYTM', 'http://amazon.in/dp/B00AREI3BC', 'http://amazon.in/dp/B000NPVDB2', 'http://amazon.in/dp/B00AREI5KG', 'http://amazon.in/dp/B08LGXB2CW', 'http://amazon.in/dp/B08PD9WXH5', 'http://amazon.in/dp/B00ID0WYHQ', 'http://amazon.in/dp/B002PBJLMU', 'http://amazon.in/dp/B00SZ7QHGG', 'http://amazon.in/dp/B00AF9DJ0Y', 'http://amazon.in/dp/B00OO18UJE', 'http://amazon.in/dp/B01MS3DF6F', 'http://amazon.in/dp/B06Y42BWNP', 'http://amazon.in/dp/B01A69YCEO', 'http://amazon.in/dp/B00EWA3X62', 'http://amazon.in/dp/B005HIH67A', 'http://amazon.in/dp/B08JWKJB9R', 'http://amazon.in/dp/B07VJNNV7D', 'http://amazon.in/dp/B07J57F3RM', 'http://amazon.in/dp/B073JNWHBT', 'http://amazon.in/dp/B08KHHJGY4', 'http://amazon.in/dp/B01N6MUC0S', 'http://amazon.in/dp/B08LH1MQ2T']
    # start_urls = ['http://amazon.in/dp/B08LH17HK8', 'http://amazon.in/dp/B08PDB3N9F', 'http://amazon.in/dp/B073BDP9VM', 'http://amazon.in/dp/B08LH2YM2G', 'http://amazon.in/dp/B08LH1V8MK', 'http://amazon.in/dp/B08LGZWDJH', 'http://amazon.in/dp/B08LGZTKCZ', 'http://amazon.in/dp/B08LH2YM3R', 'http://amazon.in/dp/B076Y229S1', 'http://amazon.in/dp/B017LTGG2S', 'http://amazon.in/dp/B07DFRLCVS', 'http://amazon.in/dp/B07DFSGXDG', 'http://amazon.in/dp/B00G9Z3HGE', 'http://amazon.in/dp/B00ENZRCBI', 'http://amazon.in/dp/B0764M9QVV', 'http://amazon.in/dp/B0764MLHRM', 'http://amazon.in/dp/B077P87ZB4', 'http://amazon.in/dp/B00ENZRLRS', 'http://amazon.in/dp/B077P1B5X4', 'http://amazon.in/dp/B08KHZH344', 'http://amazon.in/dp/B08194PS69', 'http://amazon.in/dp/B077P88293', 'http://amazon.in/dp/B01EJIEC8O', 'http://amazon.in/dp/B08KGR2MZ1', 'http://amazon.in/dp/B08KHZD46M', 'http://amazon.in/dp/B07P21CHH8', 'http://amazon.in/dp/B089DZGNN1', 'http://amazon.in/dp/B0769S19YV', 'http://amazon.in/dp/B01H7BOYNS', 'http://amazon.in/dp/B08194DMZP', 'http://amazon.in/dp/B01HBA4VMY', 'http://amazon.in/dp/B07NZW6WNN', 'http://amazon.in/dp/B077SSHGPM', 'http://amazon.in/dp/B089DZKT4W', 'http://amazon.in/dp/B081BG8LDS', 'http://amazon.in/dp/B08BXJ3WD9', 'http://amazon.in/dp/B08BXLVDF1', 'http://amazon.in/dp/B07P354C4B', 'http://amazon.in/dp/B08QV8TD41', 'http://amazon.in/dp/B07R9KVCJJ', 'http://amazon.in/dp/B012RBB148', 'http://amazon.in/dp/B01IR8NCB0', 'http://amazon.in/dp/B079VQY6VZ', 'http://amazon.in/dp/B01F6XQ9VY', 'http://amazon.in/dp/B00O0RVIJQ', 'http://amazon.in/dp/B00U5ZIYAS', 'http://amazon.in/dp/B015MXZL1W', 'http://amazon.in/dp/B017RCTGEE', 'http://amazon.in/dp/B00G7K6REU', 'http://amazon.in/dp/B01N63ZKX0', 'http://amazon.in/dp/B000GCV43O', 'http://amazon.in/dp/B00O0SA198', 'http://amazon.in/dp/B00O386FKE', 'http://amazon.in/dp/B01IR8NAE4', 'http://amazon.in/dp/B00F3IGSLE', 'http://amazon.in/dp/B01N02QFGC', 'http://amazon.in/dp/B004H6V1QU', 'http://amazon.in/dp/B01MFGTAO5', 'http://amazon.in/dp/B01M3Z247T', 'http://amazon.in/dp/B01M6D5GKX', 'http://amazon.in/dp/B006MRPMVC', 'http://amazon.in/dp/B004H6WFGA', 'http://amazon.in/dp/B0012GS2EC', 'http://amazon.in/dp/B00KIYF8VE', 'http://amazon.in/dp/B004CQ5MVU', 'http://amazon.in/dp/B000GCV49S', 'http://amazon.in/dp/B0193G18LQ', 'http://amazon.in/dp/B01N3PT4GP', 'http://amazon.in/dp/B00OP26PE4', 'http://amazon.in/dp/B000GCXSHO', 'http://amazon.in/dp/B004H6YKPE', 'http://amazon.in/dp/B00OP266NO', 'http://amazon.in/dp/B0014CVO6W', 'http://amazon.in/dp/B00VRAEWD8', 'http://amazon.in/dp/B001F51RCY', 'http://amazon.in/dp/B01MXLFQGB', 'http://amazon.in/dp/B000GCY2ZG', 'http://amazon.in/dp/B0015KO3MU', 'http://amazon.in/dp/B0076ON32U', 'http://amazon.in/dp/B01MQH343X']
    # start_urls = ['http://amazon.in/dp/B00OP1ZPLE', 'http://amazon.in/dp/B007HKXKQW', 'http://amazon.in/dp/B00OP204EG', 'http://amazon.in/dp/B000GCWPPA', 'http://amazon.in/dp/B019H3PL54', 'http://amazon.in/dp/B00LPTDIRC', 'http://amazon.in/dp/B004CQ7S2G', 'http://amazon.in/dp/B000GCXSGK', 'http://amazon.in/dp/B07YWMQRNJ', 'http://amazon.in/dp/B07YWMQWWK', 'http://amazon.in/dp/B07YWMQHYJ', 'http://amazon.in/dp/B07YWNB9T5', 'http://amazon.in/dp/B00791CQ3W', 'http://amazon.in/dp/B08JR4RHCX', 'http://amazon.in/dp/B00791CW6I', 'http://amazon.in/dp/B07YWNN6PZ', 'http://amazon.in/dp/B07YWMV2SD', 'http://amazon.in/dp/B07YWN1PFV', 'http://amazon.in/dp/B07YWMQRNK', 'http://amazon.in/dp/B07YWMQHYK', 'http://amazon.in/dp/B07YWNQPWM', 'http://amazon.in/dp/B07YWNQPWB', 'http://amazon.in/dp/B07YWNMLWX', 'http://amazon.in/dp/B00791CV8C', 'http://amazon.in/dp/B07YWM9WLX', 'http://amazon.in/dp/B07YWNFJC7', 'http://amazon.in/dp/B008TO71NS', 'http://amazon.in/dp/B007E9JHUO', 'http://amazon.in/dp/B08JR3W9TS', 'http://amazon.in/dp/B08JR5D5CT', 'http://amazon.in/dp/B007E9JLH8', 'http://amazon.in/dp/B08JR4TSZM', 'http://amazon.in/dp/B00791CVYG', 'http://amazon.in/dp/B00MM0AW6S', 'http://amazon.in/dp/B08L7K9D2T', 'http://amazon.in/dp/B07YWMQRPH', 'http://amazon.in/dp/B006W84474', 'http://amazon.in/dp/B07YWMZ8K9', 'http://amazon.in/dp/B01BK7FF24', 'http://amazon.in/dp/B08ZSF67QP', 'http://amazon.in/dp/B00791CV28', 'http://amazon.in/dp/B0948D3ZZX', 'http://amazon.in/dp/B009A3W70O', 'http://amazon.in/dp/B08QTVZ7M6', 'http://amazon.in/dp/B07YWN34P4', 'http://amazon.in/dp/B08QTZY6H1', 'http://amazon.in/dp/B07YWNCF7X', 'http://amazon.in/dp/B00791CQE6', 'http://amazon.in/dp/B08QV2PX5G', 'http://amazon.in/dp/B0948FTYMT', 'http://amazon.in/dp/B07SGQ1BSW', 'http://amazon.in/dp/B0948B6FVR', 'http://amazon.in/dp/B07V2LJGNZ', 'http://amazon.in/dp/B08QTW2BG7', 'http://amazon.in/dp/B00NWHNTVA', 'http://amazon.in/dp/B06XFTXJ63', 'http://amazon.in/dp/B06XFVWNKQ', 'http://amazon.in/dp/B08B3ZYSDT', 'http://amazon.in/dp/B0967S85J7', 'http://amazon.in/dp/B004X35SKM', 'http://amazon.in/dp/B08ZS18PNN', 'http://amazon.in/dp/B08QTXS989', 'http://amazon.in/dp/B0054MS8T4', 'http://amazon.in/dp/B08B1HT4D6', 'http://amazon.in/dp/B01N8VIB3I', 'http://amazon.in/dp/B0057P3PV4', 'http://amazon.in/dp/B08L7KXXRZ', 'http://amazon.in/dp/B08L7KMBYM', 'http://amazon.in/dp/B07K7MBQ6B', 'http://amazon.in/dp/B07FDMD7JM', 'http://amazon.in/dp/B08L7J3LL7', 'http://amazon.in/dp/B09487MH16', 'http://amazon.in/dp/B07MRF1PG9', 'http://amazon.in/dp/B01GE9NMTQ', 'http://amazon.in/dp/B077RSNP4Y', 'http://amazon.in/dp/B08KHHY46V', 'http://amazon.in/dp/B09486WSKH', 'http://amazon.in/dp/B08B1DB5NY', 'http://amazon.in/dp/B08L7JQ8CS', 'http://amazon.in/dp/B07FDJ1KG6']
    # start_urls = ['http://amazon.in/dp/B08B1JTSTB', 'http://amazon.in/dp/B06XFWBLT1', 'http://amazon.in/dp/B0948PSH2K', 'http://amazon.in/dp/B00UN5U4MG', 'http://amazon.in/dp/B06XYKK5Z8', 'http://amazon.in/dp/B08QVHXC38', 'http://amazon.in/dp/B01H8WYTCW', 'http://amazon.in/dp/B07M6B4V8X', 'http://amazon.in/dp/B06XFNNPNP', 'http://amazon.in/dp/B09486WSKX', 'http://amazon.in/dp/B07BWLLB4D', 'http://amazon.in/dp/B07MH82D47', 'http://amazon.in/dp/B08QV82VC1', 'http://amazon.in/dp/B00UN5X5V8', 'http://amazon.in/dp/B0948F21JZ', 'http://amazon.in/dp/B09488D8CW', 'http://amazon.in/dp/B07MDN5ZPD', 'http://amazon.in/dp/B07SNBRVLZ', 'http://amazon.in/dp/B08QTVDVB2', 'http://amazon.in/dp/B0146R5KIO', 'http://amazon.in/dp/B0948FSVR7', 'http://amazon.in/dp/B0948FFQ2D', 'http://amazon.in/dp/B08QVF68PS', 'http://amazon.in/dp/B08QVDFFGX', 'http://amazon.in/dp/B01N7N4VXN', 'http://amazon.in/dp/B07FDD95CC', 'http://amazon.in/dp/B0948B9L8W', 'http://amazon.in/dp/B08QV1JQJB', 'http://amazon.in/dp/B07RQM2NV6', 'http://amazon.in/dp/B06XFPQJJR', 'http://amazon.in/dp/B08PD6H9BB', 'http://amazon.in/dp/B08QTZY6HZ', 'http://amazon.in/dp/B08L7LS7RB', 'http://amazon.in/dp/B08QVFXKD4', 'http://amazon.in/dp/B08QTXS96W', 'http://amazon.in/dp/B08QTW2BJ1', 'http://amazon.in/dp/B0947XX9QB', 'http://amazon.in/dp/B0948MM1QJ', 'http://amazon.in/dp/B0948H4KRS', 'http://amazon.in/dp/B00MX8NELO', 'http://amazon.in/dp/B08KHHF9HZ', 'http://amazon.in/dp/B093G14ZMN', 'http://amazon.in/dp/B08QTPWHZ4', 'http://amazon.in/dp/B0948H64C5', 'http://amazon.in/dp/B07MRB35WC', 'http://amazon.in/dp/B013UWBE9U', 'http://amazon.in/dp/B07JXL45M3', 'http://amazon.in/dp/B01MSV9O09', 'http://amazon.in/dp/B08KHHP4PG', 'http://amazon.in/dp/B08B1GSXX7', 'http://amazon.in/dp/B0967NTMC1', 'http://amazon.in/dp/B0967SSZ9N', 'http://amazon.in/dp/B0967QHYQG', 'http://amazon.in/dp/B0948B5JH3', 'http://amazon.in/dp/B094848QSZ', 'http://amazon.in/dp/B09482GGZJ', 'http://amazon.in/dp/B07D7V1CD7', 'http://amazon.in/dp/B07TBG6H63', 'http://amazon.in/dp/B07X7P4B18', 'http://amazon.in/dp/B085TW6G85', 'http://amazon.in/dp/B07F2QCLP2', 'http://amazon.in/dp/B07F2Q4C35', 'http://amazon.in/dp/B07F2ZXJN7', 'http://amazon.in/dp/B07L3YNL2V', 'http://amazon.in/dp/B07FHD9Y8M', 'http://amazon.in/dp/B07F31KJXB', 'http://amazon.in/dp/B07L3ZCJ53', 'http://amazon.in/dp/B07FJ7NDGK', 'http://amazon.in/dp/B07M857C6Z', 'http://amazon.in/dp/B088CCYM9D', 'http://amazon.in/dp/B07MQWT396', 'http://amazon.in/dp/B07FHD9PDZ', 'http://amazon.in/dp/B07F7LB4T9', 'http://amazon.in/dp/B074ZCKWSN', 'http://amazon.in/dp/B0811T2HDY', 'http://amazon.in/dp/B08QTWMZPY', 'http://amazon.in/dp/B0811TDGVZ', 'http://amazon.in/dp/B07FJ7W7PH', 'http://amazon.in/dp/B0811TQS47', 'http://amazon.in/dp/B0839HW5GB']
    # start_urls = ['http://amazon.in/dp/B07H8Z4YRX', 'http://amazon.in/dp/B0749TNSBS', 'http://amazon.in/dp/B089H69JCW', 'http://amazon.in/dp/B0839J7LLB', 'http://amazon.in/dp/B079585Q26', 'http://amazon.in/dp/B06WGLB9FY', 'http://amazon.in/dp/B018U1F668', 'http://amazon.in/dp/B00TBJSS0A', 'http://amazon.in/dp/B0756YSR2R', 'http://amazon.in/dp/B00TBJSJV8', 'http://amazon.in/dp/B07F2RZB46', 'http://amazon.in/dp/B0839JT14H', 'http://amazon.in/dp/B07F2Q47ST', 'http://amazon.in/dp/B0811T924L', 'http://amazon.in/dp/B0839J9QRV', 'http://amazon.in/dp/B00TBJSR1A', 'http://amazon.in/dp/B0839JL9R5', 'http://amazon.in/dp/B06XDLHJFJ', 'http://amazon.in/dp/B07F2RV8BD', 'http://amazon.in/dp/B0811TVR7G', 'http://amazon.in/dp/B07F2RZ8TR', 'http://amazon.in/dp/B07C32SZ8L', 'http://amazon.in/dp/B074Z3CF8S', 'http://amazon.in/dp/B01LZKXTRI', 'http://amazon.in/dp/B01GUZC21S', 'http://amazon.in/dp/B07F344NGC', 'http://amazon.in/dp/B07VJNN2CG', 'http://amazon.in/dp/B078PKR7WF', 'http://amazon.in/dp/B07FKWKQ85', 'http://amazon.in/dp/B07CS3238V', 'http://amazon.in/dp/B07FL4M4HV', 'http://amazon.in/dp/B078GQPL14', 'http://amazon.in/dp/B00TBJSJPO', 'http://amazon.in/dp/B00TBJT3L8', 'http://amazon.in/dp/B0839J3QZT', 'http://amazon.in/dp/B07J5NLHWW', 'http://amazon.in/dp/B078GMZ96P', 'http://amazon.in/dp/B0839JC89K', 'http://amazon.in/dp/B00TBJSJM2', 'http://amazon.in/dp/B01LZWP9Q7', 'http://amazon.in/dp/B0839HQDDV', 'http://amazon.in/dp/B07F2Q4B71', 'http://amazon.in/dp/B00U1CDVT4', 'http://amazon.in/dp/B016FYQ2D8', 'http://amazon.in/dp/B0839JDKMC', 'http://amazon.in/dp/B0142R3PY4', 'http://amazon.in/dp/B0105Y4PCO', 'http://amazon.in/dp/B00YBTE0N4', 'http://amazon.in/dp/B0839HYW7B', 'http://amazon.in/dp/B06Y3QTFK3', 'http://amazon.in/dp/B08QVG8B73', 'http://amazon.in/dp/B0839JC8HR', 'http://amazon.in/dp/B0839HYW4V', 'http://amazon.in/dp/B0839J2BKF', 'http://amazon.in/dp/B00U2PPXC8', 'http://amazon.in/dp/B08PDBQ2RQ', 'http://amazon.in/dp/B01GUYOL5O', 'http://amazon.in/dp/B0839J9QX8', 'http://amazon.in/dp/B0839JBFJY', 'http://amazon.in/dp/B0839J69BR', 'http://amazon.in/dp/B0839JDVVZ', 'http://amazon.in/dp/B00AO4E9E0', 'http://amazon.in/dp/B014C5DYDS', 'http://amazon.in/dp/B0839HNNV8', 'http://amazon.in/dp/B0839J5BFL', 'http://amazon.in/dp/B08QV8JDNL', 'http://amazon.in/dp/B0839J6MNP', 'http://amazon.in/dp/B0839HQ4B3', 'http://amazon.in/dp/B0839HM1BS', 'http://amazon.in/dp/B0839K69SX', 'http://amazon.in/dp/B0839HZ2Y9', 'http://amazon.in/dp/B08KHHT2KZ', 'http://amazon.in/dp/B0839J5JVP', 'http://amazon.in/dp/B012U0UNFO', 'http://amazon.in/dp/B0839J695L', 'http://amazon.in/dp/B0839J25PM', 'http://amazon.in/dp/B0839JHJKT', 'http://amazon.in/dp/B0839JC45K', 'http://amazon.in/dp/B01CUD2U5M', 'http://amazon.in/dp/B014NC3E3A']
    # start_urls = ['http://amazon.in/dp/B07G4QSGFH', 'http://amazon.in/dp/B001EVUXY2', 'http://amazon.in/dp/B0839HWZWT', 'http://amazon.in/dp/B01HC2BPZM', 'http://amazon.in/dp/B018J0DDOW', 'http://amazon.in/dp/B0839JMCZF', 'http://amazon.in/dp/B00JEOHITE', 'http://amazon.in/dp/B01G5ZLJEE', 'http://amazon.in/dp/B012U0UZDY', 'http://amazon.in/dp/B0839JL9NK', 'http://amazon.in/dp/B00OPNES4W', 'http://amazon.in/dp/B0199WNJE8', 'http://amazon.in/dp/B00D3LJTQE', 'http://amazon.in/dp/B07FTJDF2S', 'http://amazon.in/dp/B01AM5FAHK', 'http://amazon.in/dp/B07662P4NW', 'http://amazon.in/dp/B0839H7Z8S', 'http://amazon.in/dp/B0839HXT98', 'http://amazon.in/dp/B0839JDW6W', 'http://amazon.in/dp/B0839JMD7R', 'http://amazon.in/dp/B016P6GBB4', 'http://amazon.in/dp/B004Q5M7O2', 'http://amazon.in/dp/B00OQ85N8Q', 'http://amazon.in/dp/B00PATJUOS', 'http://amazon.in/dp/B0073SBEPC', 'http://amazon.in/dp/B00I9OIBRS', 'http://amazon.in/dp/B01NBC40S9', 'http://amazon.in/dp/B00I877BJK', 'http://amazon.in/dp/B012U0WEBA', 'http://amazon.in/dp/B004Q5M7L0', 'http://amazon.in/dp/B003VDGE80', 'http://amazon.in/dp/B00GYB1AQM', 'http://amazon.in/dp/B0839J1T81', 'http://amazon.in/dp/B01BX1NLT6', 'http://amazon.in/dp/B0839HV7XD', 'http://amazon.in/dp/B00TBJSRLA', 'http://amazon.in/dp/B0839JSZNL', 'http://amazon.in/dp/B00P7RGSWK', 'http://amazon.in/dp/B00OQ3C8FM', 'http://amazon.in/dp/B00D9R1OY2', 'http://amazon.in/dp/B01CHNX97I', 'http://amazon.in/dp/B00OQ890AI', 'http://amazon.in/dp/B003F184N6', 'http://amazon.in/dp/B00CQ41JE4', 'http://amazon.in/dp/B07HB4FKZS', 'http://amazon.in/dp/B07HB4L36F', 'http://amazon.in/dp/B07H9SV61Y', 'http://amazon.in/dp/B07HLZDR9S', 'http://amazon.in/dp/B07H9X7WT9', 'http://amazon.in/dp/B07H9T25WH', 'http://amazon.in/dp/B07HMCC4RF', 'http://amazon.in/dp/B07H9YBYSK', 'http://amazon.in/dp/B07HB1YHZP', 'http://amazon.in/dp/B085WKPQZ7', 'http://amazon.in/dp/B00QKAQN3M', 'http://amazon.in/dp/B07HLZDKNN', 'http://amazon.in/dp/B085WJY6NH', 'http://amazon.in/dp/B07H9X7WTG', 'http://amazon.in/dp/B07HMCZJ2P', 'http://amazon.in/dp/B018HGSZO6', 'http://amazon.in/dp/B07H9YCB5L', 'http://amazon.in/dp/B00MUYXORA', 'http://amazon.in/dp/B00CQ416YW', 'http://amazon.in/dp/B017BFNGLG', 'http://amazon.in/dp/B0811TYPM5', 'http://amazon.in/dp/B006T8BXF8', 'http://amazon.in/dp/B01CGETA9Y', 'http://amazon.in/dp/B00IOVOFGW', 'http://amazon.in/dp/B07F4551H9', 'http://amazon.in/dp/B07BDP69GH', 'http://amazon.in/dp/B00UFF6NR4', 'http://amazon.in/dp/B01INE0P6I', 'http://amazon.in/dp/B08377XNND', 'http://amazon.in/dp/B078B5LLBV', 'http://amazon.in/dp/B07J314NP8', 'http://amazon.in/dp/B07NWN452X', 'http://amazon.in/dp/B082XLSR2X', 'http://amazon.in/dp/B00GSGO6OQ', 'http://amazon.in/dp/B0811TXJ26', 'http://amazon.in/dp/B0757317HZ']
    # start_urls = ['http://amazon.in/dp/B06XSC2GYR', 'http://amazon.in/dp/B075766WW1', 'http://amazon.in/dp/B0839PMTP3', 'http://amazon.in/dp/B00UFF6WSY', 'http://amazon.in/dp/B07BDQ5G1L', 'http://amazon.in/dp/B085WKPQZ8', 'http://amazon.in/dp/B06Y5T7TMJ', 'http://amazon.in/dp/B00XHRR3FI', 'http://amazon.in/dp/B06XRX1S56', 'http://amazon.in/dp/B00BU1FYUO', 'http://amazon.in/dp/B01DP01I7A', 'http://amazon.in/dp/B00CQ417NM', 'http://amazon.in/dp/B07XTM81NS', 'http://amazon.in/dp/B095C9DZTG', 'http://amazon.in/dp/B00OJ2B9AU', 'http://amazon.in/dp/B000GCY224', 'http://amazon.in/dp/B071P13PSJ', 'http://amazon.in/dp/B01BGSDWKO', 'http://amazon.in/dp/B01MA6CBRC', 'http://amazon.in/dp/B00Y9M46AA', 'http://amazon.in/dp/B095C8VJZ4', 'http://amazon.in/dp/B0839PY7SR', 'http://amazon.in/dp/B0839HH1NH', 'http://amazon.in/dp/B00LM6ASRQ', 'http://amazon.in/dp/B0839HRX8C', 'http://amazon.in/dp/B075TGTP17', 'http://amazon.in/dp/B01MXX6IC8', 'http://amazon.in/dp/B095C8S456', 'http://amazon.in/dp/B095C8MWRP', 'http://amazon.in/dp/B0839HXSZ8', 'http://amazon.in/dp/B01MRVZQ0F', 'http://amazon.in/dp/B095C95CM6', 'http://amazon.in/dp/B073RHPWF9', 'http://amazon.in/dp/B095C94LKP', 'http://amazon.in/dp/B0811TGMRZ', 'http://amazon.in/dp/B000RK9XLA', 'http://amazon.in/dp/B0839J5JKP', 'http://amazon.in/dp/B08X4TCWJD', 'http://amazon.in/dp/B000JBY3CG', 'http://amazon.in/dp/B071XQ8LR2', 'http://amazon.in/dp/B00JVBGX8C', 'http://amazon.in/dp/B08398V93H', 'http://amazon.in/dp/B0839912XQ', 'http://amazon.in/dp/B00EK0BH9Y', 'http://amazon.in/dp/B07W1RYDDT', 'http://amazon.in/dp/B01N49E07T', 'http://amazon.in/dp/B07BHYB44L', 'http://amazon.in/dp/B0839JL9G6', 'http://amazon.in/dp/B08399PQ3J', 'http://amazon.in/dp/B08399CNJT', 'http://amazon.in/dp/B01N1NRJVZ', 'http://amazon.in/dp/B00OZG2RPG', 'http://amazon.in/dp/B00FQR4JOK', 'http://amazon.in/dp/B08398YNKF', 'http://amazon.in/dp/B000RYYI7K', 'http://amazon.in/dp/B07FKF8J7V', 'http://amazon.in/dp/B0839JHJBW', 'http://amazon.in/dp/B08399NC37', 'http://amazon.in/dp/B00JOLRYXW', 'http://amazon.in/dp/B01MXTOD3A', 'http://amazon.in/dp/B00JGQ2R1Y', 'http://amazon.in/dp/B0839HMC39', 'http://amazon.in/dp/B01MRW052J', 'http://amazon.in/dp/B004DBXKS6', 'http://amazon.in/dp/B083991L8X', 'http://amazon.in/dp/B07G1D17TY', 'http://amazon.in/dp/B01MEENE3N', 'http://amazon.in/dp/B00CHHKN3S', 'http://amazon.in/dp/B00CHHJQOU', 'http://amazon.in/dp/B01BMQ2BLQ', 'http://amazon.in/dp/B00NH74FAE', 'http://amazon.in/dp/B006T8BWUE', 'http://amazon.in/dp/B00JVBJ2EE', 'http://amazon.in/dp/B00AVWJROM', 'http://amazon.in/dp/B00CTSYIWM', 'http://amazon.in/dp/B001ET7ERS', 'http://amazon.in/dp/B06XG4YCK6', 'http://amazon.in/dp/B00JFLDMZU', 'http://amazon.in/dp/B095C7TWZ5', 'http://amazon.in/dp/B0839HLKFN', 'http://amazon.in/dp/B078FBR95Z']
    start_urls = ["http://amazon.in/dp/B015Z96HQ6"]
    # start_urls = ['http://amazon.in/dp/B07L3ZCJ53', 'http://amazon.in/dp/B07L3YNL2V', 'http://amazon.in/dp/B08T2Y2Q4T', 'http://amazon.in/dp/B08CSHBPD5', 'http://amazon.in/dp/B07H9SV624', 'http://amazon.in/dp/B07HB4FKZS', 'http://amazon.in/dp/B00ENZRCBI', 'http://amazon.in/dp/B00JS3PICK', 'http://amazon.in/dp/B07YWMQWWK', 'http://amazon.in/dp/B07YWMQRNJ']

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

    def parse(self, response):
        items = AmazonProductScrapingItem()
        title = self.get_title(response)
        brand = self.get_brand(response)
        sale_price = self.get_sale_price(response)
        offers = self.get_offers(response)
        original_price = self.get_original_price(response)
        fullfilled = self.get_fullfilled(response)
        rating = self.get_rating(response)
        total_reviews = self.get_total_reviews(response)
        availability = self.get_availability(response)
        category = self.get_category(response)
        icons = self.get_icons(response)
        best_seller_rank = self.get_best_seller_rank(response)
        product_details = self.get_product_details(response)
        asin = self.get_asin(response)
        important_information = self.get_important_information(response)
        product_description = self.get_product_description(response)
        bought_together = self.get_bought_together(response)
        subscription_discount = self.get_subscription_discount(response)
        variations = self.get_variations(response)

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
