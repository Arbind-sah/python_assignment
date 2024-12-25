import sqlite3
import hashlib
import os

# Helper functions for hashing and validating passwords
def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()  # Generate a random salt
    salted_password = salt + password
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed, salt

def verify_password(password, salt, hashed_password):
    return hash_password(password, salt)[0] == hashed_password

# Laptop database operations
def create_table():
    conn = sqlite3.connect('laptop.db')
    c = conn.cursor()
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
        check = c.execute('SELECT * FROM laptop_list WHERE name = ?', (product['name'],)).fetchone()
        if check:
            print(f'Data already exists for product: {product["name"]}')
            continue
        c.execute('''
            INSERT INTO laptop_list (name, original_price, offer, new_price, details_link)
            VALUES (?, ?, ?, ?, ?)
        ''', (product['name'], product['original_price'], product['offer'], product['new_price'], product['details_link']))
        print(f'Data inserted successfully for product: {product["name"]}')
    conn.commit()
    conn.close()

# User database operations
def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            salt TEXT,
            email TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(username, password, email, phone):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password, salt = hash_password(password)
    try:
        c.execute('''
            INSERT INTO users (username, password, salt, email, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, hashed_password, salt, email, phone))
        print(f'User {username} registered successfully.')
    except sqlite3.IntegrityError:
        print(f'Username {username} already exists.')
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password, salt FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    if user:
        stored_password, salt = user
        return verify_password(password, salt, stored_password)
    return False
