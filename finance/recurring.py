import datetime
import sqlite3
import os

class Recurring:
    def __init__(self):
        # Łączymy się z bazą danych i blokujemy otwieranie bazy danych w folderze gui
        db_path = os.path.join(os.path.dirname(__file__), "../transactions.db")
        self.connection = sqlite3.connect(db_path)

        # Tworzymy cursor
        self.cursor = self.connection.cursor()

        # Tworzymy bazę danych
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recurring_transactions (
            id INTEGER PRIMARY KEY,
            amount REAl,
            day INTEGER,
            type TEXT,
            category TEXT)
            """)

    # Funkcja dodająca cyklicznę transakcję
    def add_transaction(self, amount, day, type, category):
        # Zapisujemy transakcję wraz z jej parametrami
        self.cursor.execute(
            """INSERT INTO recurring_transactions (amount, day, type, category) VALUES (?, ?, ?, ?)""",
            (amount, day, type, category)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()