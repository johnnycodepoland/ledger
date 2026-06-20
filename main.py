import datetime
from finance import Finance

if __name__ == "__main__":
    finance = Finance()
    while True:
        print("================================")
        print("  WITAJ W PANELU UŻYTKOWNIKA  ")
        print("================================")
        print("Wybierz jedną z poniższych opcji:")
        print("1. Wyświetl saldo")
        print("2. Wyświetl historię")
        print("3. Dodaj transakcję")
        print("4. Edytuj transakcje")
        print("5. Usuń transakcje")
        print("6. Zamknij program")

        choose = input("Wybierz akcję do wykonania: ")

        if choose == "1":
            finance.show_balance()
        elif choose == "2":
            while True:
                filter_by_category = input("Czy chcesz filtrować po kategorii (t/n): ")

                if filter_by_category == "t":
                    category = input("Podaj kategorie transakcji: ")
                    break
                elif filter_by_category == "n":
                    category = None
                    break
                else:
                    print("Podano niepoprawną opcję")

            while True:
                filter_by_date = input("Czy chcesz filtrować po dacie (t/n): ")

                if filter_by_date == "t":
                    while True:
                        try:
                            date = str(input("Podaj datę transakcji (YYYY-MM-DD): "))
                            datetime.datetime.strptime(date, "%Y-%m-%d")  # ta funkcja pozwala nam
                            break
                        except:
                            print("Podano niepoprawny format daty")
                    break
                elif filter_by_date == "n":
                    date = None
                    break
                else:
                    print("Podano niepoprawną opcję")
            finance.show_history(category, date)
        elif choose == "3":
            while True:
                transaction_type = input("Podaj typ transakcji (wydatek, przychód): ")

                if transaction_type == "wydatek":
                    transaction_type = "expense"
                    break
                elif transaction_type == "przychód":
                    transaction_type = "income"
                    break
                else:
                    print("Podano niepoprawny typ transakcji")
            try:
                amount = float(input("Podaj kwotę transakcji: "))
            except ValueError:
                print("Podaj poprawną kwotę transakcji")
                continue
            if transaction_type == "expense":
                amount = 0 - amount
            category = input("Podaj kategorie transakcji: ")
            finance.add_transcation(amount, str(datetime.date.today()), transaction_type, category)
        elif choose == "4":
            if not finance.transactions:
                print("Brak transakcji do edycji")
            else:
                finance.show_history()
                done = False
                while not done:
                    try:
                        id = int(input("Podaj id transakcji, którą chcesz edytować: "))
                    except ValueError:
                        continue
                    if id in finance.transactions:
                        while True:
                            category_of_edit = input("Podaj kategorie edycji (kwota, data, typ, kategoria): ")
                            if category_of_edit == "kwota":
                                try:
                                    amount = float(input("Podaj nową kwotę transakcji: "))
                                except ValueError:
                                    print("Podano niepoprawną kwotę transakcji")
                                    continue
                                finance.edit_transaction(id, amount)
                                done = True
                                break
                            elif category_of_edit == "data":
                                try:
                                    date = str(input("Podaj nową datę transakcji (YYYY-MM-DD): "))
                                    datetime.datetime.strptime(date, "%Y-%m-%d")  # ta funkcja pozwala nam
                                except:
                                    print("Podano niepoprawny format daty")
                                finance.edit_transaction(id, date)
                                done = True
                                break
                            elif category_of_edit == "typ":
                                transaction_type = input("Podaj nowy typ transakcji (wydatek, przychód): ")

                                if transaction_type == "wydatek":
                                    transaction_type = "expense"
                                elif transaction_type == "przychód":
                                    transaction_type = "income"
                                else:
                                    print("Podano niepoprawny typ transakcji")
                                finance.edit_transaction(id, transaction_type)
                                done = True
                                break
                            elif category_of_edit == "kategoria":
                                category = input("Podaj nową kategorie transakcji: ")
                                finance.edit_transaction(id, category)
                                done = True
                                break
                            else:
                                print("Podano niepoprawną kategorię edycji transakcji")
                    else:
                        print("Podano nie poprawne id transakcji")
        elif choose == "5":
            if not finance.transactions:
                print("Brak transakcji do usunięcia")
            else:
                finance.show_history()
                while True:
                    try:
                     id = int(input("Podaj id transakcji, którą chcesz edytować: "))
                    except ValueError:
                        continue
                    if id in finance.transactions:
                        finance.delete_transaction(id)
                        break
                    else:
                        print("Podano nie poprawne id transakcji")
        elif choose == "6":
            print("Program za chwilę się wyłączy...")
            break
        else:
            print("Nieznana opcja! Wybierz ponownie.")

