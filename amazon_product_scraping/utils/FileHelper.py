import pandas as pd

class FileHelper:

	def get_urls(file):
		df = pd.read_csv(file)
		urls = df['URL']
		return list(urls)