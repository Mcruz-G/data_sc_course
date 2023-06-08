import sqlite3
from faker import Faker
import random
import os
import string
from datetime import datetime

def create_db_sqlite():
    if not os.path.exists(os.curdir + 'databases/Retail.db'):
        conn = sqlite3.connect('databases/Retail.db')
        c = conn.cursor()

        # Create customers table
        c.execute('''
                CREATE TABLE customers
                (id INTEGER PRIMARY KEY, name TEXT, address TEXT, city TEXT)
                ''')

        # Create products table
        c.execute('''
                CREATE TABLE products
                (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)
                ''')

        # Create sales table
        c.execute('''
                CREATE TABLE sales
                (sale_id INTEGER PRIMARY KEY, product_id INTEGER, customer_id INTEGER, quantity INTEGER, sale_date TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(customer_id) REFERENCES customers(id))
                ''')

        conn.commit()

        # Generating fake data and inserting it into the tables
        fake = Faker()

        # Inserting data into customers table
        for _ in range(1000):
            c.execute("INSERT INTO customers (name, address, city) VALUES (?, ?, ?)",
                    (fake.name(), fake.address().replace('\n', ', '), fake.city()))

        # Inserting data into products table
        categories = ['Electronics', 'Fashion', 'Groceries', 'Health', 'Books', 'Toys', 'Tools', 'Kitchen']
        for _ in range(1000):
            c.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                    (fake.bs(), random.choice(categories), round(random.uniform(10.5, 200.5), 2)))

        conn.commit()

        # Get customer ids and product ids for creating sales data
        c.execute("SELECT id FROM customers")
        customer_ids = [cid[0] for cid in c.fetchall()]

        c.execute("SELECT id FROM products")
        product_ids = [pid[0] for pid in c.fetchall()]

        # Inserting data into sales table
        for _ in range(5000):
            c.execute("INSERT INTO sales (product_id, customer_id, quantity, sale_date) VALUES (?, ?, ?, ?)",
                    (random.choice(product_ids), random.choice(customer_ids), random.randint(1, 5), fake.date_this_decade().isoformat()))

        conn.commit()

        # Close the connection
        conn.close()

# Create the SQLite database and tables
create_db_sqlite()
