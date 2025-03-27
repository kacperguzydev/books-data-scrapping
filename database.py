import sqlite3
from datetime import datetime
import logging
from config import DATABASE_NAME

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_book_data(link, name, price):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    date_scraped = datetime.now().strftime('%Y-%m-%d')

    cursor.execute('''
        SELECT COUNT(*) FROM books WHERE link = ? AND date = ?
    ''', (link, date_scraped))

    if cursor.fetchone()[0] > 0:
        logging.info(f"Record with link {link} and date {date_scraped} already exists. Skipping insertion.")
    else:
        cursor.execute('''
            INSERT INTO books (link, name, price, date)
            VALUES (?, ?, ?, ?)
        ''', (link, name, price, date_scraped))
        logging.info(f"Inserted record with link {link} and date {date_scraped}.")

    conn.commit()
    conn.close()

def print_books():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    print("=" * 100)

    for row in rows:
        print(f'id: {row[0]}')
        print(f'link: {row[1]}')
        print(f'name: {row[2]}')
        print(f'price: {row[3]}')
        print(f'date: {row[4]}')
        print("=" * 100)

    conn.close()