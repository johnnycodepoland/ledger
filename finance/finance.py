import datetime
import sqlite3
import os

class Finance:
    def __init__(self):
        # Łączymy się z bazą danych i blokujemy otwieranie bazy danych w folderze gui
        db_path = os.path.join(os.path.dirname(__file__), "../transactions.db")
        self.connection = sqlite3.connect(db_path)

        # Tworzymy cursor
        self.cursor = self.connection.cursor()

        # Tworzymy bazę danych
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            amount REAl,
            date TEXT,
            type TEXT,
            category TEXT)
            """)

    # Funkcja dodająca transakcje
    def add_transaction(self, amount, date, type, category):
        # Zapisujemy transakcję wraz z jej parametrami
        self.cursor.execute(
            """INSERT INTO transactions (amount, date, type, category) VALUES (?, ?, ?, ?)""",
            (amount, date, type, category)
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
                """SELECT * FROM transactions WHERE category = ? AND type = ?""",
                (category, type,)
            )
        elif category is not None:
            self.cursor.execute(
                """SELECT * FROM transactions WHERE category = ?""",
                (category,)
            )
        elif type is not None:
            self.cursor.execute(
                """SELECT * FROM transactions WHERE type = ?""",
                (type,)
            )
        else:
            self.cursor.execute(
                """SELECT * FROM transactions"""
            )
        transactions = self.cursor.fetchall()
        return transactions

    # Funkcja umożliwiająca edycję transakcji
    def edit_transaction(self, id, amount=None, date=None, type=None, category=None):
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
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja umożliwiająca usunięcie transakcji
    def delete_transaction(self, id):
        self.cursor.execute(
            """DELETE FROM transactions WHERE id = ?""",
            (id,)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja podsumowująca dany miesiąc transakcji
    def monthly_summary(self, month, year):
        month = str(month)
        # Korzystamy z funkcji .zfill(x) aby dodać zera z lewej strony, co ma na celu zwiększenie długości zmiennej
        month = month.zfill(2)
        year = str(year)

        # Tutaj korzystamy ze wbudowanej w sqlite3 funkcji strftime, która pozwala nam wyciągnąć operacje z danego okresu czasowego
        self.cursor.execute(
            """ SELECT COUNT(*) FROM transactions WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?""",
            (month, year)
        )
        count = self.cursor.fetchone()
        self.cursor.execute(
            """SELECT SUM(amount) FROM transactions WHERE type = 'income' AND strftime('%m', date) = ? AND strftime('%Y', date) = ?""",
            (month, year)
        )
        income_amount = self.cursor.fetchone()
        self.cursor.execute(
            """SELECT SUM(amount) FROM transactions WHERE type = 'expense' AND strftime('%m', date) = ? AND strftime('%Y', date) = ?""",
            (month, year)
        )
        expense_amount = self.cursor.fetchone()

        print(f"Miesiąc: {month}")
        print(f"Kwota wpłat: {income_amount[0]}")
        print(f"Kwota wydatków: {expense_amount[0]}")
        print(f"Ilość transakcji: {count[0]}")

    # Funkcja kończąca połączenie z bazą danych
    def close_connection(self):
        self.connection.close()

    # Funkcja sprawdzająca istnienie transakcji w bazie danych
    def has_transactions(self):
        self.cursor.execute(
            """ SELECT 1 FROM transactions LIMIT 1;"""
        )
        exists = self.cursor.fetchone()
        if exists is not None:
            return True
        else:
            return False

    # Funkcja sprawdzająca, czy transakcja o danym id istnieje
    def transaction_exists(self, id):
        self.cursor.execute(
            """SELECT EXISTS (SELECT 1 FROM transactions  WHERE id = ? LIMIT 1)""",
            (id,)
        )
        exists = self.cursor.fetchone()
        if exists[0] == 1:
            return True
        else:
            return False