import datetime
import requests
import sqlite3
import os

class Finance:
    def __init__(self):
        # Łączymy się z bazą danych i blokujemy otwieranie bazy danych w folderze gui
        db_path = os.path.join(os.path.dirname(__file__), "../transactions.db")
        self.connection = sqlite3.connect(db_path)

        # Tworzymy cursor
        self.cursor = self.connection.cursor()

        # Tworzymy bazę danych na transakcje
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            amount REAl,
            date TEXT,
            type TEXT,
            category TEXT,
            currency_code TEXT,
            exchange_rate REAL)
            """)

        # Tworzymy bazę danych na waluty
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
            currency_code TEXT PRIMARY KEY,
            exchange_rate REAL)
            """)

        # Dodajemy podstawowe waluty
        self.initialize_currencies()

        # Aktualizujemy kursy walut
        self.update_exchange_rates()

    # Funkcja pobierająca aktualny kurs walut poprzez exchangerate-api.com, który jest następnie aktutalizowany
    def update_exchange_rates(self):
        # Ustawiamy adres url do pobrania kursu walut
        url = "https://v6.exchangerate-api.com/v6/e1336ab92ccda65437b1b7d0/latest/PLN"

        # Wysyłamy prośbe do adresu url
        response = requests.get(url)
        # Sprawdzamy czy wszystko poprawanie działa
        if response.status_code == 200:
            exchange_rates = response.json()
        else:
            print(f"Error: {response.status_code}")
        # Aktualizujemy kursy walut
        self.cursor.execute(
            """UPDATE currencies SET exchange_rate = ? WHERE currency_code = ?""",
            (1 / exchange_rates["conversion_rates"]["EUR"], "EUR")
        )
        self.cursor.execute(
            """UPDATE currencies SET exchange_rate = ? WHERE currency_code = ?""",
            (1 / exchange_rates["conversion_rates"]["USD"], "USD")
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja dodająca podstawowe waluty
    def initialize_currencies(self):
        # Dodajemy walutę, tylko jeśli nie istnieje
        self.cursor.execute(
            """INSERT OR IGNORE INTO currencies (currency_code, exchange_rate) VALUES (?, ?)""",
            ("PLN", 1.0)
        )
        self.cursor.execute(
            """INSERT OR IGNORE INTO currencies (currency_code, exchange_rate) VALUES (?, ?)""",
            ("EUR", 4.32)
        )
        self.cursor.execute(
            """INSERT OR IGNORE INTO currencies (currency_code, exchange_rate) VALUES (?, ?)""",
            ("USD", 3.79)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja dodająca transakcje
    def add_transaction(self, amount, date, type, category, currency_code, exchange_rate):
        # Zapisujemy transakcję wraz z jej parametrami
        self.cursor.execute(
            """INSERT INTO transactions (amount, date, type, category, currency_code, exchange_rate) VALUES (?, ?, ?, ?, ?, ?)""",
            (amount, date, type, category, currency_code, exchange_rate)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja zwracająca aktualne saldo
    def return_balance(self):
        # Wyciągamy sumę z wszystkich transakcji
        self.cursor.execute(
                """SELECT SUM(amount) FROM transactions"""
        )
        balance = self.cursor.fetchone()
        if balance[0] is None:
            balance = 0
        else:
            balance = balance[0]
        return balance

    # Funkcja zwracająca sumę przychodów, za aktualny miesiąc
    def return_income(self):
        # Zapisujemy dzisiejszy miesiąc i rok
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        month = str(month)
        # Korzystamy z funkcji .zfill(x) aby dodać zera z lewej strony, co ma na celu zwiększenie długości zmiennej
        month = month.zfill(2)
        year = str(year)

        # Wyciągamy sumę z wszystkich przychodów
        self.cursor.execute(
            """SELECT SUM(amount) FROM transactions WHERE type = ? and strftime('%m', date) = ? AND strftime('%Y', date) = ?""",
            ("income", month, year)
        )
        income = self.cursor.fetchone()
        if income[0] is None:
            income = 0
        else:
            income = income[0]
        return income

    # Funkcja zwracająca sumę wydatków, za aktualny miesiąc
    def return_expense(self):
        # Zapisujemy dzisiejszy miesiąc i rok
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        month = str(month)
        # Korzystamy z funkcji .zfill(x) aby dodać zera z lewej strony, co ma na celu zwiększenie długości zmiennej
        month = month.zfill(2)
        year = str(year)

        # Wyciągamy sumę z wszystkich przychodów
        self.cursor.execute(
            """SELECT SUM(amount) FROM transactions WHERE type = ? and strftime('%m', date) = ? AND strftime('%Y', date) = ?""",
            ("expense", month, year)
        )
        expense = self.cursor.fetchone()
        if expense[0] is None:
            expense = 0
        else:
            expense = expense[0]
        # Wyciągamy wartośc bezwzględną z kwoty wydatków, aby wyświetlała się poprawnie na dashboardzie
        expense = abs(expense)
        return expense

    # Funkcja wypisująca historię transakcji
    def show_history(self, category=None, type=None):
        # Korzystamy z sortowania wbudowanego w sqlite3
        if category is not None and type is not None:
            self.cursor.execute(
                """SELECT * FROM transactions WHERE category = ? AND type = ? ORDER BY id DESC""",
                (category, type,)
            )
        elif category is not None:
            self.cursor.execute(
                """SELECT * FROM transactions WHERE category = ? ORDER BY id DESC""",
                (category,)
            )
        elif type is not None:
            self.cursor.execute(
                """SELECT * FROM transactions WHERE type = ? ORDER BY id DESC""",
                (type,)
            )
        else:
            self.cursor.execute(
                """SELECT * FROM transactions ORDER BY id DESC"""
            )
        transactions = self.cursor.fetchall()
        return transactions

    # Funkcja wypisująca 10 ostatnich transakcji
    def show_recent_history(self):
        # Wybieramy 10 ostatnich transakcji
        self.cursor.execute(
            """SELECT * FROM transactions ORDER BY id desc LIMIT 10""")
        recent_transactions = self.cursor.fetchall()
        return recent_transactions

    # Funkcja wypisująca wszystkie kody walut
    def get_currencies(self):
        # Wybieramy wszystko z kolumny currency_code
        self.cursor.execute("""SELECT currency_code FROM currencies""")
        # Wysuwamy PLN na samą górę
        self.cursor.execute(
            """SELECT currency_code FROM currencies ORDER BY currency_code = 'PLN' DESC"""
        )
        # Zwracamy kody walut
        return self.cursor.fetchall()

    # Funkcja pobiera kurs dla danego kodu waluty
    def get_exchange_rate(self, currency_code):
        # Wyciągamy kurs dla wybrengo kodu waluty
        self.cursor.execute(
        """SELECT exchange_rate FROM currencies WHERE currency_code = ?""",
            (currency_code,)
        )
        exchange_rate = self.cursor.fetchone()
        # Zwracamy kurs
        return exchange_rate[0]

    # Funkcja umożliwiająca edycję transakcji
    def edit_transaction(self, id, amount=None, date=None, type=None, category=None, currency_code=None, exchange_rate=None):
        # Sprawdzamy które zmienne dostała funkcja, a następnie jeśli istnieją, aktualizujemy je
        if amount is not None:
            self.cursor.execute(
                """UPDATE transactions
                SET amount = ?
                WHERE id = ?""",
                (amount, id)
            )
        if date is not None:
            self.cursor.execute(
                """UPDATE transactions
                SET date = ?
                WHERE id = ?""",
                (date, id)
            )
        if type is not None:
            self.cursor.execute(
                """UPDATE transactions
                SET type = ?
                WHERE id = ?""",
                (type, id)
            )
        if category is not None:
            self.cursor.execute(
                """UPDATE transactions
                SET category = ?
                WHERE id = ?""",
                (category, id)
            )
        if currency_code is not None:
            self.cursor.execute(
                """UPDATE transactions
                SET currency_code = ?
                WHERE id = ?""",
                (currency_code, id)
            )
        if exchange_rate is not None:
            self.cursor.execute(
                """UPDATE transactions
                SET exchange_rate = ?
                WHERE id = ?""",
                (exchange_rate, id)
            )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja umożliwiająca usunięcie transakcji
    def delete_transaction(self, id):
        # Usuwamy transakcja o id które otrzymała funkcja
        self.cursor.execute(
            """DELETE FROM transactions WHERE id = ?""",
            (id,)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()