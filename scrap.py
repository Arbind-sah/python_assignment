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

        
    def get_response(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            print(f'Failed to retrieve data for {self.brand} brand. Status code: {response.status_code}')
            return None
        else:
            return response

    def parse_product_details(self, product):
        product_name = product.find('a', class_='product-item-link')
        product_name = product_name.text.strip()[0:100] if product_name else 'Not available'

        product_old_price = product.find('span', class_='old-price')
        product_old_price = product_old_price.text.strip() if product_old_price else 'Not available'

        offer = product.find('div', class_='sale-badge')
        offer = offer.text.strip()[4:9] if offer else 'No offer'

        product_new_price = product.find('span', class_='price')
        product_new_price = product_new_price.text.strip() if product_new_price else 'Not available'

        product_details_link = product.find('a', class_='product-item-link', href=True)
        product_details_link = product_details_link['href'] if product_details_link else 'Not available'

        return {
            'name': product_name,
            'original_price': product_old_price,
            'offer': offer,
            'new_price': product_new_price,
            'details_link': product_details_link
        }
    
    def fetch_products(self):
        response = self.get_response()
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='product details product-item-details')

            if not products:
                print(f'Sorry, {self.brand} brand is not available')
                return

            for product in products:
                product_details = self.parse_product_details(product)
                self.product_list.append(product_details)

    def display_products(self):
        if not self.product_list:
            print(f'No products found for {self.brand} brand.')
            return

        print(f'{self.brand} brand products are:')
        for product in self.product_list:
            print(product)
            print('\n')


    def save_products_to_db(self):
        create_table()
        insert_data(self.product_list)


if __name__ == '__main__':
    while True:
        search_term = input('Enter the brand name you want to search:\n').strip()
        if search_term:
            break
        else:
            print('Please enter a valid brand name')

    scraper = LaptopScraper(search_term)
    scraper.fetch_products()
    scraper.display_products()
    scraper.save_products_to_db()