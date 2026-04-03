
from model import BankAccount


class BankAccountCollection:
    """
    Класс для управления коллекцией банковских счетов.
    Обеспечивает добавление, удаление, поиск, итерацию, индексацию и сортировку.
    """

    def __init__(self):
        """Инициализирует пустую коллекцию."""
        self._items = []  # список для хранения счетов

    # ========== Базовые операции ==========

    def add(self, account: BankAccount) -> None:
        """
        Добавляет банковский счет в коллекцию.
        Проверяет тип и наличие дубликата по номеру счета.
        """
        if not isinstance(account, BankAccount):
            raise TypeError("Можно добавлять только объекты BankAccount")

        # Проверка на дубликат по номеру счета
        for existing in self._items:
            if existing.account_number == account.account_number:
                raise ValueError(f"Счет {account.account_number} уже существует в коллекции")

        self._items.append(account)

    def remove(self, account: BankAccount) -> None:
        """Удаляет банковский счет из коллекции."""
        if account not in self._items:
            raise ValueError("Такого счета нет в коллекции")
        self._items.remove(account)

    def remove_at(self, index: int) -> None:
        """Удаляет счет по индексу."""
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        del self._items[index]

    def get_all(self) -> list:
        """Возвращает список всех счетов."""
        return self._items.copy()  # возвращаем копию для защиты от внешнего изменения

    # ========== Поиск ==========

    def find_by_owner_name(self, name: str) -> list:
        """Возвращает список счетов по имени владельца (частичное совпадение)."""
        return [acc for acc in self._items if name.lower() in acc.owner_name.lower()]

    def find_by_account_number(self, number: str) -> list:
        """Возвращает список счетов по номеру счета."""
        return [acc for acc in self._items if acc.account_number == number]

    def find_by_balance_range(self, min_balance: float, max_balance: float) -> list:
        """Возвращает список счетов с балансом в заданном диапазоне."""
        return [acc for acc in self._items if min_balance <= acc.balance <= max_balance]

    # ========== Фильтрация (логические операции) ==========

    def get_active(self) -> 'BankAccountCollection':
        """Возвращает новую коллекцию с активными счетами."""
        new_collection = BankAccountCollection()
        for acc in self._items:
            if acc.is_active:
                new_collection.add(acc)
        return new_collection

    def get_closed(self) -> 'BankAccountCollection':
        """Возвращает новую коллекцию с закрытыми счетами."""
        new_collection = BankAccountCollection()
        for acc in self._items:
            if not acc.is_active:
                new_collection.add(acc)
        return new_collection

    def get_with_balance_above(self, amount: float) -> 'BankAccountCollection':
        """Возвращает новую коллекцию счетов с балансом выше указанной суммы."""
        new_collection = BankAccountCollection()
        for acc in self._items:
            if acc.balance > amount:
                new_collection.add(acc)
        return new_collection

    # ========== Сортировка ==========

    def sort_by_balance(self, reverse: bool = False) -> None:
        """Сортирует коллекцию по балансу."""
        self._items.sort(key=lambda acc: acc.balance, reverse=reverse)

    def sort_by_owner_name(self, reverse: bool = False) -> None:
        """Сортирует коллекцию по имени владельца."""
        self._items.sort(key=lambda acc: acc.owner_name, reverse=reverse)

    def sort_by_account_number(self, reverse: bool = False) -> None:
        """Сортирует коллекцию по номеру счета."""
        self._items.sort(key=lambda acc: acc.account_number, reverse=reverse)

    def sort(self, key=None, reverse: bool = False) -> None:
        """
        Универсальная сортировка с пользовательским ключом.
        key: функция, возвращающая значение для сравнения.
        """
        if key is None:
            key = lambda acc: acc.account_number
        self._items.sort(key=key, reverse=reverse)

    # ========== Магические методы ==========

    def __len__(self) -> int:
        """Возвращает количество счетов в коллекции."""
        return len(self._items)

    def __iter__(self):
        """Возвращает итератор для обхода коллекции."""
        return iter(self._items)

    def __getitem__(self, index: int) -> BankAccount:
        """Позволяет обращаться по индексу (collection[0])."""
        if isinstance(index, slice):
            # Поддержка срезов
            new_collection = BankAccountCollection()
            for acc in self._items[index]:
                new_collection.add(acc)
            return new_collection
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items[index]

    def __setitem__(self, index: int, value: BankAccount) -> None:
        """Позволяет заменять элемент по индексу."""
        if not isinstance(value, BankAccount):
            raise TypeError("Можно устанавливать только объекты BankAccount")
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        self._items[index] = value

    def __contains__(self, account: BankAccount) -> bool:
        """Проверяет, есть ли счет в коллекции."""
        return account in self._items

    def __str__(self) -> str:
        """Возвращает строковое представление коллекции."""
        if not self._items:
            return "Коллекция пуста"
        result = f"Коллекция банковских счетов (всего: {len(self._items)}):\n"
        for acc in self._items:
            result += f"  {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.\n"
        return result

    def __repr__(self) -> str:
        """Официальное представление для разработчиков."""
        return f"BankAccountCollection({self._items})"