import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../lab03'))

from typing import List
from app import BankApp
from exceptions import ItemNotFoundError, DuplicateItemError, InvalidInputError
from models import BankAccount, SavingsAccount, CreditAccount

class ConsoleInterface:
    def __init__(self, app: BankApp):
        self.app = app

    def display_menu(self):
        print("\n" + "="*50)
        print("    БАНКОВСКАЯ СИСТЕМА")
        print("="*50)
        print("1. Показать все счета")
        print("2. Добавить счёт")
        print("3. Удалить счёт")
        print("4. Внести депозит")
        print("5. Снять средства")
        print("6. Начислить проценты на сберегательные счета")
        print("7. Найти счёт по владельцу")
        print("8. Фильтровать по балансу")
        print("9. Фильтровать по типу")
        print("10. Сортировка")
        print("11. Установить стратегию комиссии")
        print("12. Общий баланс")
        print("0. Выйти и сохранить")
        print("="*50)

    def get_int_input(self, prompt, min_val=None, max_val=None):
        while True:
            try:
                val = int(input(prompt))
                if min_val is not None and val < min_val:
                    raise InvalidInputError(f"Число должно быть ≥ {min_val}")
                if max_val is not None and val > max_val:
                    raise InvalidInputError(f"Число должно быть ≤ {max_val}")
                return val
            except ValueError:
                print("Ошибка: введите целое число")
            except InvalidInputError as e:
                print(f"Ошибка: {e}")

    def get_float_input(self, prompt, positive=True):
        while True:
            try:
                val = float(input(prompt))
                if positive and val <= 0:
                    raise InvalidInputError("Сумма должна быть положительной")
                return val
            except ValueError:
                print("Ошибка: введите число")
            except InvalidInputError as e:
                print(f"Ошибка: {e}")

    def get_string_input(self, prompt, allow_empty=False):
        while True:
            val = input(prompt).strip()
            if val or allow_empty:
                return val
            print("Ошибка: поле не может быть пустым")

    def show_accounts(self, accounts):
        if not accounts:
            print("Счета не найдены.")
        else:
            for acc in accounts:
                print(acc)

    def add_account_flow(self):
        print("\n--- Добавление счёта ---")
        owner = self.get_string_input("Владелец: ")
        print("Тип: 1 - обычный, 2 - сберегательный, 3 - расчётный")
        typ = self.get_int_input("Выбор: ", 1, 3)
        balance = self.get_float_input("Начальный баланс: ", positive=False)
        try:
            if typ == 1:
                self.app.add_account('basic', owner, balance)
            elif typ == 2:
                rate_percent = self.get_float_input("Процентная ставка (0..10): ", positive=False)
                if not (0 <= rate_percent <= 10):
                    raise InvalidInputError("Ставка должна быть от 0 до 10")
                rate = rate_percent / 100.0
                self.app.add_account('savings', owner, balance, interest_rate=rate)
            else:
                limit = self.get_float_input("Лимит овердрафта: ", positive=False)
                self.app.add_account('credit', owner, balance, credit_limit=limit)
            print("✅ Счёт добавлен")
        except (DuplicateItemError, ValueError, InvalidInputError) as e:
            print(f"❌ Ошибка: {e}")

    def remove_account_flow(self):
        print("\n--- Удаление счёта ---")
        owner = self.get_string_input("Владелец счёта: ")
        confirm = input(f"Удалить счёт владельца '{owner}'? (y/n): ").lower()
        if confirm != 'y':
            print("Удаление отменено")
            return
        try:
            self.app.remove_account(owner)
            print("✅ Счёт удалён")
        except ItemNotFoundError as e:
            print(f"❌ {e}")

    def deposit_flow(self):
        print("\n--- Внесение депозита ---")
        owner = self.get_string_input("Владелец счёта: ")
        amount = self.get_float_input("Сумма: ")
        try:
            self.app.deposit_to_account(owner, amount)
            print("✅ Депозит выполнен")
        except ItemNotFoundError as e:
            print(f"❌ {e}")

    def withdraw_flow(self):
        print("\n--- Снятие средств ---")
        owner = self.get_string_input("Владелец счёта: ")
        amount = self.get_float_input("Сумма: ")
        try:
            self.app.withdraw_from_account(owner, amount)
            print("✅ Снятие выполнено")
        except (ItemNotFoundError, ValueError) as e:
            print(f"❌ Ошибка: {e}")

    def find_account_flow(self):
        print("\n--- Поиск счёта по владельцу ---")
        owner = self.get_string_input("Владелец: ")
        acc = self.app.find_account(owner)
        if acc is None:
            print("❌ Счёт не найден")
        else:
            print(acc)

    def filter_by_balance_flow(self):
        print("\n--- Фильтрация по балансу ---")
        min_bal = self.get_float_input("Минимальный баланс: ", positive=False)
        max_bal = self.get_float_input("Максимальный баланс: ", positive=False)
        if min_bal > max_bal:
            print("❌ Ошибка: min > max")
            return
        accounts = self.app.filter_by_balance(min_bal, max_bal)
        self.show_accounts(accounts)

    def filter_by_type_flow(self):
        print("\n--- Фильтрация по типу счёта ---")
        print("1 - Обычный\n2 - Сберегательный\n3 - Расчётный")
        typ = self.get_int_input("Выбор: ", 1, 3)
        if typ == 1:
            accounts = self.app.filter_by_type(BankAccount)
        elif typ == 2:
            accounts = self.app.filter_by_type(SavingsAccount)
        else:
            accounts = self.app.filter_by_type(CreditAccount)
        self.show_accounts(accounts)

    def sort_flow(self):
        print("\n--- Сортировка ---")
        print("1 - По балансу (возр.)")
        print("2 - По балансу (убыв.)")
        print("3 - По владельцу (возр.)")
        print("4 - По владельцу (убыв.)")
        print("5 - По типу, затем по балансу")
        choice = self.get_int_input("Выбор: ", 1, 5)
        if choice == 1:
            self.app.sort_by_balance(False)
        elif choice == 2:
            self.app.sort_by_balance(True)
        elif choice == 3:
            self.app.sort_by_owner(False)
        elif choice == 4:
            self.app.sort_by_owner(True)
        else:
            self.app.sort_by_type_then_balance(False)
        print("✅ Сортировка выполнена")

    def set_fee_strategy_flow(self):
        print("\n--- Установка стратегии комиссии ---")
        owner = self.get_string_input("Владелец счёта: ")
        print("Стратегия: 1 - нет, 2 - фиксированная, 3 - процентная")
        choice = self.get_int_input("Выбор: ", 1, 3)
        value = 0.0
        if choice == 2:
            value = self.get_float_input("Фиксированная сумма: ")
        elif choice == 3:
            value = self.get_float_input("Процент (0..100): ")
        try:
            if choice == 1:
                self.app.set_fee_strategy(owner, 'no')
            elif choice == 2:
                self.app.set_fee_strategy(owner, 'flat', value)
            else:
                self.app.set_fee_strategy(owner, 'percent', value)
            print("✅ Стратегия установлена")
        except ItemNotFoundError as e:
            print(f"❌ {e}")

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_int_input("Ваш выбор: ", 0, 12)
            if choice == 0:
                break
            elif choice == 1:
                self.show_accounts(self.app.get_all_accounts())
            elif choice == 2:
                self.add_account_flow()
            elif choice == 3:
                self.remove_account_flow()
            elif choice == 4:
                self.deposit_flow()
            elif choice == 5:
                self.withdraw_flow()
            elif choice == 6:
                self.app.apply_interest_to_savings()
                print("✅ Проценты начислены")
            elif choice == 7:
                self.find_account_flow()
            elif choice == 8:
                self.filter_by_balance_flow()
            elif choice == 9:
                self.filter_by_type_flow()
            elif choice == 10:
                self.sort_flow()
            elif choice == 11:
                self.set_fee_strategy_flow()
            elif choice == 12:
                total = self.app.total_balance()
                print(f"Общий баланс: {total:.2f} руб.")
            input("\nНажмите Enter...")