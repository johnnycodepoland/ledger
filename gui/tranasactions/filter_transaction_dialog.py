import datetime
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox

class FilterTransactionDialog(QDialog):
    # Dodatkowo przekazujemy obiekt Finance, aby wykorzystać ją potem do zapisania dodanej transakcji w bazie danych
    def __init__(self):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Ustawiamy tytuł okna formularza
        self.setWindowTitle("Filtruj transakcje")

        # Dodajemy pionowy layout
        central_layout = QVBoxLayout(self)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.amount_input = QLineEdit()

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
        confirm_button = QPushButton("Filtruj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku
        confirm_button.clicked.connect(self.filter_transaction)

        # Dodajemy przycisk do zatwierdzania formularza, do głównego layoutu
        central_layout.addWidget(confirm_button)

    # Tworzymy funkcję, która poprzez klasę Finance zapiszę nam naszą nową transakcję, po zaakceptowaniu danych z formularza przyciskiem "Edytuj transakcję"
    def filter_transaction(self):
        # Zamieniamy dane z formularza na tekst
        self.type = self.type_input.currentText()

        self.category = self.category_input.text() or None

        # Zmieniamy język zmiennej "type" na j.ang
        self.type = "expense" if self.type == "Wydatek" else "income"

        # Akceptujemy prawidłowe zakończenie, dodawania danych z formularza
        self.accept()
