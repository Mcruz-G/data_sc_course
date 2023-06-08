import sqlite3
import random

def create_db_stock_market():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect('finance_database.db')
    cursor = conn.cursor()

    # Create the tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            company TEXT,
            price REAL,
            quantity INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            stock_id INTEGER,
            date TEXT,
            type TEXT,
            price REAL,
            quantity INTEGER,
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
        )
    ''')

    # Generate random data for the stocks table
    stocks = [
        ('AAPL', 'Apple Inc.', 150.23, 100),
        ('GOOGL', 'Alphabet Inc.', 2300.45, 50),
        ('MSFT', 'Microsoft Corporation', 250.67, 75),
        ('AMZN', 'Amazon.com, Inc.', 3500.12, 25),
        ('TSLA', 'Tesla, Inc.', 600.34, 40)
    ]

    cursor.executemany('INSERT INTO stocks (symbol, company, price, quantity) VALUES (?, ?, ?, ?)', stocks)

    # Generate random data for the transactions table
    transaction_types = ['Buy', 'Sell']

    for stock_id in range(1, len(stocks) + 1):
        for _ in range(5):
            date = f'2023-06-{random.randint(1, 30):02d}'
            transaction_type = random.choice(transaction_types)
            price = random.uniform(0.8, 1.2) * stocks[stock_id - 1][2]  # Random variation in price
            quantity = random.randint(5, 20)
            
            cursor.execute('INSERT INTO transactions (stock_id, date, type, price, quantity) VALUES (?, ?, ?, ?, ?)',
                        (stock_id, date, transaction_type, price, quantity))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

