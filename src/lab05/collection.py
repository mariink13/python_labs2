import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lab03'))
from models import BankAccount

class BankAccountCollection:
    """Коллекция банковских счетов с поддержкой функциональных операций."""

    def __init__(self):
        self._items = []

    def add(self, account: BankAccount):
        if not isinstance(account, BankAccount):
            raise TypeError("Можно добавлять только BankAccount")
        for ex in self._items:
            if ex.account_number == account.account_number:
                raise ValueError(f"Счёт {account.account_number} уже есть")
        self._items.append(account)

    def remove(self, account: BankAccount):
        if account not in self._items:
            raise ValueError("Счёт не найден")
        self._items.remove(account)

    def remove_at(self, idx: int):
        if 0 <= idx < len(self._items):
            del self._items[idx]
        else:
            raise IndexError("Индекс вне диапазона")

    def get_all(self):
        return self._items.copy()

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, idx):
        return self._items[idx]

    def __setitem__(self, idx, value):
        if not isinstance(value, BankAccount):
            raise TypeError("Можно присваивать только BankAccount")
        self._items[idx] = value

    def __str__(self):
        if not self._items:
            return "Коллекция пуста"
        res = f"Коллекция счетов (всего: {len(self._items)}):\n"
        for acc in self._items:
            res += f"  {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.\n"
        return res

    # ----- Функциональные методы (задание 4,5) -----
    def sort_by(self, key_func, reverse=False):
        """
        Сортирует коллекцию, используя функцию извлечения ключа.
        Возвращает self (поддержка цепочек).
        """
        self._items.sort(key=key_func, reverse=reverse)
        return self

    def filter_by(self, predicate):
        """
        Создаёт новую коллекцию, содержащую элементы, для которых predicate вернул True.
        Возвращает новую коллекцию (для цепочек).
        """
        new_coll = BankAccountCollection()
        for item in self._items:
            if predicate(item):
                new_coll.add(item)
        return new_coll

    def apply(self, func):
        """
        Применяет функцию func к каждому элементу коллекции.
        func может изменять объект (in-place) и должна возвращать обработанный объект.
        Возвращает self (поддержка цепочек).
        """
        for i, item in enumerate(self._items):
            self._items[i] = func(item)
        return self
    
    def find(self, predicate):
        for item in self._items:
            if predicate(item):
                return item
        return None