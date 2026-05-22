import sys
import os
from typing import List, Optional
from abc import ABC, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), '../lab03'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../lab05'))

from models import BankAccount, SavingsAccount, CreditAccount
from collection import BankAccountCollection
from exceptions import ItemNotFoundError, DuplicateItemError

# ----- Стратегии комиссий -----
class FeeStrategy(ABC):
    @abstractmethod
    def calculate(self, account, operation_amount):
        pass

class NoFee(FeeStrategy):
    def calculate(self, account, operation_amount):
        return 0

class FlatFee(FeeStrategy):
    def __init__(self, amount):
        self.amount = amount
    def calculate(self, account, operation_amount):
        return self.amount

class PercentFee(FeeStrategy):
    def __init__(self, percent):
        self.percent = percent
    def calculate(self, account, operation_amount):
        return operation_amount * self.percent / 100

class TieredFee(FeeStrategy):
    def __init__(self, thresholds):
        self.thresholds = thresholds
    def calculate(self, account, operation_amount):
        for limit, percent in self.thresholds:
            if operation_amount < limit:
                return operation_amount * percent / 100
        return 0

class BankApp:
    def __init__(self, collection: BankAccountCollection):
        self.collection = collection

    def add_account(self, account_type: str, owner: str, balance: float, **kwargs):
        if account_type == 'savings':
            rate = kwargs.get('interest_rate', 0.01)
            acc = SavingsAccount(owner, balance, rate)
        elif account_type == 'credit':
            limit = kwargs.get('credit_limit', 1000)
            acc = CreditAccount(owner, balance, credit_limit=limit)
        else:
            acc = BankAccount(owner, balance)
        try:
            self.collection.add(acc)
        except ValueError as e:
            raise DuplicateItemError(str(e))

    def remove_account(self, owner: str):
        acc = self.collection.find(lambda a: a._owner_name == owner)
        if acc is None:
            raise ItemNotFoundError(f"Счёт владельца '{owner}' не найден")
        self.collection.remove(acc)

    def get_all_accounts(self) -> List[BankAccount]:
        return self.collection.get_all()

    def find_account(self, owner: str) -> Optional[BankAccount]:
        return self.collection.find(lambda a: a._owner_name == owner)

    def filter_by_balance(self, min_bal: float, max_bal: float) -> List[BankAccount]:
        return self.collection.filter_by(lambda a: min_bal <= a.balance <= max_bal)

    def filter_by_type(self, account_class):
        return self.collection.filter_by(lambda a: isinstance(a, account_class))

    def apply_interest_to_savings(self):
        for acc in self.collection:
            if isinstance(acc, SavingsAccount):
                acc.apply_interest()

    def set_fee_strategy(self, owner: str, strategy_type: str, value: float = 0):
        acc = self.find_account(owner)
        if acc is None:
            raise ItemNotFoundError(f"Счёт владельца '{owner}' не найден")
        if strategy_type == 'percent':
            acc._fee_strategy = PercentFee(value)
        elif strategy_type == 'flat':
            acc._fee_strategy = FlatFee(value)
        else:
            acc._fee_strategy = NoFee()

    def sort_by_balance(self, reverse=False):
        self.collection.sort_by(lambda a: a.balance, reverse)

    def sort_by_owner(self, reverse=False):
        self.collection.sort_by(lambda a: a._owner_name, reverse)

    def sort_by_type_then_balance(self, reverse=False):
        def key_func(a):
            return (a.__class__.__name__, a.balance)
        self.collection.sort_by(key_func, reverse)

    def total_balance(self) -> float:
        return sum(acc.balance for acc in self.collection)

    def deposit_to_account(self, owner: str, amount: float):
        acc = self.find_account(owner)
        if acc is None:
            raise ItemNotFoundError(f"Счёт владельца '{owner}' не найден")
        acc.deposit(amount)

    def withdraw_from_account(self, owner: str, amount: float):
        acc = self.find_account(owner)
        if acc is None:
            raise ItemNotFoundError(f"Счёт владельца '{owner}' не найден")
        acc.withdraw(amount)