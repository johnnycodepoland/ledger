import datetime
import sqlite3
import os

class Savings:
    def __init__(self):
        # Łączymy się z bazą danych i blokujemy otwieranie bazy danych w folderze gui
        db_path = os.path.join(os.path.dirname(__file__), "../transactions.db")
        self.connection = sqlite3.connect(db_path)

        # Tworzymy cursor
        self.cursor = self.connection.cursor()

        # Tworzymy bazę danych
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS savings_goals (
            id INTEGER PRIMARY KEY,
            target_amount REAl,
            saved_amount REAl,
            name TEXT,
            date TEXT)
            """)

    # Funkcja dodająca cele oszszczędnościowe
    def add_savings_goal(self, target_amount, saved_amount, name, date):
        # Zapisujemy transakcję wraz z jej parametrami
        self.cursor.execute(
            """INSERT INTO savings_goals (target_amount, saved_amount, name, date) VALUES (?, ?, ?, ?)""",
            (target_amount, saved_amount, name, date)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja wypisująca cele oszszczędnościowe
    def show_savings_goals_history(self):
        self.cursor.execute(
            """SELECT * FROM savings_goals"""
        )
        savings_goals = self.cursor.fetchall()
        return savings_goals

    # Funkcja umożliwiająca celów oszczędnościowych
    def edit_savings_goal(self, id, target_amount=None, saved_amount=None, name=None, date=None):
        if target_amount is not None:
            self.cursor.execute(
                """UPDATE savings_goals
                SET target_amount = ?
                WHERE id = ?""",
                (target_amount, id)
            )
        if saved_amount is not None:
            self.cursor.execute(
                """UPDATE savings_goals
                SET saved_amount = ?
                WHERE id = ?""",
                (saved_amount, id)
            )
        if name is not None:
            self.cursor.execute(
                """UPDATE savings_goals
                SET name = ?
                WHERE id = ?""",
                (name, id)
            )
        if date is not None:
            self.cursor.execute(
                """UPDATE savings_goals
                SET date = ?
                WHERE id = ?""",
                (date, id)
            )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()

    # Funkcja umożliwiająca usunięcie celu oszczędnościowego
    def delete_savings_goal(self, id):
        self.cursor.execute(
            """DELETE FROM savings_goals WHERE id = ?""",
            (id,)
        )
        # Zapisujemy zmiany i kończymy połączenie
        self.connection.commit()