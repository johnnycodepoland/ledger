import datetime
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox

class AddTransactionDialog(QDialog):
    # Dodatkowo przekazujemy obiekt finance, aby wykorzystać go potem do zapisania dodanej transakcji w bazie danych
    def __init__(self, finance, savings):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę finance
        self.finance = finance

        # Inicjalizujemy klasę savings
        self.savings = savings

        # Ustawiamy tytuł okna formularza
        self.setWindowTitle("Dodaj transakcje")

        # Dodajemy pionowy layout
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

        # Tworzymy obiekt QComboBox, który pozwoli nam wybierać elementy z rozwijanej listy
        self.category_input = QComboBox()

        # Dajemy użytkownikowi wybór, dostępnych kategorii, w zależności od typu transakcji, currentIndexChanged daje nam sygnał za każdym razem, gdy mamy doczynienie ze zmianą typu transakcji
        self.type_input.currentIndexChanged.connect(self.update_categories)

        # Dodajemy widget do wprowadzania kategorii
        central_layout.addWidget(self.category_input)

        # Dodajemy przycisk do zatwierdzania formularza
        confirm_button = QPushButton("Dodaj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku
        confirm_button.clicked.connect(self.add_transaction)

        # Dodajemy przycisk do zatwierdzania formularza, do głównego layoutu
        central_layout.addWidget(confirm_button)

        # Wczytujemy od razy kategorie dla przychodów, aby dodawanie zajmowało mniej czasu
        self.update_categories()

    # Tworzymy funkcję, która poprzez klasę Finance zapiszę nam naszą nową transakcję, po zaakceptowaniu danych z formularza przyciskiem "Dodaj transakcję"
    def add_transaction(self):
        # Wyciągamy z wartość tekstową, z pól formularza, przy pomocy metody text()
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.information(self, "Błąd", "Podaj poprawną kwotę transakcji",)
            return
        type = self.type_input.currentText()
        category = self.category_input.currentText()

        # Zmieniamy język zmiennej "type" na j.ang
        type = "expense" if type == "Wydatek" else "income"

        # Zamieniamy kwotę transakcji na ujemną, jeśli jest ona wydatkiem
        if type == "expense":
            amount = 0 - amount

        # Pobieramy cele osczędnościowe poprzez klasę Savings, korzystając z funkcji savings.show_savings_goals_history()
        savings_goals = self.savings.show_savings_goals_history()

        # Iterujemy przez wszystkie cele osczędnościowe
        for savings_goal in savings_goals:
            # Porównujemy kategorie celu osczędnościowego z kategorią którą właśnie zapisujemy
            if savings_goal[3] == category:
                # Sprawdzamy typ transakcji
                if type == "expense":
                    # Jeżeli typ transakcji to wydatek, to dodajemy wartość bezwzględną tej kwoty
                    self.savings.edit_savings_goal(savings_goal[0], saved_amount=savings_goal[2] + abs(amount))
                else:
                    # Sprawdzamy czy po wykonaniu transakcji, saldo nie będzie ujemne
                    if savings_goal[2] - abs(amount) < 0:
                        QMessageBox.information(self, "Błąd", "Nie możesz wypłacić więcej niż odłożyłeś")
                        return

                    # Jeżeli typ transakcji to przychód, to odejmujemy wartość bezwzględną tej kwoty
                    self.savings.edit_savings_goal(savings_goal[0], saved_amount=savings_goal[2] - abs(amount))

        # Zapisujemy transakcję korzystając z funkcji klasy Finance
        self.finance.add_transaction(amount,  str(datetime.date.today()), type, category)

        # Akceptujemy prawidłowe zakończenie, dodawania danych z formularza
        self.accept()

    # Tworzymy funkcję, która pozwoli nam aktualizować wybór kategorii transakcji, w zależności od wybranego typu transakcji
    def update_categories(self):
        # Sprawdzamy typ transakcji
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

            # Pobieramy cele osczędnościowe poprzez klasę Savings, korzystając z funkcji savings.show_savings_goals_history()
            savings_goals = self.savings.show_savings_goals_history()

            # Iterujemy przez wszystkie cele osczędnościowe
            for savings_goal in savings_goals:
                # Zapisujemy nazwę celu do zmiennej name
                name = savings_goal[3]

                # Dodajemy name do kategorii transakcji
                self.category_input.addItem(name)

        elif self.type_input.currentText() == "Przychód":
            # Czyścimy dostępne opcje
            self.category_input.clear()

            # Dodajemy opcje wyboru kategorii transakcji
            self.category_input.addItem("💼 Wynagrodzenie")

            self.category_input.addItem("💻 Freelance")

            self.category_input.addItem("📈 Inwestycje")

            self.category_input.addItem("🎁 Prezent")

            self.category_input.addItem("🔄 Zwrot")

            self.category_input.addItem("💰 Inne przychody")

            # Pobieramy cele osczędnościowe poprzez klasę Savings, korzystając z funkcji savings.show_savings_goals_history()
            savings_goals = self.savings.show_savings_goals_history()

            # Iterujemy przez wszystkie cele osczędnościowe
            for savings_goal in savings_goals:
                # Zapisujemy nazwę celu do zmiennej name
                name = savings_goal[3]

                # Dodajemy name do kategorii transakcji
                self.category_input.addItem(name)

