import requests
from bs4 import BeautifulSoup
from data import create_table, insert_data


class LaptopScraper:
    def __init__(self, brand):
        self.brand = brand.strip().lower()
        self.base_url = f'https://mudita.com.np/laptops-nepal/by-brand/{self.brand}-laptops-nepal.html'
        self.headers = {
            'User-Agent': 'python-requests/2.32.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        self.product_list = []