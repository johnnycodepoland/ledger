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
    def add_recurring_transaction(self, amount, day, type, category):
        # Zapisujemy transakcję wraz z jej parametrami
        self.cursor.execute(
            """INSERT INTO recurring_transactions (amount, day, type, category) VALUES (?, ?, ?, ?)""",
            (amount, day, type, category)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja wypisująca wszystkie cykliczne transakcje
    def show_recurring_history(self, category=None, type=None):
        # Korzystamy z sortowania wbudowanego w sqlite3
        if category is not None and type is not None:
            self.cursor.execute(
                """SELECT * FROM recurring_transactions WHERE category = ? AND type = ?""",
                (category, type,)
            )
        elif category is not None:
            self.cursor.execute(
                """SELECT * FROM recurring_transactions WHERE category = ?""",
                (category,)
            )
        elif type is not None:
            self.cursor.execute(
                """SELECT * FROM recurring_transactions WHERE type = ?""",
                (type,)
            )
        else:
            self.cursor.execute(
                """SELECT * FROM recurring_transactions"""
            )
        transactions = self.cursor.fetchall()
        return transactions

    # Funkcja umożliwiająca usunięcie cyklicznej transakcji
    def delete_recurring_transaction(self, id):
        self.cursor.execute(
            """DELETE FROM recurring_transactions WHERE id = ?""",
            (id,)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    def process_recurring_transaction(self):
        # Zapisujemy dzisiejszy dzień
        day = datetime.datetime.now().day
        # Zapisujemy wszystkie transakcje
        transactions = self.show_recurring_history()

        for transaction in transactions:
            # Sprawdzamym czy dzisiejszy dzień zgadza się z dniem cyklicznej transakcji
            if transaction[2] == day:
                # Zapisujemy transakcję wraz z jej parametrami
                self.cursor.execute(
                    """INSERT INTO transactions (amount, date, type, category) VALUES (?, ?, ?, ?)""",
                    (transaction[1], str(datetime.date.today()), transaction[3], transaction[4])
                )
                # Zapisujemy zmiany i kończymy połączenie
                self.connection.commit()

    # Funkcja umożliwiająca edycję cyklicznej transakcji
    def edit_recurring_transaction(self, id, amount=None, day=None, type=None, category=None):
        if amount is not None:
            self.cursor.execute(
                """UPDATE recurring_transactions
                SET amount = ?
                WHERE id = ?""",
                (amount, id)
            )
        if day is not None:
            self.cursor.execute(
                """UPDATE recurring_transactions
                SET day = ?
                WHERE id = ?""",
                (day, id)
            )
        if type is not None:
            self.cursor.execute(
                """UPDATE recurring_transactions
                SET type = ?
                WHERE id = ?""",
                (type, id)
            )
        if category is not None:
            self.cursor.execute(
                """UPDATE recurring_transactions
                SET category = ?
                WHERE id = ?""",
                (category, id)
            )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()