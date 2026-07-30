import datetime
import calendar
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
            category TEXT,
            last_added TEXT,
            currency_code TEXT,
            exchange_rate REAL)
            """)

    # Funkcja dodająca cyklicznę transakcję
    def add_recurring_transaction(self, amount, day, type, category, curency_code, exchange_rate):
        # Zapisujemy transakcję wraz z jej parametrami
        self.cursor.execute(
            """INSERT INTO recurring_transactions (amount, day, type, category, last_added, currency_code, exchange_rate) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (amount, day, type, category, None, curency_code, exchange_rate)
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

    # Funkcja, która sprawdza, czy w dzisiejszym dniu są do dodania jakieś stałe transakcje
    def process_recurring_transaction(self):
        # Zapisujemy dzisiejszy dzień, miesiąc i rok
        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        # Zapisujemy wszystkie transakcje
        recurring_transactions = self.show_recurring_history()

        for recurring_transaction in recurring_transactions:
            # Zapisujemy do zmiennej ilość dni aktualnego miesiąca
            number_of_days = calendar.monthrange(year, month)[1]
            # Dodajemy transakcję, jeśli dzień się zgadza, albo jeśli dzień transakcji jest większy niż liczba dni w miesiącu i dziś jest ostatni dzień miesiąca.
            if (int(recurring_transaction[2]) == day or (int(recurring_transaction[2]) > number_of_days and day == number_of_days)) and (recurring_transaction[5] != str(datetime.date.today())):
                # Zapisujemy transakcję wraz z jej parametrami
                self.cursor.execute(
                    """INSERT INTO transactions (amount, date, type, category, currency_code, exchange_rate) VALUES (?, ?, ?, ?, ?, ?)""",
                    (recurring_transaction[1], str(datetime.date.today()), recurring_transaction[3], recurring_transaction[4], recurring_transaction[6], recurring_transaction[7])
                )
                # Aktualizujemy datę ostatniego dodania transakcji
                self.cursor.execute(
                    """UPDATE recurring_transactions set last_added = ? WHERE id = ?""",
                    (str(datetime.date.today()), recurring_transaction[0])
                )
                # Zapisujemy zmiany i kończymy połączenie
                self.connection.commit()

    # Funkcja umożliwiająca edycję cyklicznej transakcji
    def edit_recurring_transaction(self, id, amount=None, day=None, type=None, category=None, currency_code=None, exchange_rate=None):
        # Sprawdzamy które zmienne dostała funkcja, a następnie jeśli istnieją, aktualizujemy je
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
        if currency_code is not None:
            self.cursor.execute(
                """UPDATE recurring_transactions
                SET currency_code = ?
                WHERE id = ?""",
                (currency_code, id)
            )
        if exchange_rate is not None:
            self.cursor.execute(
                """UPDATE recurring_transactions
                SET exchange_rate = ?
                WHERE id = ?""",
                (exchange_rate, id)
            )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

        # Funkcja umożliwiająca usunięcie cyklicznej transakcji
        def delete_recurring_transaction(self, id):
            # Usuwamy transakcja o id które otrzymała funkcja
            self.cursor.execute(
                """DELETE FROM recurring_transactions WHERE id = ?""",
                (id,)
            )
            # Zapisujemy zmiany i kończymy połączenie
            self.connection.commit()