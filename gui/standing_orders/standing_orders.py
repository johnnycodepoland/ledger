from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from gui.standing_orders.edit_standing_order_dialog import EditStandingOrderDialog
from gui.standing_orders.filter_standing_orders_dialog import FilterStandingOrdersDialog

class StandingOrders(QWidget):
    def __init__(self, recurring):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę recurring
        self.recurring = recurring

        # Ustawiamy pionowy layout
        self.central_layout = QVBoxLayout(self)

        # Dodajemy widget na tabele na stałe transakcje
        self.create_standing_orders_table()

    def create_standing_orders_table(self):
        # Tworzymy "kontener" na stałe transakcje, aby uniknąć błędu ze stylem widgetu na transakcje, który jest w formie tabeli
        standing_orders_container = QWidget()

        # Ustawiamy layout dla "kontenera" na stałe transakcje
        standing_orders_layout = QVBoxLayout(standing_orders_container)

        # Ustawiamy wielkość "kontenera" na stałe transakcje
        standing_orders_container.setFixedSize(1450, 650)

        # Dodajemy nazwę obiektu, dla standing_orders_container, aby uniknąć przekazywania stylu na "dzieci" standing_orders_container
        standing_orders_container.setObjectName("standing_orders_container")

        # Ustawiamy styl, tylko dla standing_orders_container bez przekazywania na jego "dzieci"
        standing_orders_container.setStyleSheet("#standing_orders_container {background-color: white; border-radius: 10px; padding: 10px;}")

        # Dodajemy tabele do widgetu na stałe transakcje
        self.standing_orders_table = QTableWidget(0, 5)

        # Blokujemy możliwość edycji komórek w tabeli
        self.standing_orders_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Importujemy wszystkie transakcje, korzystając z funkcji show_history()
        recurring = self.recurring.show_recurring_history()

        # Iterujemy przez wszystkie transakcje, aby dodać je do tabeli ze stałymi transakcjami
        for order in recurring:
            row = self.standing_orders_table.rowCount()
            self.standing_orders_table.insertRow(row)
            self.standing_orders_table.setItem(row, 0, QTableWidgetItem(str(order[0])))
            amount = abs(order[1])
            self.standing_orders_table.setItem(row, 1, QTableWidgetItem(str(amount)))
            self.standing_orders_table.setItem(row, 2, QTableWidgetItem(str(order[2])))
            type = "wydatek" if order[3] == "expense" else "przychód"
            self.standing_orders_table.setItem(row, 3, QTableWidgetItem(type))
            self.standing_orders_table.setItem(row, 4, QTableWidgetItem(str(order[4])))

        # Ukrywamy kolumnę z ID
        self.standing_orders_table.setColumnHidden(0, True)

        # Ustawiamy automatyczne wypełnianie całej dostępnej przestrzeni przez kolumny
        self.standing_orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Dodajemy widget na historię transakcji do layoutu "kontenera" na stałe transakcje
        standing_orders_layout.addWidget(self.standing_orders_table)

        # Ustawiamy nagłówki / nazwy kolumn dla tabeli history_table
        self.standing_orders_table.setHorizontalHeaderLabels(["ID", "Kwota", "Dzień miesiąca", "Typ", "Kategoria"])

        # Dodajemy "kontener" na transakcje, do głównego layoutu
        self.central_layout.addWidget(standing_orders_container)

    def delete_standing_order(self):
        # Sprawdzamy, czy wiersz został uprzednio zaznaczony
        if self.standing_orders_table.currentRow() == -1:
            return

        # Sprawdzamy numer aktualnie zaznaczonego wiersza
        current_row = self.standing_orders_table.currentRow()

        # Wyciągamy id z wybranego rzędu
        id = self.standing_orders_table.item(current_row, 0).text()

        # Zamieniamy string "id" na int
        id = int(id)

        # Usuwamy daną transakcję
        self.recurring.delete_recurring_transaction(id)

        # Odświeżamy tabele ze stałym transakcjami
        self.refresh_standing_orders_table()

    def open_edit_dialog(self):
        # Sprawdzamy, czy wiersz został uprzednio zaznaczony
        if self.standing_orders_table.currentRow() == -1:
            return

        # Sprawdzamy numer aktualnie zaznaczonego wiersza
        current_row = self.standing_orders_table.currentRow()

        # Wyciągamy id z wybranego rzędu
        id = self.standing_orders_table.item(current_row, 0).text()

        # Zamieniamy string "id" na int
        id = int(id)

        # Inicjalizujemy klasę EditStandingOrderDialog
        edit = EditStandingOrderDialog(id, self.recurring)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz edycji stałej transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        edit.exec()

        # Odświeżamy tabele z historią stałych transakcji
        self.refresh_standing_orders_table()

    def open_filter_dialog(self):
        # Inicjalizujemy klasę FilterTransactionDialog
        filter = FilterStandingOrdersDialog()

        # Sprawdzamy, czy formularz został zaakceptowany, korzystając z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania stałej transakcji, blokując przy tym korzystanie z wszystkich innych okien aplikacji
        if filter.exec() == QDialog.DialogCode.Accepted:
            # Zapisujemy dane z formularza do zmiennych, które zostaną wykorzystane przez refresh_standing_orders_table
            type = filter.type

            category = filter.category

            # Odświeżamy tabele z historią stałych transakcji
            self.refresh_standing_orders_table(type, category)

    # Dodajemy funkcję, która odświeży nam historię transakcji po jakiejś aktywności np. usunięciu stałej transakcji
    def refresh_standing_orders_table(self, type=None, category=None):
        # Resetujemy liczbę wierszy
        self.standing_orders_table.setRowCount(0)

        # Importujemy wszystkie stałę transakcje, korzystając z funkcji show_history()
        transactions = self.recurring.show_recurring_history(type=type, category=category)

        # Iterujemy przez wszystkie stałe transakcje, aby dodać je do tabeli z ostatnimi stałymi transakcjami
        for transaction in transactions:
            row = self.standing_orders_table.rowCount()
            self.standing_orders_table.insertRow(row)
            self.standing_orders_table.setItem(row, 0, QTableWidgetItem(str(transaction[0])))
            amount = abs(transaction[1])
            self.standing_orders_table.setItem(row, 1, QTableWidgetItem(str(amount)))
            self.standing_orders_table.setItem(row, 2, QTableWidgetItem(str(transaction[2])))
            type = "wydatek" if transaction[3] == "expense" else "przychód"
            self.standing_orders_table.setItem(row, 3, QTableWidgetItem(type))
            self.standing_orders_table.setItem(row, 4, QTableWidgetItem(str(transaction[4])))