import mysql.connector
from faker import Faker
import random

DB_USERNAME = "rakesh"
DB_PASSWORD = "rakesh"

fake = Faker()

def generate_random_book():
    return {
        "title": fake.catch_phrase(),
        "author": fake.name(),
        "publication_year": random.randint(1800, 2023),
    }

def create_books_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            publication_year INT
        )
    """)

def insert_random_books(num_books):
    try:
        conn = mysql.connector.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host="localhost",
            database="library",
        )

        cursor = conn.cursor()

        create_books_table(cursor)

        for _ in range(num_books):
            book = generate_random_book()
            cursor.execute(
                "INSERT INTO books (title, author, publication_year) VALUES (%s, %s, %s)",
                (book["title"], book["author"], book["publication_year"]),
            )

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    num_books_to_insert = 10
    insert_random_books(num_books_to_insert)
