from utils import Utils

class Finance:
    def __init__(self):
        # Zmienna monitorująca aktualne saldo
        self.balance = 0

        # Słownik zapisujący wszystkie transakcje
        self.transactions = {}

        # Wywołanie potrzebnych klas
        self.utils = Utils()

        # Tutaj próbujemy wczytać zmienne z pliku
        try:
            data = self.utils.load_transactions("data.json")
            self.balance = data["balance"]
            self.transactions = data["transactions"]
        except:
            pass

    # Funkcja dodająca transakcje
    def add_transcation(self, amount, date, transcation_type, transaction_category):
        self.transactions[len(self.transactions) +1] = {"amount": amount, "date": date, "type": transcation_type, "category": transaction_category}
        self.balance += amount
        self.utils.save_transactions({"balance": self.balance, "transactions": self.transactions}, "data.json")

    # Funkcja wypisująca aktulane saldo
    def show_balance(self):
        print(f"Saldo: {self.balance}")

    # Funkcja wypisująca historię transakcji
    def show_history(self, category=None, date=None):
        for key in self.transactions:
            operation = self.transactions[key]
            if category is not None and category not in operation["category"]:
                continue
            if date is not None and date not in operation["date"]:
                continue
            transaction_type = "wydatek" if operation['type'] == "expense" else "przychód"
            print(
                f"ID transakcji: {key}, Kwota: {operation['amount']}, Typ: {transaction_type}, Data: {operation['date']}, Kategoria: {operation['category']}")

    # Funkcja umożliwiająca edycję transakcji
    def edit_transaction(self, id, amount=None, date=None, transaction_type=None, transaction_category=None):
        if id in self.transactions:
            if amount is not None:
                if self.transactions[id]["type"] == "expense":
                    amount = -amount
                self.transactions[id]["amount"] = amount
            if date is not None:
                self.transactions[id]["date"] = date
            if transaction_type is not None:
                self.transactions[id]["type"] = transaction_type
            if transaction_category is not None:
                self.transactions[id]["category"] = transaction_category
            self.utils.save_transactions({"balance": self.balance, "transactions": self.transactions}, "data.json")

    def delete_transaction(self, id):
        if id in self.transactions:
            amount = self.transactions[id]["amount"]
            # Korzystamy z funkcji abs(x) do wyliczenia wartości bezwzględnej z kwoty transakcji, którą usuwamy
            if self.transactions[id]["type"] == "expense":
                self.balance += abs(amount)
            else:
                self.balance -= abs(amount)
            del self.transactions[id]
            self.utils.save_transactions({"balance": self.balance, "transactions": self.transactions}, "data.json")