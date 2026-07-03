from finance.finance import Finance
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QFont
from gui.add_transaction_dialog import AddTransactionDialog
from gui.transaction_history import TransactionHistory
from gui.charts import Charts

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

        # Zapisujemy aktualną zakładke
        self.current_tab = "Dashboard"

    def create_navigation(self):
        # Tworzymy widget na zakładki
        tab_widget = QWidget()

        # Tworzymy layout dla widgetu na zakładki
        self.tab_layout = QHBoxLayout(tab_widget)

        # Dodajemy przycisk "Dodaj transakcje"
        transaction_button = QPushButton("Dodaj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        transaction_button.clicked.connect(self.open_add_transaction_dialog)

        # Dodajemy przycisk "Dodaj transakcje" do layoutu na zakładki
        self.tab_layout.addWidget(transaction_button)

        # Dodajemy przycisk "Edytuj transakcję"
        self.edit_button = QPushButton("Edytuj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.edit_button.clicked.connect(self.on_edit_clicked)

        # Dodajemy edit_button do layoutu na zakładki
        self.tab_layout.addWidget(self.edit_button)

        # Dodajemy przycisk "Usuń transakcję"
        self.delete_button = QPushButton("Usuń transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.delete_button.clicked.connect(self.on_delete_clicked)

        # Dodajemy delete_button do layoutu na zakładki
        self.tab_layout.addWidget(self.delete_button)

        # Dodajemy przycisk "Filtruj transakcję"
        self.filter_button = QPushButton("Filtruj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.filter_button.clicked.connect(self.on_filter_clicked)

        # Dodajemy delete_button do layoutu na zakładki
        self.tab_layout.addWidget(self.filter_button)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na False
        self.edit_button.setVisible(False)

        self.delete_button.setVisible(False)

        self.filter_button.setVisible(False)

        # Przesuwamy przycisk na maksa w lewo
        self.tab_layout.addStretch()

        # Dodajemy przycisk "Dashboard"
        dashboard_button = QPushButton("Dashboard")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        dashboard_button.clicked.connect(self.show_dashboard)

        # Dodajemy dashboard_button do layoutu na zakładki
        self.tab_layout.addWidget(dashboard_button)

        # Dodajemy przycisk "Transakcje"
        transactions_button = QPushButton("Transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        transactions_button.clicked.connect(self.show_transactions)

        # Dodajemy transactions_button do layoutu na zakładki
        self.tab_layout.addWidget(transactions_button)

        # Dodajemy przycisk "Cykliczne"
        cyclical_button = QPushButton("Cykliczne")

        # Dodajemy cyclical_button do layoutu na zakładki
        self.tab_layout.addWidget(cyclical_button)

        # Dodajemy przycisk "Oszczędności"
        savings_button = QPushButton("Oszczędności")

        # Dodajemy report_button do layoutu na zakładki
        self.tab_layout.addWidget(savings_button)

        # Ustawiamy maksymalną wielkość dla widgetu, tab_widget
        tab_widget.setMaximumHeight(50)

        # Dodajemy tab_widget do głównego layoutu
        self.layout.addWidget(tab_widget)

    # Główny dashboard
    def create_dashboard(self):
        # Tworzymy widget na treść
        self.content_widget = QWidget()

        # Tworzymy layout dla widgetu na treść
        self.content_layout = QVBoxLayout(self.content_widget)

        # Dodajemy widget na treść do głównego layoutu
        self.layout.addWidget(self.content_widget)

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
        self.balance_label.setFixedSize(600, 150)

        # Ustawiamy czcionkę i jej rozmiar, dla widgetu na balans
        self.balance_label.setFont(QFont("San Francisco", 70))

        # Dodajemy widget na wpłaty do górnego widgetu na treść
        top_layout.addWidget(self.balance_label)

        # Tworzymy kontener na wydatki
        expense_container = QWidget()

        # Tworzymy layout na "kontener" na wpłaty
        expense_layout = QVBoxLayout(expense_container)

        # Ustawiamy customową odległość między widgetami
        expense_layout.setSpacing(0)

        # Tworzymy widget na nazwę miesiąca
        month_widget_expense = QLabel("Wydatki (miesiąc):")

        # Tworzymy widget na kwotę wpłat za dany miesiąc
        self.amount_widget_expense = QLabel(f"{self.finance.return_expense()}zł")

        # Ustawiamy styl kontenera na wpłaty
        expense_container.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")

        # Dodajemy widget na nazwę miesiąca do layoutu "kontenera" na wpłaty
        expense_layout.addWidget(month_widget_expense)

        # Dodajemy widget na kwotę do layoutu "kontenera" na wpłaty
        expense_layout.addWidget(self.amount_widget_expense)

        # Ustawiamy wielkość "kontenera" na wpłaty
        expense_container.setFixedSize(400, 150)

        # Ustawiamy czcionkę i jej rozmiar, dla widgetu na miesiąc
        month_widget_expense.setFont(QFont("San Francisco", 30))

        # Ustawiamy czcionkę i jej rozmiar, dla widgetu na kwotę
        self.amount_widget_expense.setFont(QFont("San Francisco", 40))

        # Dodajemy "kontener" na wpłaty do górnego widgetu na treść
        top_layout.addWidget(expense_container)

        # Tworzymy kontener na wpłaty
        income_container = QWidget()

        # Tworzymy layout na "kontener" na wpłaty
        income_layout = QVBoxLayout(income_container)

        # Ustawiamy customową odległość między widgetami
        income_layout.setSpacing(0)

        # Tworzymy widget na nazwę miesiąca
        month_widget_income = QLabel("Wpłaty (miesiąc):")

        # Tworzymy widget na kwotę wpłat za dany miesiąc
        self.amount_widget_income = QLabel(f"{self.finance.return_income()}zł")

        # Ustawiamy styl kontenera na wpłaty
        income_container.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")

        # Dodajemy widget na nazwę miesiąca do layoutu "kontenera" na wpłaty
        income_layout.addWidget(month_widget_income)

        # Dodajemy widget na kwotę do layoutu "kontenera" na wpłaty
        income_layout.addWidget(self.amount_widget_income)

        # Ustawiamy wielkość "kontenera" na wpłaty
        income_container.setFixedSize(400, 150)

        # Ustawiamy czcionkę i jej rozmiar, dla widgetu na miesiąc
        month_widget_income.setFont(QFont("San Francisco", 30))

        # Ustawiamy czcionkę i jej rozmiar, dla widgetu na kwotę
        self.amount_widget_income.setFont(QFont("San Francisco", 40))

        # Dodajemy "kontener" na wpłaty do górnego widgetu na treść
        top_layout.addWidget(income_container)

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

        # Tworzymy "kontener" na wykres, aby uniknąć błędu ze stylem widgetu na transakcje, który jest w formie tabeli
        charts_container = QWidget()

        # Ustawiamy layout dla "kontenera" na historię transakcji
        charts_layout = QVBoxLayout(charts_container)

        # Ustawiamy wielkość "kontenera" na wykresy
        charts_container.setFixedSize(806, 480)

        # Dodajemy nazwę obiektu, dla charts_container, aby uniknąć przekazywania stylu na "dzieci" table_container
        charts_container.setObjectName("charts_container")

        # Ustawiamy styl, tylko dla charts_container bez przekazywania na jego "dzieci"
        charts_container.setStyleSheet("#charts_container {background-color: white; border-radius: 10px; padding: 10px;}")

        # Tworzymy widget na wykres
        self.chart = Charts()

        # Rysujemy słupki na wykresie
        self.chart.create_bar_chart(self.finance.return_income(), self.finance.return_expense())

        # Dodajemy widget na wykres do layoutu na wykresy
        charts_layout.addWidget(self.chart)

        # Dodajemy "kontener" na wykresy, do dolnego layoutu
        bottom_layout.addWidget(charts_container)

        # Wypychamy dolną część treści na maksa w lewo
        bottom_layout.addStretch()

    # Ta funkcji pozwoli nam uniknąć otwierania okna dodawania transakcji za każdym razem po włączeniu programu
    def open_add_transaction_dialog(self):
        # Inicjalizujemy klasę AddTransactionDialog
        add = AddTransactionDialog(self.finance)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        add.exec()

        if self.current_tab == "Dashboard":
            # Korzystamy z funkcji refresh_dashboard, do odświeżenia dashboardu
            self.refresh_dashboard()
        elif self.current_tab == "Transactions":
            # Korzystamy z funkcji refresh_history_table, do odświeżenia tabeli z historią transakcji
            self.history.refresh_history_table()

    # Ta funkcja usunie nam wszystkie widgety z dashboardu i zainicjalizuje klasę TransactionHistory
    def show_transactions(self):
        if self.current_tab == "Transactions":
            return

        # Ustawiamy widoczność widgetu na treść na False
        self.content_widget.setVisible(False)

        # Inicjalizujemy klasę TransactionHistory
        self.history = TransactionHistory(self.finance)

        # Dodajemy klasę history, do głównego layoutu
        self.layout.addWidget(self.history)

        self.current_tab = "Transactions"

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na True
        self.edit_button.setVisible(True)

        self.delete_button.setVisible(True)

        self.filter_button.setVisible(True)

    # Ta funkcji wróci nam do głównego widgetu dashboard, o ile wszystkie wymagane warunki zostaną spełnione
    def show_dashboard(self):
        # Sprawdzamy aktualnie otwartą zakładkę
        if self.current_tab == "Dashboard":
            return

        # Ustawiamy widoczność self.history na False
        self.history.setVisible(False)

        # Ustawiamy widoczność widgetu na treść na True
        self.content_widget.setVisible(True)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na False
        self.edit_button.setVisible(False)

        self.delete_button.setVisible(False)

        self.filter_button.setVisible(False)

        # Odświeżamy dashboard
        self.refresh_dashboard()

        # Ustawiamy aktualną zakładke
        self.current_tab = "Dashboard"

    # Ta funkcji usunie nam wybraną transakcję, tylko jeśli będziemy znajdować się w oknie "Transactions"
    def on_delete_clicked(self):
        # Sprawdzamy aktualnie otwartą zakładkę
        if self.current_tab == "Dashboard":
            return

        # Wywołujemy usunięcie transakcji
        self.history.delete_transaction()

    def on_edit_clicked(self):
        # Sprawdzamy aktualnie otwartą zakładkę
        if self.current_tab == "Dashboard":
            return

        # Wywołujemy okno do edycji transakcji
        self.history.open_edit_dialog()

    def on_filter_clicked(self):
        # Sprawdzamy aktualnie otwartą zakładkę
        if self.current_tab == "Dashboard":
            return

        # Wywołujemy okno do edycji transakcji
        self.history.open_filter_dialog()

    # Tworzymy funkcje do odświeżania dashboardu
    def refresh_dashboard(self):
        # Ustawiamy na nowo wszystkie wartości widgetów
        self.balance_label.setText(f"Saldo: {self.finance.return_balance()}zł")

        self.amount_widget_income.setText(f"{self.finance.return_income()}zł")

        self.amount_widget_expense.setText(f"{self.finance.return_expense()}zł")

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

        # Odświeżamy wykres
        self.chart.refresh_charts(self.finance.return_income(), self.finance.return_expense())

