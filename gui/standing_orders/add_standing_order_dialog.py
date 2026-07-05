from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox

class AddStandingOrderDialog(QDialog):
    # Dodatkowo przekazujemy obiekt Finance, aby wykorzystać ją potem do zapisania dodanej transakcji w bazie danych
    def __init__(self, recurring):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę recurring
        self.recurring = recurring

        # Ustawiamy tytuł okna formularza
        self.setWindowTitle("Dodaj stałą transakcje")

        # Dodajemy pionowy layout
        central_layout = QVBoxLayout(self)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.amount_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania kwoty transakcji
        self.amount_input.setPlaceholderText("Kwota")

        # Dodajemy widget do wprowadzania kwoty
        central_layout.addWidget(self.amount_input)

        # Tworzymy obiekt QLineEdit, który pozwoli nam wprowadzać tekst
        self.day_input = QLineEdit()

        # Ustawiamy nazwę dla placeholderu, do przyjmowania kwoty transakcji
        self.day_input.setPlaceholderText("Dzień miesiąca (1-31)")

        # Dodajemy widget do wprowadzania dnia, do głównego layoutu
        central_layout.addWidget(self.day_input)

        # Tworzymy obiekt QComboBox, który pozwoli nam wybierać elementy z rozwijanej listy
        self.type_input = QComboBox()

        # Dodajemy opcje wyboru typu transakcji
        self.type_input.addItem("Przychód")

        self.type_input.addItem("Wydatek")

        # Dodajemy widget do wprowadzania typu transakcji
        central_layout.addWidget(self.type_input)

        # Tworzymy obiekt QComboBox, który pozwoli nam wybierać elementy z rozwijanej listy
        self.category_input = QComboBox()

        # Dajemy użytkownikowi wybór, dostępnych kategorii, w zależności od typu stałej transakcji, currentIndexChanged daje nam sygnał za każdym razem, gdy mamy doczynienie ze zmianą typu transakcji
        self.type_input.currentIndexChanged.connect(self.update_categories)

        # Dodajemy widget do wprowadzania kategorii
        central_layout.addWidget(self.category_input)

        # Dodajemy przycisk do zatwierdzania formularza
        confirm_button = QPushButton("Dodaj stałą transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku
        confirm_button.clicked.connect(self.add_standing_order)

        # Dodajemy przycisk do zatwierdzania formularza, do głównego layoutu
        central_layout.addWidget(confirm_button)

    # Tworzymy funkcję, która poprzez klasę Finance zapiszę nam naszą nową transakcję, po zaakceptowaniu danych z formularza przyciskiem "Dodaj transakcję"
    def add_standing_order(self):
        # Wyciągamy z wartość tekstową, z pól formularza, przy pomocy metody text()
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.information(self, "Błąd", "Podaj poprawną kwotę stałej transakcji",)
            return
        if not self.day_input.text():
            QMessageBox.information(self, "Błąd", "Podaj dzień miesiąca")
            return
        try:
            day = int(self.day_input.text())
            if day < 1 or day > 31:
                # Jeżeli podany dzień nie będzie prawidłowy, to zostanie wywołany ValueError
                raise ValueError
        except ValueError:
            QMessageBox.information(self, "Błąd", "Podaj poprawny dzień (1-31)")
            return
        type = self.type_input.currentText()
        category = self.category_input.currentText()

        # Zmieniamy język zmiennej "type" na j.ang
        type = "expense" if type == "Wydatek" else "income"

        # Zamieniamy kwotę transakcji na ujemną, jeśli jest ona wydatkiem
        if type == "expense":
            amount = 0 - amount

        # Zapisujemy transakcję korzystając z funkcji klasy Recurring
        self.recurring.add_recurring_transaction(amount, day, type, category)

        # Akceptujemy prawidłowe zakończenie, dodawania danych z formularza
        self.accept()

    # Tworzymy funkcję, która pozwoli nam aktualizować wybór kategorii stałej transakcji, w zależności od wybranego typu transakcji
    def update_categories(self):
        # Sprawdzamy typ stałej transakcji
        if self.type_input.currentText() == "Wydatek":
            # Czyścimy dostępne opcje
            self.category_input.clear()

            # Dodajemy opcje wyboru kategorii transakcji
            self.category_input.addItem("🍔 Jedzenie")

            self.category_input.addItem("🚗 Transport")

            self.category_input.addItem("🏠 Mieszkanie")

            self.category_input.addItem("🏥 Zdrowie")

            self.category_input.addItem("🎮 Rozrywka")

            self.category_input.addItem("👕 Ubrania")

            self.category_input.addItem("📚 Edukacja")

            self.category_input.addItem("📱 Subskrypcje")

            self.category_input.addItem("💪 Sport")

            self.category_input.addItem("✈️ Podróże")

            self.category_input.addItem("💸 Inne wydatki")

        elif self.type_input.currentText() == "Przychód":
            # Czyścimy dostępne opcje
            self.category_input.clear()

            # Dodajemy opcje wyboru kategorii stałej transakcji
            self.category_input.addItem("💼 Wynagrodzenie")

            self.category_input.addItem("💻 Freelance")

            self.category_input.addItem("📈 Inwestycje")

            self.category_input.addItem("🎁 Prezent")

            self.category_input.addItem("🔄 Zwrot")

            self.category_input.addItem("💰 Inne przychody")