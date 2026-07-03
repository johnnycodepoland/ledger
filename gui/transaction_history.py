from tracemalloc import Filter

from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from gui.edit_transaction_dialog import EditTransactionDialog
from gui.filter_transaction_dialog import FilterTransactionDialog

class TransactionHistory(QWidget):
    def __init__(self, finance):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę finance
        self.finance = finance

        # Ustawiamy pionowy layout
        self.central_layout = QVBoxLayout(self)

        # Dodajemy tabele na historię transakcji
        self.create_transaction_table()

    def create_transaction_table(self):
        # Tworzymy "kontener" na historię transakcji, aby uniknąć błędu ze stylem widgetu na transakcje, który jest w formie tabeli
        table_container = QWidget()

        # Ustawiamy layout dla "kontenera" na historię transakcji
        table_layout = QVBoxLayout(table_container)

        # Ustawiamy wielkość "kontenera" na historię na transakcji
        table_container.setFixedSize(1450, 650)

        # Dodajemy nazwę obiektu, dla table_container, aby uniknąć przekazywania stylu na "dzieci" table_container
        table_container.setObjectName("table_container")

        # Ustawiamy styl, tylko dla table_container bez przekazywania na jego "dzieci"
        table_container.setStyleSheet("#table_container {background-color: white; border-radius: 10px; padding: 10px;}")

        # Dodajemy widget na historię transakcji
        self.history_table = QTableWidget(0, 5)

        # Blokujemy możliwość edycji komórek w tabeli
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Importujemy wszystkie transakcje, korzystając z funkcji show_history()
        transactions = self.finance.show_history()

        # Iterujemy przez wszystkie transakcje, aby dodać je do tabeli z ostatnimi transakcjami
        for transaction in transactions:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(str(transaction[0])))
            amount = abs(transaction[1])
            self.history_table.setItem(row, 1, QTableWidgetItem(str(amount)))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(transaction[2])))
            type = "wydatek" if transaction[3] == "expense" else "przychód"
            self.history_table.setItem(row, 3, QTableWidgetItem(type))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(transaction[4])))

        # Ukrywamy kolumnę z ID
        self.history_table.setColumnHidden(0, True)

        # Ustawiamy automatyczne wypełnianie całej dostępnej przestrzeni przez kolumny
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Dodajemy widget na historię transakcji do layoutu "kontenera" na transakcje
        table_layout.addWidget(self.history_table)

        # Ustawiamy nagłówki / nazwy kolumn dla tabeli history_table
        self.history_table.setHorizontalHeaderLabels(["ID", "Kwota", "Data", "Typ", "Kategoria"])

        # Dodajemy "kontener" na transakcje, do głównego layoutu
        self.central_layout.addWidget(table_container)

    def delete_transaction(self):
        # Sprawdzamy, czy wiersz został uprzednio zaznaczony
        if self.history_table.currentRow() == -1:
            return

        # Sprawdzamy numer aktualnie zaznaczonego wiersza
        current_row = self.history_table.currentRow()

        # Wyciągamy id z wybranego rzędu
        id = self.history_table.item(current_row, 0).text()

        # Zamieniamy string "id" na int
        id = int(id)

        # Usuwamy daną transakcję
        self.finance.delete_transaction(id)

        # Odświeżamy tabele z historią transakcji
        self.refresh_history_table()

    def open_edit_dialog(self):
        # Sprawdzamy, czy wiersz został uprzednio zaznaczony
        if self.history_table.currentRow() == -1:
            return

        # Sprawdzamy numer aktualnie zaznaczonego wiersza
        current_row = self.history_table.currentRow()

        # Wyciągamy id z wybranego rzędu
        id = self.history_table.item(current_row, 0).text()

        # Zamieniamy string "id" na int
        id = int(id)

        # Inicjalizujemy klasę EditTransactionHistory
        edit = EditTransactionDialog(id, self.finance)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        edit.exec()

        # Odświeżamy tabele z historią transakcji
        self.refresh_history_table()

    def open_filter_dialog(self):
        # Inicjalizujemy klasę FilterTransactionHistory
        filter = FilterTransactionDialog()

        # Sprawdzamy, czy formularz został zaakceptowany, korzystając z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokując przy tym korzystanie z wszystkich innych okien aplikacji
        if filter.exec() == QDialog.DialogCode.Accepted:
            # Zapisujemy dane z formularza do zmiennych, które zostaną wykorzystane przez refresh_history_table
            type = filter.type

            category = filter.category

            # Odświeżamy tabele z historią transakcji
            self.refresh_history_table(type, category)

    # Dodajemy funkcję, która odświeży nam historię transakcji po jakiejś aktywności np. usunięciu transakcji
    def refresh_history_table(self, type=None, category=None):
        # Resetujemy liczbę wierszy
        self.history_table.setRowCount(0)

        # Importujemy wszystkie transakcje, korzystając z funkcji show_history()
        transactions = self.finance.show_history(type=type, category=category)

        # Iterujemy przez wszystkie transakcje, aby dodać je do tabeli z ostatnimi transakcjami
        for transaction in transactions:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(str(transaction[0])))
            amount = abs(transaction[1])
            self.history_table.setItem(row, 1, QTableWidgetItem(str(amount)))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(transaction[2])))
            type = "wydatek" if transaction[3] == "expense" else "przychód"
            self.history_table.setItem(row, 3, QTableWidgetItem(type))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(transaction[4])))