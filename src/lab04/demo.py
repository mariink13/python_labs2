import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../lab01'))

from models import BankAccount, SavingsAccount, CreditAccount
from interfaces import Printable, Comparable

# ------------------------------------------------------------
# Простая коллекция для демонстрации (аналог BankAccountCollection)
# ------------------------------------------------------------
class BankAccountCollection:
    def __init__(self):
        self._items = []

    def add(self, account):
        if not isinstance(account, (BankAccount, SavingsAccount, CreditAccount)):
            raise TypeError("Можно добавлять только BankAccount или его наследников")
        # Проверка дубликата по номеру счета
        for existing in self._items:
            if existing.account_number == account.account_number:
                raise ValueError(f"Счет {account.account_number} уже существует")
        self._items.append(account)

    def remove(self, account):
        if account not in self._items:
            raise ValueError("Счет не найден")
        self._items.remove(account)

    def remove_at(self, index):
        if 0 <= index < len(self._items):
            del self._items[index]
        else:
            raise IndexError("Индекс вне диапазона")

    def get_all(self):
        return self._items.copy()

    def find_by_owner_name(self, name):
        return [acc for acc in self._items if name.lower() in acc.owner_name.lower()]

    def find_by_balance_range(self, min_bal, max_bal):
        return [acc for acc in self._items if min_bal <= acc.balance <= max_bal]

    def sort_by_balance(self, reverse=False):
        self._items.sort(key=lambda acc: acc.balance, reverse=reverse)

    def sort_by_owner_name(self, reverse=False):
        self._items.sort(key=lambda acc: acc.owner_name, reverse=reverse)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, idx):
        return self._items[idx]

    def __setitem__(self, idx, value):
        if not isinstance(value, (BankAccount, SavingsAccount, CreditAccount)):
            raise TypeError("Можно присваивать только BankAccount")
        self._items[idx] = value

    def __str__(self):
        if not self._items:
            return "Коллекция пуста"
        res = f"Коллекция счетов (всего: {len(self._items)}):\n"
        for acc in self._items:
            res += f"  {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.\n"
        return res

# ------------------------------------------------------------
# Вспомогательные функции для работы с интерфейсами
# ------------------------------------------------------------
def filter_by_interface(collection, interface):
    new_coll = BankAccountCollection()
    for item in collection:
        if isinstance(item, interface):
            new_coll.add(item)
    return new_coll

def print_all_printable(items):
    for item in items:
        print(item.to_string())

# ------------------------------------------------------------
# Сценарии
# ------------------------------------------------------------
def print_separator(title: str = ""):
    print(f"\n{'='*50}")
    if title:
        print(f" {title} ".center(50, '='))
    print(f"{'='*50}")

def scenario_1():
    print_separator("СЦЕНАРИЙ 1: МЕТОДЫ ИНТЕРФЕЙСА")
    accounts = [
        BankAccount("Сьюзан Майер", 5000),
        SavingsAccount("Бри Ван де Камп", 10000, min_balance=2000),
        CreditAccount("Габриэль Солис", 5000, credit_limit=30000)
    ]
    for acc in accounts:
        print(f"Тип: {type(acc).__name__}")
        print(acc.to_string())
        print(f"Баланс для сравнения: {acc.balance}\n")

def scenario_2():
    print_separator("СЦЕНАРИЙ 2: ПОЛИМОРФНАЯ ФУНКЦИЯ")
    objects = [
        BankAccount("Линетт Скаво", 1500),
        SavingsAccount("Иди Бритт", 8000, min_balance=1000),
        CreditAccount("Рене Перри", -2000, credit_limit=10000),
        "Не Printable"
    ]
    printable = [obj for obj in objects if isinstance(obj, Printable)]
    print("Только Printable объекты:")
    print_all_printable(printable)
    print("\nПроверка isinstance:")
    for obj in objects[:3]:
        print(f"{obj.owner_name}: Printable? {isinstance(obj, Printable)}, Comparable? {isinstance(obj, Comparable)}")

def scenario_3():
    print_separator("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ И ФИЛЬТРАЦИЯ")
    coll = BankAccountCollection()
    coll.add(BankAccount("Анна Обычная", 1000))
    coll.add(SavingsAccount("Борис Сбер", 5000, min_balance=500))
    coll.add(CreditAccount("Виктор Кредит", -1000, credit_limit=5000))
    coll.add(SavingsAccount("Галина Сбер", 3000))

    print("Исходная коллекция:")
    print(coll)

    printable_coll = filter_by_interface(coll, Printable)
    print("\nТолько Printable (все счета):")
    print(printable_coll)

    print("\nСортировка по балансу (Comparable):")
    coll.sort_by_balance()
    print(coll)

    acc1 = BankAccount("Первый", 2000)
    acc2 = BankAccount("Второй", 3000)
    cmp = acc1.compare_to(acc2)
    print(f"\nacc1.compare_to(acc2) = {cmp} ({'меньше' if cmp<0 else 'больше' if cmp>0 else 'равно'})")

if __name__ == "__main__":
    scenario_1()
    scenario_2()
    scenario_3()