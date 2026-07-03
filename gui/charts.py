from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Charts(FigureCanvasQTAgg):
    def __init__(self):
        # Tworzymy obiekt wykresu, który będzie przechowywał wszystkie informacje o nim
        fig = Figure()

        # Dajemy informację do klasy nadrzędnej, że ma z tego wykresu utworzyć później widget
        super().__init__(fig)

        # Dodajemy osie do naszego wykresu, jako atrybut klasy, żeby móc potem na nich rysować
        self.axes = fig.add_subplot(111)

    # Tworzymy funkcję, która stworzy na wykres słupkowy
    def create_bar_chart(self, income, expense):
        # Dodajemy listę kolorów
        colors = ["green", "red"]

        # Tworzymy wykres słupkowy, najpierw podajemy etykiety słupków, a potem ich wartości
        self.axes.bar(["Przychody", "Wydatki"], [income, expense], color=colors)

    # Tworzymy funkcję, która wyczyści nam osię i narysuję je od nowa
    def refresh_charts(self, income, expense):
        # Czyścimy osię
        self.axes.clear()

        # Wywołujemy od nowa funkcję: create_bar_chart()
        self.create_bar_chart(income, expense)

        # Rysujemy od nowa wykresy, bez tego użytkownik dalej będzie widział to co było przed odświerzeniem
        self.draw()

