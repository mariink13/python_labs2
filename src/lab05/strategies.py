import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lab03'))
from models import SavingsAccount, CreditAccount

# ----- Стратегии сортировки (key-функции) -----
def by_owner_name(account):
    """Ключ для сортировки по имени владельца."""
    return account.owner_name

def by_balance(account):
    """Ключ для сортировки по балансу."""
    return account.balance

def by_owner_name_then_balance(account):
    """Сортировка сначала по имени, затем по балансу."""
    return (account.owner_name, account.balance)

def by_account_number(account):
    """Ключ для сортировки по номеру счёта."""
    return account.account_number

# ----- Функции-фильтры (предикаты) -----
def is_balance_above(limit):
    """Фабрика фильтров: возвращает функцию, проверяющую баланс > limit."""
    def predicate(account):
        return account.balance > limit
    return predicate

def is_owner_contains(substring):
    """Фабрика: фильтр по вхождению подстроки в имя владельца."""
    def predicate(account):
        return substring.lower() in account.owner_name.lower()
    return predicate

def is_savings_account(account):
    """Фильтр: только сберегательные счета."""
    from models import SavingsAccount
    return isinstance(account, SavingsAccount)

def is_credit_account(account):
    """Фильтр: только кредитные счета."""
    from models import CreditAccount
    return isinstance(account, CreditAccount)

def is_any_account(account):
    """Фильтр, принимающий все счета (для демонстрации)."""
    return True

# ----- Функции преобразования (map) -----
def extract_owner_name(account):
    """Извлекает имя владельца."""
    return account.owner_name

def extract_balance(account):
    """Извлекает баланс."""
    return account.balance

def apply_discount(percent):
    """
    Фабрика: применяет скидку к балансу (уменьшает на percent%).
    Возвращает функцию преобразования объекта.
    """
    def discount_func(account):
        account._balance = account.balance * (1 - percent/100)
        return account
    return discount_func

def to_string_representation(account):
    """Преобразует счёт в строку (для map)."""
    return account.to_string()

# ----- Callable-стратегии (паттерн Стратегия) -----
class WithdrawStrategy:
    """Абстрактная стратегия снятия денег."""
    def __call__(self, account, amount):
        raise NotImplementedError

class StandardWithdrawStrategy(WithdrawStrategy):
    """Обычное снятие (без ограничений, только проверка достаточности)."""
    def __call__(self, account, amount):
        if amount > account.balance:
            raise ValueError("Недостаточно средств")
        account.withdraw(amount)
        return account

class SafeWithdrawStrategy(WithdrawStrategy):
    """Безопасное снятие с проверкой минимального остатка (если есть)."""
    def __call__(self, account, amount):
        # Если счёт имеет атрибут min_balance (SavingsAccount)
        if hasattr(account, '_min_balance'):
            if account.balance - amount < account._min_balance:
                raise ValueError(f"Нельзя опустить баланс ниже {account._min_balance}")
        account.withdraw(amount)
        return account