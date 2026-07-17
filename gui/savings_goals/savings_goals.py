import datetime
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from gui.savings_goals.edit_savings_goal_dialog import EditSavingsGoalDialog\

class SavingsGoals(QWidget):
    def __init__(self, savings, finance):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę savings
        self.savings = savings

        # Inicjalizujemy klasę finance
        self.finance = finance

        # Ustawiamy pionowy layout
        self.central_layout = QVBoxLayout(self)

        # Dodajemy widget na tabele na cele oszczędnościowe
        self.create_savings_goals_table()

    def create_savings_goals_table(self):
        # Tworzymy "kontener" na cele oszczędnościowe transakcje, aby uniknąć błędu ze stylem widgetu na transakcje, który jest w formie tabeli
        savings_goals_container = QWidget()

        # Ustawiamy layout dla "kontenera" na cele oszczędnościowe
        savings_goals_layout = QVBoxLayout(savings_goals_container)

        # Ustawiamy wielkość "kontenera" na cele oszczędnościowe
        savings_goals_container.setFixedSize(1450, 650)

        # Dodajemy nazwę obiektu, dla savings_goals_container, aby uniknąć przekazywania stylu na "dzieci" savings_goals_container
        savings_goals_container.setObjectName("savings_goals_container")

        # Ustawiamy styl, tylko dla savings_goals_container bez przekazywania na jego "dzieci"
        savings_goals_container.setStyleSheet("#savings_goals_container {background-color: white; border-radius: 10px; padding: 10px;}")

        # Dodajemy tabele do widgetu na cele oszczędnościowe
        self.savings_goals_table = QTableWidget(0, 5)

        # Blokujemy możliwość edycji komórek w tabeli
        self.savings_goals_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Importujemy wszystkie cele oszczędnościowe, korzystając z funkcji show_savings_goals_history()
        savings_goals = self.savings.show_savings_goals_history()

        # Iterujemy przez wszystkie cele oszczędnościowe, aby dodać je do tabeli z celami oszczędnościowymi
        for savings_goal in savings_goals:
            row = self.savings_goals_table.rowCount()
            self.savings_goals_table.insertRow(row)
            self.savings_goals_table.setItem(row, 0, QTableWidgetItem(str(savings_goal[0])))
            target_amount = abs(savings_goal[1])
            self.savings_goals_table.setItem(row, 1, QTableWidgetItem(str(target_amount)))
            saved_amount = str(savings_goal[2])
            self.savings_goals_table.setItem(row, 2, QTableWidgetItem(str(saved_amount)))
            self.savings_goals_table.setItem(row, 3, QTableWidgetItem(str(savings_goal[3])))
            self.savings_goals_table.setItem(row, 4, QTableWidgetItem(str(savings_goal[4])))

        # Ukrywamy kolumnę z ID
        self.savings_goals_table.setColumnHidden(0, True)

        # Ustawiamy automatyczne wypełnianie całej dostępnej przestrzeni przez kolumny
        self.savings_goals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Dodajemy widget na cele oszczędnościowe do layoutu "kontenera" na cele oszczędnościowe
        savings_goals_layout.addWidget(self.savings_goals_table)

        # Ustawiamy nagłówki / nazwy kolumn dla tabeli savings_goals_table
        self.savings_goals_table.setHorizontalHeaderLabels(["ID", "Kwota docelowa", "Kwota odłożona", "Nazwa", "Data zakończenia"])

        # Dodajemy "kontener" na cele oszczędnościowe, do głównego layoutu
        self.central_layout.addWidget(savings_goals_container)

    def delete_savings_goal(self):
        # Sprawdzamy, czy wiersz został uprzednio zaznaczony
        if self.savings_goals_table.currentRow() == -1:
            return

        # Sprawdzamy numer aktualnie zaznaczonego wiersza
        current_row = self.savings_goals_table.currentRow()

        # Wyciągamy id z wybranego rzędu
        id = self.savings_goals_table.item(current_row, 0).text()

        # Zamieniamy string "id" na int
        id = int(id)

        # Wyciągamy saved_amount z wybranego rzędu
        saved_amount = self.savings_goals_table.item(current_row, 2).text()

        # Zamieniamy string "saved_amount" na float
        saved_amount = float(saved_amount)

        # Wyciągamy name z wybranego rzędu
        name = self.savings_goals_table.item(current_row, 3).text()

        self.finance.add_transaction(saved_amount, str(datetime.date.today()), "income", name)

        # Usuwamy dany cel osczędnościowy
        self.savings.delete_savings_goal(id)

        # Odświeżamy tabele z celami osczędnościowymi
        self.refresh_savings_goals_table()

    def open_edit_dialog(self):
        # Sprawdzamy, czy wiersz został uprzednio zaznaczony
        if self.savings_goals_table.currentRow() == -1:
            return

        # Sprawdzamy numer aktualnie zaznaczonego wiersza
        current_row = self.savings_goals_table.currentRow()

        # Wyciągamy id z wybranego rzędu
        id = self.savings_goals_table.item(current_row, 0).text()

        # Zamieniamy string "id" na int
        id = int(id)

        # Inicjalizujemy klasę EditStandingOrderDialog
        edit = EditSavingsGoalDialog(id, self.savings, self)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz edycji celu osczędnościowego, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        edit.exec()

        # Odświeżamy tabele z historią transakcji
        self.refresh_savings_goals_table()

    # Dodajemy funkcję, która odświeży nam cele oszczędnościowe po jakiejś aktywności np. usunięciu celu oszczędnościowego
    def refresh_savings_goals_table(self, type=None, category=None):
        # Resetujemy liczbę wierszy
        self.savings_goals_table.setRowCount(0)

        # Importujemy wszystkie cele oszczędnościowe, korzystając z funkcji show_savings_goals_history()
        savings_goals = self.savings.show_savings_goals_history()

        # Iterujemy przez wszystkie cele oszczędnościowe, aby dodać je do tabeli z celami oszczędnościowymi
        for savings_goal in savings_goals:
            row = self.savings_goals_table.rowCount()
            self.savings_goals_table.insertRow(row)
            self.savings_goals_table.setItem(row, 0, QTableWidgetItem(str(savings_goal[0])))
            target_amount = abs(savings_goal[1])
            self.savings_goals_table.setItem(row, 1, QTableWidgetItem(str(target_amount)))
            saved_amount = str(savings_goal[2])
            self.savings_goals_table.setItem(row, 2, QTableWidgetItem(str(saved_amount)))
            self.savings_goals_table.setItem(row, 3, QTableWidgetItem(str(savings_goal[3])))
            self.savings_goals_table.setItem(row, 4, QTableWidgetItem(str(savings_goal[4])))