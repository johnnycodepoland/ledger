import json

class Utils:
    # Funkcja zapisująca transakcję, do pliku json
    def save_transactions(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    # Funkcja ładująca wszystkie transakcje, z pliku json
    def load_transactions(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            # Słownik składany, który pozwala nam zwięźle i szybko przekształcić słownik w inty
            data["operations"] = {int(k): v for k, v in data["operations"].items()}
            return data
