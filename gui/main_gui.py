import sys
from finance import Finance
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QHBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QFont
from add_transaction_dialog import AddTransactionDialog

class MainWindow(QMainWindow):
    def __init__(self):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę finance
        self.finance = Finance()

        # Ustawiamy tytuł okna aplikacji
        self.setWindowTitle("Financial tracker")

        # Ustawiamy rozmiar okna
        self.setGeometry(100, 200, 1500, 800)

        # Pusty pojemnik na zawartość okna
        central_widget = QWidget()

        # Informacja dla okna o tym, że pojemnik, który przed chwilą utworzyliśmy jest jego wnętrzem
        self.setCentralWidget(central_widget)

        # Informacja dla pojemnika o tym, że ma wszystko układać pionowo
        self.layout = QVBoxLayout(central_widget)

        # Dodajemy nawigacje
        self.create_navigation()

        # Dodajemy dashboard
        self.create_dashboard()

    def create_navigation(self):
        # Tworzymy widget na zakładki
        tab_widget = QWidget()

        # Tworzymy layout dla widgetu na zakładki
        tab_layout = QHBoxLayout(tab_widget)

        # Dodajemy przycisk "Dodaj transakcje"
        transactions_button = QPushButton("Dodaj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        transactions_button.clicked.connect(self.open_add_transaction_dialog)

        # Dodajemy przycisk "Dodaj transakcje" do layoutu na zakładki
        tab_layout.addWidget(transactions_button)

        # Przesuwamy przyciski na prawą stronę
        tab_layout.addStretch()

        # Dodajemy przycisk "Dashboard"
        dashboard_button = QPushButton("Dashboard")

        # Dodajemy dashboard_button do layoutu na zakładki
        tab_layout.addWidget(dashboard_button)

        # Dodajemy przycisk "Transakcje"
        transactions_button = QPushButton("Transakcje")

        # Dodajemy dashboard_button do layoutu na zakładki
        tab_layout.addWidget(transactions_button)

        # Dodajemy przycisk "Cykliczne"
        cyclical_button = QPushButton("Cykliczne")

        # Dodajemy cyclical_button do layoutu na zakładki
        tab_layout.addWidget(cyclical_button)

        # Dodajemy przycisk "Raporty"
        report_button = QPushButton("Oszczędności")

        # Dodajemy report_button do layoutu na zakładki
        tab_layout.addWidget(report_button)

        # Ustawiamy maksymalną wielkość dla widgetu, tab_widget
        tab_widget.setMaximumHeight(50)

        # Dodajemy tab_widget do głównego layoutu
        self.layout.addWidget(tab_widget)

    # Główny dashboard
    def create_dashboard(self):
        # Tworzymy widget na treść
        content_widget = QWidget()

        # Tworzymy layout dla widgetu na treść
        self.content_layout = QVBoxLayout(content_widget)

        # Dodajemy widget na treść do głównego layoutu
        self.layout.addWidget(content_widget)

        # Wywołujemy widgety na górną i dolną treść
        self.create_top_section()

        self.create_bottom_section()

    # Górna część dashboardu
    def create_top_section(self):
        # Tworzymy widget na górną część treści
        top_widget = QWidget()

        # Tworzymy layout dla widgetu na górną część treści
        top_layout = QHBoxLayout(top_widget)

        # Dodajemy widget na górną część treści do layoutu na treść
        self.content_layout.addWidget(top_widget)

        # Dodajemy widget na balans
        self.balance_label = QLabel(f"Saldo: {self.finance.return_balance()}zł")

        # Ustawiamy styl widgetu na balans
        self.balance_label.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")

        # Ustawiamy wielkość widgetu na balans
        self.balance_label.setFixedSize(600, 120)

        # Ustawiamy czcionkę i jej rozmiar
        self.balance_label.setFont(QFont("Arial", 70))

        # Dodajemy widget na wpłaty do górnego widgetu na treść
        top_layout.addWidget(self.balance_label)

        # Dodajemy widget na wpłaty
        self.income_label = QLabel(f"Wpłaty: {self.finance.return_income()}zł")

        # Ustawiamy styl widgetu na wpłaty
        self.income_label.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")

        # Ustawiamy wielkość widgetu na wpłaty
        self.income_label.setFixedSize(400, 120)

        # Ustawiamy czcionkę i jej rozmiar
        self.income_label.setFont(QFont("Arial", 40))

        # Dodajemy widget na wpłaty do górnego widgetu na treść
        top_layout.addWidget(self.income_label)

        # Dodajemy widget na wydatki
        self.expense_label = QLabel(f"Wydatki: {self.finance.return_expense()}zł")

        # Ustawiamy styl widgetu na wydatki
        self.expense_label.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")

        # Ustawiamy wielkość widgetu na wydatki
        self.expense_label.setFixedSize(400, 120)

        # Ustawiamy czcionkę i jej rozmiar
        self.expense_label.setFont(QFont("Arial", 40))

        # Dodajemy widget na wydatki do górnego widgetu na treść
        top_layout.addWidget(self.expense_label)

        # Wypychamy widget na saldo na maksa w lewo
        top_layout.addStretch()

    # Dolna część dashboardu
    def create_bottom_section(self):
        # Tworzymy widget na dolną część treści
        bottom_widget = QWidget()

        # Tworzymy layout dla widgetu na dolną część treści
        bottom_layout = QHBoxLayout(bottom_widget)

        # Dodajemy widget na dolną część treści do layoutu na treść
        self.content_layout.addWidget(bottom_widget)

        # Tworzymy "kontener" na historię transakcji, aby uniknąć błędu ze stylem widgetu na transakcje, który jest w formie tabeli
        table_container = QWidget()

        # Ustawiamy layout dla "kontenera" na historię transakcji
        table_layout = QVBoxLayout(table_container)

        # Ustawiamy wielkość "kontenera" na historię na transakcji
        table_container.setFixedSize(600, 480)

        # Dodajemy nazwę obiektu, dla table_container, aby uniknąć przekazywania stylu na "dzieci" table_container
        table_container.setObjectName("table_container")

        # Ustawiamy styl, tylko dla table_container bez przekazywania na jego "dzieci"
        table_container.setStyleSheet("#table_container {background-color: white; border-radius: 10px; padding: 10px;}")

        # Dodajemy widget na historię transakcji
        self.history_table = QTableWidget(0, 4)

        # Blokujemy możliwość edycji komórek w tabeli
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Importujemy wszystkie transakcje, korzystając z funkcji show_history()
        transactions = self.finance.show_history()

        # Iterujemy przez wszystkie transakcje, aby dodać je do tabeli z ostatnimi transakcjami
        for transaction in transactions:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            amount = abs(transaction[1])
            self.history_table.setItem(row, 0, QTableWidgetItem(str(amount)))
            self.history_table.setItem(row, 1, QTableWidgetItem(str(transaction[2])))
            type = "wydatek" if transaction[3] == "expense" else "przychód"
            self.history_table.setItem(row, 2, QTableWidgetItem(type))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(transaction[4])))

        # Ustawiamy automatyczne wypełnianie całej dostępnej przestrzeni przez kolumny
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Dodajemy widget na historię transakcji do layoutu "kontenera" na transakcje
        table_layout.addWidget(self.history_table)

        # Ustawiamy nagłówki / nazwy kolumn dla tabeli history_table
        self.history_table.setHorizontalHeaderLabels(["Kwota", "Data", "Typ", "Kategoria"])

        # Dodajemy "kontener" na transakcje, do dolnego layoutu
        bottom_layout.addWidget(table_container)

        # Wypychamy dolną część treści na maksa w lewo
        bottom_layout.addStretch()

    # Ta funkcji pozwoli nam uniknąć otwierania okna dodawania transakcji za każdym razem po włączeniu programu
    def open_add_transaction_dialog(self):
        # Inicjalizujemy klasę AddTransactionDialog
        dialog = AddTransactionDialog(self.finance)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        dialog.exec()

        # Korzystamy z funkcji refresh_dashboard, do odświeżenia dashboardu
        self.refresh_dashboard()

    # Tworzymy funkcje do odświeżania dashboardu
    def refresh_dashboard(self):
        # Ustawiamy na nowo wszystkie wartości widgetów
        self.balance_label.setText(f"Saldo: {self.finance.return_balance()}zł")

        self.income_label.setText(f"Wpłaty: {self.finance.return_income()}zł")

        self.expense_label.setText(f"Wydatki: {self.finance.return_expense()}zł")

        # Resetujemy liczbę wierszy
        self.history_table.setRowCount(0)

        # Importujemy wszystkie transakcje, korzystając z funkcji show_history()
        transactions = self.finance.show_history()

        # Iterujemy przez wszystkie transakcje, aby dodać je do tabeli z ostatnimi transakcjami
        for transaction in transactions:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            amount = abs(transaction[1])
            self.history_table.setItem(row, 0, QTableWidgetItem(str(amount)))
            self.history_table.setItem(row, 1, QTableWidgetItem(str(transaction[2])))
            type = "wydatek" if transaction[3] == "expense" else "przychód"
            self.history_table.setItem(row, 2, QTableWidgetItem(type))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(transaction[4])))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

