import requests
from bs4 import BeautifulSoup
from data import create_table, insert_data, create_user_table, insert_user, validate_user
import hashlib


class LaptopScraper:
    def __init__(self, brand):
        self.brand = brand.strip().lower()
        if self.brand in ['apple', 'mac', 'mac-book']:
            self.base_url = 'https://mudita.com.np/laptops-nepal/by-brand/apple-macbook-nepal.html'
        else:
            self.base_url = f'https://mudita.com.np/laptops-nepal/by-brand/{self.brand}-laptops-nepal.html'
        self.headers = {
            'User-Agent': 'python-requests/2.32.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        self.product_list = []

    def get_response(self):
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None

    def parse_product_details(self, product):
        try:
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
        except AttributeError as e:
            print(f"Error parsing product details: {e}")
            return None

    def fetch_products(self):
        response = self.get_response()
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='product details product-item-details')
            if not products:
                print(f'Sorry, {self.brand} brand is not available\n')
                return
            for product in products:
                product_details = self.parse_product_details(product)
                if product_details:
                    self.product_list.append(product_details)

    def save_products_to_db(self):
        create_table()
        insert_data(self.product_list)

    def display_products(self):
        print(f'{self.brand.capitalize()} Laptops:\n')
        for product in self.product_list:
            print(f'Name: {product["name"]}')
            print(f'Original Price: {product["original_price"]}')
            print(f'Offer: {product["offer"]}')
            print(f'New Price: {product["new_price"]}')
            print(f'Details Link: {product["details_link"]}\n')


def register_user():
    create_user_table()
    username = input('Enter username: ').strip()
    email = input('Enter email: ').strip()
    password = input('Enter password: ').strip()
    phone = input('Enter phone number: ').strip()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    insert_user(username, hashed_password, email, phone)


def login_user():
    username = input('Enter username: ').strip()
    password = input('Enter password: ').strip()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if validate_user(username, hashed_password):
        print(f'Welcome back, {username}!\n')
        return True
    else:
        print('User not found ! Plz register first.\n')
        return False


if __name__ == '__main__':
    create_user_table()
    print('Welcome to Laptop Scraper!\n')
    username = input("Enter username:\n")
    password = input("Enter password:\n")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if validate_user(username, hashed_password):
        print(f'Welcome back, {username}!\n')
    else:
        print('User not found! Please register first.\n')
        register_user()
        

    while True:
        brand = input('Enter the brand of laptop you want to search: ')
        print('Processing your request, please wait...')
        scraper = LaptopScraper(brand)
        scraper.fetch_products()
        scraper.save_products_to_db()
        scraper.display_products()
        choice = input('Do you want to search for another brand? (y/n): ')
        if choice.lower() != 'y':
            break
    print('exiting...')
    print('Thank you for using Laptop Scraper!')
