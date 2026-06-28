import datetime
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox


class AddTransactionDialog(QDialog):
    # Dodatkowo przekazujemy obiekt Finance, aby wykorzystać ją potem do zapisania dodanej transakcji w bazie danych
    def __init__(self, finance):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę finance
        self.finance = finance

        # Ustawiamy tytuł okna formularza
        self.setWindowTitle("Dodaj transakcje")

        # Dodajemy layout
        central_layout = QVBoxLayout(self)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.amount_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania kwoty transakcji
        self.amount_input.setPlaceholderText("Kwota")

        # Dodajemy widget do wprowadzania kwoty
        central_layout.addWidget(self.amount_input)

        # Tworzymy obiekt QComboBox, który pozwoli nam wybierać elementy z rozwijanej listy
        self.type_input = QComboBox()

        # Dodajemy opcje wyboru typu transakcji
        self.type_input.addItem("Przychód")

        self.type_input.addItem("Wydatek")

        # Dodajemy widget do wprowadzania typu transakcji
        central_layout.addWidget(self.type_input)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.category_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania kategori transakcji
        self.category_input.setPlaceholderText("Kategoria")

        # Dodajemy widget do wprowadzania kategorii
        central_layout.addWidget(self.category_input)

        # Dodajemy przycisk do zatwierdzania formularza
        confirm_button = QPushButton("Dodaj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku
        confirm_button.clicked.connect(self.add_transaction)

        # Dodajemy przycisk do zatwierdzania formularza, do głównego layoutu
        central_layout.addWidget(confirm_button)

    # Tworzymy funkcję, która poprzez klasę Finance zapiszę nam naszą nową transakcję
    def add_transaction(self):
        # Wyciągamy z wartość tekstową, z pól formularza, przy pomocy metody text()
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.information(self, "Błąd", "Podaj poprawną kwotę transakcji",)
            return
        type = self.type_input.currentText()
        category = self.category_input.text()

        # Zmieniamy język zmiennej "type" na j.ang
        type = "expense" if type == "Wydatek" else "income"

        # Zamieniamy kwotę transakcji na ujemną, jeśli jest ona wydatkiem
        if type == "expense":
            amount = 0 - amount

        # Zapisujemy transakcję korzystając z funkcji klasy Finance
        self.finance.add_transaction(amount,  str(datetime.date.today()), type, category)

        # Akceptujemy prawidłowe zakończenie, dodawania danych z formularza
        self.accept()

