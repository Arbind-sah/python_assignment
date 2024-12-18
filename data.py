import sqlite3

def create_table():
    conn = sqlite3.connect('laptop.db')
    c = conn.cursor()

    # Create table if it does not exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS laptop_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            original_price TEXT,
            offer TEXT,
            new_price TEXT,
            details_link TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(product_list):
    conn = sqlite3.connect('laptop.db')
    c = conn.cursor()

    for product in product_list:
        # Check if the product already exists
        check = c.execute('SELECT * FROM laptop_list WHERE name = ?', (product['name'],)).fetchone()
        if check:
            print(f'Data already exists')
            continue

        c.execute('''
            INSERT INTO laptop_list (name, original_price, offer, new_price, details_link)
            VALUES (?, ?, ?, ?, ?)
        ''', (product['name'], product['original_price'], product['offer'], product['new_price'], product['details_link']))


        print(f'Data inserted successfully for product: {product["name"]}')

    conn.commit()
    conn.close()