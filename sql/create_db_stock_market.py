import sqlite3
import random
from faker import Faker

def create_db_stock_market():

    # Create a connection to a SQLite database
    conn = sqlite3.connect('databases/stock_market.db')
    cur = conn.cursor()

    # Create the tables
    cur.execute("""
    CREATE TABLE Companies(
        company_id INTEGER PRIMARY KEY,
        company_name TEXT,
        sector TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE Stocks(
        stock_id INTEGER PRIMARY KEY,
        company_id INTEGER,
        ticker_symbol TEXT,
        price REAL,
        market_cap REAL,
        FOREIGN KEY(company_id) REFERENCES Companies(company_id)
    );
    """)

    cur.execute("""
    CREATE TABLE Transactions(
        transaction_id INTEGER PRIMARY KEY,
        stock_id INTEGER,
        quantity INTEGER,
        transaction_type TEXT,
        transaction_date TEXT,
        FOREIGN KEY(stock_id) REFERENCES Stocks(stock_id)
    );
    """)

    # Generate random data and load it into the tables
    faker = Faker()
    sectors = ['Tech', 'Finance', 'Healthcare', 'Energy', 'Consumer Goods']
    transaction_types = ['BUY', 'SELL']

    # Generate a list of market caps
    market_caps = sorted([random.uniform(1000000000, 1000000000000) for _ in range(10)], reverse=True)

    for i in range(10):
        company_name = faker.company()
        sector = random.choice(sectors)
        cur.execute(f"INSERT INTO Companies (company_name, sector) VALUES ('{company_name}', '{sector}');")

        # Assign market cap to stock
        ticker_symbol = faker.lexify(text="???")
        price = random.uniform(10, 1000)
        market_cap = market_caps[i]
        cur.execute(f"INSERT INTO Stocks (company_id, ticker_symbol, price, market_cap) VALUES ({i}, '{ticker_symbol}', {price}, {market_cap});")

        for _ in range(10):  # Assuming there are 10 transactions for each stock
            quantity = random.randint(1, 100)
            transaction_type = random.choice(transaction_types)
            transaction_date = faker.date_between(start_date='-1y', end_date='today')
            cur.execute(f"INSERT INTO Transactions (stock_id, quantity, transaction_type, transaction_date) VALUES ({i}, {quantity}, '{transaction_type}', '{transaction_date}');")

    # Commit changes and close connection
    conn.commit()
    conn.close()


create_db_stock_market()