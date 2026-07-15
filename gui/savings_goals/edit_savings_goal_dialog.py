import datetime
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox

class EditSavingsGoalDialog(QDialog):
    # Dodatkowo przekazujemy obiekt Finance, aby wykorzystać ją potem do zapisania dodanej transakcji w bazie danych
    def __init__(self, id, savings):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Zapisujemy id jako self. żeby wszystkie funkcje miały do niego dostęp
        self.id = id

        # Inicjalizujemy klasę savings
        self.savings = savings

        # Ustawiamy tytuł okna formularza
        self.setWindowTitle("Edytuj cel osczędnościowy")

        # Dodajemy pionowy layout
        central_layout = QVBoxLayout(self)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.target_amount_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania docelowej kwoty celu oszczędnościowego
        self.target_amount_input.setPlaceholderText("Kwota docelowa")

        # Dodajemy widget do wprowadzania kwoty docelowej do głównego layoutu
        central_layout.addWidget(self.target_amount_input)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.name_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania nazwy celu oszczędnościowego
        self.name_input.setPlaceholderText("Nazwa")

        # Dodajemy widget do wprowadzania nazwy, do głównego layoutu
        central_layout.addWidget(self.name_input)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.target_date_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania daty celu
        self.target_date_input.setPlaceholderText("Data celu (YYYY-MM-DD)")

        # Dodajemy widget do wprowadzania daty celu, do głównego layoutu
        central_layout.addWidget(self.target_date_input)

        # Dodajemy przycisk do zatwierdzania formularza
        confirm_button = QPushButton("Edytuj cel osczędnościowy")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku
        confirm_button.clicked.connect(self.edit_savings_goal)

        # Dodajemy przycisk do zatwierdzania formularza, do głównego layoutu
        central_layout.addWidget(confirm_button)

    # Tworzymy funkcję, która poprzez klasę Savings zatwierdzi nam edycje celu osczędnościowego, po zaakceptowaniu danych z formularza przyciskiem "Edytuj transakcję"
    def edit_savings_goal(self):
        # Wyciągamy wartość tekstową, z pól formularza, przy pomocy metody text()
        try:
            target_amount = float(self.target_amount_input.text())
        except ValueError:
            QMessageBox.information(self, "Błąd", "Podaj poprawną docelową kwotę celu osczędnościowego",)
            return
        name = self.name_input.text()
        try:
            datetime.datetime.strptime(self.target_date_input.text(), "%Y-%m-%d")
        except ValueError:
            QMessageBox.information(self, "Błąd", "Podaj datę w formacie YYYY-MM-DD")
            return
        date = self.target_date_input.text()

        # Zapisujemy cel osczędnościowy korzystając z funkcji klasy Savings
        self.savings.edit_savings_goal(self.id, target_amount, 0, name, date)

        # Akceptujemy prawidłowe zakończenie, dodawania danych z formularza
        self.accept()