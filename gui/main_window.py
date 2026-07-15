from finance.finance import Finance
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QFont
from gui.standing_orders.standing_orders import StandingOrders
from gui.tranasactions.add_transaction_dialog import AddTransactionDialog
from gui.tranasactions.transaction_history import TransactionHistory
from gui.charts import Charts
from finance.recurring import Recurring
from gui.standing_orders.add_standing_order_dialog import AddStandingOrderDialog
from finance.savings import Savings
from gui.savings_goals.savings_goals import SavingsGoals
from gui.savings_goals.add_savings_goal_dialog import AddSavingsGoalDialog

class MainWindow(QMainWindow):
    def __init__(self):
        # Inicjalizacja klasy nadrzędnej, bez której program nie będzie poprawnie działał
        super().__init__()

        # Inicjalizujemy klasę finance
        self.finance = Finance()

        # Inicjalizujemy klasę recurring
        self.recurring = Recurring()

        # Inicjalizujemy klasę savings
        self.savings = Savings()

        # Sprawdzamy, czy jakieś stałe transakcje mają dziś miejsce
        self.recurring.process_recurring_transaction()

        # Ustawiamy tytuł okna aplikacji
        self.setWindowTitle("Financial tracker")

        # Ustawiamy rozmiar okna
        self.setGeometry(100, 200, 1500, 800)

        # Blokujemy możliwość powiększania okna, powyżej określonych rozmiarów
        self.setFixedSize(1500, 800)

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
        self.add_button = QPushButton("Dodaj transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.add_button.clicked.connect(self.open_add_transaction_dialog)

        # Dodajemy przycisk "Dodaj transakcje" do layoutu na zakładki
        self.tab_layout.addWidget(self.add_button)

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

        # Dodajemy filter_button do layoutu na zakładki
        self.tab_layout.addWidget(self.filter_button)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na False
        self.edit_button.setVisible(False)

        self.delete_button.setVisible(False)

        self.filter_button.setVisible(False)

        # Dodajemy przycisk "Dodaj transakcje" dla cyklicznych transakcji
        self.so_add_button = QPushButton("Dodaj stałą transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.so_add_button.clicked.connect(self.on_so_add_clicked)

        # Dodajemy przycisk "Dodaj transakcje" dla cyklicznych transakcji do layoutu na zakładki
        self.tab_layout.addWidget(self.so_add_button)

        # Dodajemy przycisk "Edytuj transakcję" dla cyklicznych transakcji
        self.so_edit_button = QPushButton("Edytuj stałą transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.so_edit_button.clicked.connect(self.on_so_edit_clicked)

        # Dodajemy edit_button dla cyklicznych transakcji do layoutu na zakładki
        self.tab_layout.addWidget(self.so_edit_button)

        # Dodajemy przycisk "Usuń transakcję" dla cyklicznych transakcji
        self.so_delete_button = QPushButton("Usuń stałą transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.so_delete_button.clicked.connect(self.on_so_delete_clicked)

        # Dodajemy delete_button do layoutu dla cyklicznych transakcji na zakładki
        self.tab_layout.addWidget(self.so_delete_button)

        # Dodajemy przycisk "Filtruj transakcję" dla cyklicznych transakcji
        self.so_filter_button = QPushButton("Filtruj stałe transakcje")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.so_filter_button.clicked.connect(self.on_so_filter_clicked)

        # Dodajemy filter_button dla cyklicznych transakcji do layoutu na zakładki
        self.tab_layout.addWidget(self.so_filter_button)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" dla cyklicznych transakcji na False
        self.so_add_button.setVisible(False)

        self.so_edit_button.setVisible(False)

        self.so_delete_button.setVisible(False)

        self.so_filter_button.setVisible(False)

        # Dodajemy przycisk "Dodaj transakcje" dla celów osczędnościowych
        self.sg_add_button = QPushButton("Dodaj cel oszczędnościowy")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.sg_add_button.clicked.connect(self.on_sg_add_clicked)

        # Dodajemy przycisk "Dodaj transakcje" dla celów osczędnościowych do layoutu na zakładki
        self.tab_layout.addWidget(self.sg_add_button)

        # Dodajemy przycisk "Edytuj transakcję" dla celów osczędnościowych
        self.sg_edit_button = QPushButton("Edytuj cel osczędnościowy")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.sg_edit_button.clicked.connect(self.on_sg_edit_clicked)

        # Dodajemy edit_button dla celów osczędnościowych do layoutu na zakładki
        self.tab_layout.addWidget(self.sg_edit_button)

        # Dodajemy przycisk "Usuń transakcję" dla celów osczędnościowych
        self.sg_delete_button = QPushButton("Usuń cel osczędnościowy")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        self.sg_delete_button.clicked.connect(self.on_sg_delete_clicked)

        # Dodajemy delete_button do layoutu dla celów osczędnościowych na zakładki
        self.tab_layout.addWidget(self.sg_delete_button)

        # Ustawiamy widoczność przycisków "Dodaj cel osczędnościowy", "Usuń cel osczędnościowy" i "Edytuj cel osczędnościowy" dla celów osczędnościowych na False
        self.sg_add_button.setVisible(False)

        self.sg_edit_button.setVisible(False)

        self.sg_delete_button.setVisible(False)

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

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        cyclical_button.clicked.connect(self.show_standing_orders)

        # Dodajemy cyclical_button do layoutu na zakładki
        self.tab_layout.addWidget(cyclical_button)

        # Dodajemy przycisk "Oszczędności"
        savings_button = QPushButton("Oszczędności")

        # Korzystamy z funkcji clicked, która wykonuje konkretną funkcję po kliknięciu danego przycisku, korzystamy z niej jako referencji, czyli informujemy program o tym, że ma się ona wykonać dopiero wtedy, kiedy zostanie spełniony jakiś warunek
        savings_button.clicked.connect(self.show_savings_goals)

        # Dodajemy savings_button do layoutu na zakładki
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
        add = AddTransactionDialog(self.finance, self.savings)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        add.exec()

        if self.current_tab == "Dashboard":
            # Korzystamy z funkcji refresh_dashboard, do odświeżenia dashboardu
            self.refresh_dashboard()
        elif self.current_tab == "Transactions":
            # Korzystamy z funkcji refresh_history_table, do odświeżenia tabeli z historią transakcji
            self.history.refresh_history_table()

    # Ta funkcji wróci nam do głównego widgetu dashboard, o ile wszystkie wymagane warunki zostaną spełnione
    def show_dashboard(self):
        # Sprawdzamy aktualnie otwartą zakładkę
        if self.current_tab == "Dashboard":
            return
        elif self.current_tab == "Transactions":
            # Ustawiamy widoczność self.history na False
            self.history.setVisible(False)
        elif self.current_tab == "Standing Orders":
            # Ustawiamy widoczność self.standing_orders na False
            self.standing_orders.setVisible(False)
        elif self.current_tab == "Savings Goals":
            # Ustawiamy widoczność self.savings_goals na False
            self.savings_goals.setVisible(False)

        # Ustawiamy widoczność widgetu na treść i przycisku "Dodaj transakcje" na True
        self.content_widget.setVisible(True)

        self.add_button.setVisible(True)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na False
        self.edit_button.setVisible(False)

        self.delete_button.setVisible(False)

        self.filter_button.setVisible(False)

        # Ustawiamy widoczność przycisków "Dodaj transakcje", "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" dla cyklicznych transakcji na False
        self.so_add_button.setVisible(False)

        self.so_edit_button.setVisible(False)

        self.so_delete_button.setVisible(False)

        self.so_filter_button.setVisible(False)

        # Ustawiamy widoczność przycisków "Dodaj cel osczędnościowy", "Usuń cel osczędnościowy" i "Edytuj cel osczędnościowy" dla celów osczędnościowych na False
        self.sg_add_button.setVisible(False)

        self.sg_edit_button.setVisible(False)

        self.sg_delete_button.setVisible(False)

        # Odświeżamy dashboard
        self.refresh_dashboard()

        # Ustawiamy aktualną zakładke
        self.current_tab = "Dashboard"

    # Ta funkcja ukryje nam wszystkie widgety z dashboardu i zainicjalizuje klasę TransactionHistory
    def show_transactions(self):
        if self.current_tab == "Transactions":
            return
        elif self.current_tab == "Standing Orders":
            self.standing_orders.setVisible(False)
        elif self.current_tab == "Savings Goals":
            self.savings_goals.setVisible(False)

        # Ustawiamy widoczność widgetu na treść na False
        self.content_widget.setVisible(False)

        # Sprawdzamy, czy obiekt history już istnieje przy pomocy wbudowanej w PyQt6 funkcji hasattr
        if hasattr(self, "history"):
            # Jeżeli istnieje zmieniamy tylko jego widoczność
            self.history.setVisible(True)
        else:
            # Inicjalizujemy klasę TransactionHistory
            self.history = TransactionHistory(self.finance)

            # Dodajemy klasę history, do głównego layoutu
            self.layout.addWidget(self.history)

        # Ustawiamy aktualną zakładkę
        self.current_tab = "Transactions"

        # Odświeżamy tabele z transakcjami
        self.history.refresh_history_table()

        # Ustawiamy widoczność przycisków "Dodaj transakcje", "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na True
        self.add_button.setVisible(True)

        self.edit_button.setVisible(True)

        self.delete_button.setVisible(True)

        self.filter_button.setVisible(True)

        # Ustawiamy widoczność przycisków "Dodaj transakcje", "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" dla cyklicznych transakcji na False
        self.so_add_button.setVisible(False)

        self.so_edit_button.setVisible(False)

        self.so_delete_button.setVisible(False)

        self.so_filter_button.setVisible(False)

        # Ustawiamy widoczność przycisków "Dodaj cel osczędnościowy", "Usuń cel osczędnościowy" i "Edytuj cel osczędnościowy" dla celów osczędnościowych na False
        self.sg_add_button.setVisible(False)

        self.sg_edit_button.setVisible(False)

        self.sg_delete_button.setVisible(False)


    # Ta funkcja ukryje nam wszystkie widgety z dashboardu i zainicjalizuje klasę StandingOrders
    def show_standing_orders(self):
        if self.current_tab == "Standing Orders":
            return
        elif self.current_tab == "Transactions":
            self.history.setVisible(False)
        elif self.current_tab == "Savings Goals":
            self.savings_goals.setVisible(False)

        # Ustawiamy widoczność widgetu na treść na False
        self.content_widget.setVisible(False)

        # Sprawdzamy, czy obiekt standing_orders już istnieje przy pomocy wbudowanej w PyQt6 funkcji hasattr
        if hasattr(self, "standing_orders"):
            # Jeżeli istnieje zmieniamy tylko jego widoczność
            self.standing_orders.setVisible(True)
        else:
            # A jeżeli nie istnieje, to tworzymy go inicjalizując klasę StandingOrders
            self.standing_orders = StandingOrders(self.recurring)

            # Dodajemy klasę standing_orders, do głównego layoutu
            self.layout.addWidget(self.standing_orders)

        self.current_tab = "Standing Orders"

        # Ustawiamy widoczność standardowego przycisku "Dodaj transakcję", "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na False
        self.add_button.setVisible(False)

        self.edit_button.setVisible(False)

        self.delete_button.setVisible(False)

        self.filter_button.setVisible(False)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" dla cyklicznych transakcji na True
        self.so_add_button.setVisible(True)

        self.so_edit_button.setVisible(True)

        self.so_delete_button.setVisible(True)

        self.so_filter_button.setVisible(True)

        # Ustawiamy widoczność przycisków "Dodaj cel osczędnościowy", "Usuń cel osczędnościowy" i "Edytuj cel osczędnościowy" dla celów osczędnościowych na False
        self.sg_add_button.setVisible(False)

        self.sg_edit_button.setVisible(False)

        self.sg_delete_button.setVisible(False)


    # Ta funkcja ukryje nam wszystkie widgety z dashboardu i zainicjalizuje klasę StandingOrders
    def show_savings_goals(self):
        if self.current_tab == "Savings Goals":
            return
        elif self.current_tab == "Standing Orders":
            self.standing_orders.setVisible(False)
        elif self.current_tab == "Transactions":
            self.history.setVisible(False)

        # Ustawiamy widoczność widgetu na treść na False
        self.content_widget.setVisible(False)

        # Sprawdzamy, czy obiekt savings_goals już istnieje przy pomocy wbudowanej w PyQt6 funkcji hasattr
        if hasattr(self, "savings_goals"):
            # Jeżeli istnieje zmieniamy tylko jego widoczność
            self.savings_goals.setVisible(True)

            # Odświerzamy zakładke z celami osczędnościowymi
            self.savings_goals.refresh_savings_goals_table()
        else:
            # A jeżeli nie istnieje, to tworzymy go inicjalizując klasę SavingsGoals
            self.savings_goals = SavingsGoals(self.savings)

            # Dodajemy klasę savings_goals, do głównego layoutu
            self.layout.addWidget(self.savings_goals)

        self.current_tab = "Savings Goals"

        # Ustawiamy widoczność standardowego przycisku "Dodaj transakcję", "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" na False
        self.add_button.setVisible(False)

        self.edit_button.setVisible(False)

        self.delete_button.setVisible(False)

        self.filter_button.setVisible(False)

        # Ustawiamy widoczność przycisków "Usuń transakcje", "Edytuj transakcje" i "Filtruj transakcje" dla cyklicznych transakcji na False
        self.so_add_button.setVisible(False)

        self.so_edit_button.setVisible(False)

        self.so_delete_button.setVisible(False)

        self.so_filter_button.setVisible(False)

        # Ustawiamy widoczność przycisków "Dodaj transakcje", "Edytuj transakcje" i "Usuń transakcje" dla celów oszczędnościowych na True
        self.sg_add_button.setVisible(True)

        self.sg_edit_button.setVisible(True)

        self.sg_delete_button.setVisible(True)

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

    # Ta funkcji pozwoli nam uniknąć otwierania okna dodawania stałej transakcji za każdym razem po włączeniu programu, korzystamy od razu z klasy AddStandingOrderDialog, bez integracji z klasą StandingOrders
    def on_so_add_clicked(self):
        if self.current_tab == "Dashboard" or self.current_tab == "Transactions":
            return

        # Inicjalizujemy klasę AddStandingOrderDialog
        so_add = AddStandingOrderDialog(self.recurring)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        so_add.exec()

        # Odświeżamy tabele na stałe transakcje
        self.standing_orders.refresh_standing_orders_table()

    def on_so_delete_clicked(self):
        if self.current_tab == "Dashboard" or self.current_tab == "Transactions":
            return

        # Wywołujemy usunięcie stałej transakcji
        self.standing_orders.delete_standing_order()

    def on_so_edit_clicked(self):
        if self.current_tab == "Dashboard" or self.current_tab == "Transactions":
            return

        # Wywołujemy okno edycji stałej transakcji
        self.standing_orders.open_edit_dialog()

    def on_so_filter_clicked(self):
        if self.current_tab == "Dashboard" or self.current_tab == "Transactions":
            return

        # Wywołujemy okno filtracji stałych transakcji
        self.standing_orders.open_filter_dialog()

    # Ta funkcji pozwoli nam uniknąć otwierania okna dodawania celu oszczędnościowego za każdym razem po włączeniu programu, korzystamy od razu z klasy AddSavingsGoalDialog, bez integracji z klasą SavingsGoals
    def on_sg_add_clicked(self):
        # Inicjalizujemy klasę AddSavingsGoalDialog
        sg_add = AddSavingsGoalDialog(self.savings)

        # Korzystamy z metody QDialog exec(), która pozwoli nam wyświetlić formularz dodawania transakcji, blokująć przy tym korzystanie z wszytkich innych okien aplikacji
        sg_add.exec()

        # Odświeżamy tabele na cele osczędnościowe
        self.savings_goals.refresh_savings_goals_table()

    def on_sg_edit_clicked(self):
        # Wywołujemy okno edycji celu osczędnościowego
        self.savings_goals.open_edit_dialog()

    def on_sg_delete_clicked(self):
        # Wywołujemy usunięcie celu osczędnościowego
        self.savings_goals.delete_savings_goal()

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

