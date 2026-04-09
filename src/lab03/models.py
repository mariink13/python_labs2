# models.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../lab01'))

from validate import Validator, TransactionValidator
from base import BankAccount


class SavingsAccount(BankAccount):
    # ... (без изменений, как было ранее)
    def __init__(self, owner_name: str, initial_balance: float = 0.0,
                 interest_rate: float = 1.0, min_balance: float = 1000.0,
                 interest_bonus: float = 0.5):
        super().__init__(owner_name, initial_balance, interest_rate)
        if min_balance < 0:
            raise ValueError("Минимальный остаток не может быть отрицательным")
        if interest_bonus < 0:
            raise ValueError("Бонус к ставке не может быть отрицательным")
        self._min_balance = min_balance
        self._interest_bonus = interest_bonus

    def apply_bonus_interest(self) -> float:
        total_rate = self._interest_rate + self._interest_bonus
        interest = self._balance * (total_rate / 100)
        self._balance += interest
        return interest

    def withdraw(self, amount: float) -> float:
        TransactionValidator.validate_withdrawal(self, amount)
        if self._balance - amount < self._min_balance:
            raise ValueError(f"Снятие невозможно: остаток упадёт ниже минимального {self._min_balance:.2f} руб.")
        self._balance -= amount
        return self._balance

    def __str__(self) -> str:
        base_str = super().__str__()
        return base_str + f"\n  Мин. остаток: {self._min_balance:.2f} руб., Бонус: {self._interest_bonus}%"


class CreditAccount(BankAccount):
    def __init__(self, owner_name: str, initial_balance: float = 0.0,
                 interest_rate: float = 1.0, credit_limit: float = 100000.0,
                 credit_rate: float = 15.0):
        # Обходим валидацию баланса в базовом классе
        super().__init__(owner_name, 0.0, interest_rate)
        self._balance = initial_balance   # разрешаем отрицательный баланс

        if credit_limit < 0:
            raise ValueError("Кредитный лимит не может быть отрицательным")
        if credit_rate < 0:
            raise ValueError("Кредитная ставка не может быть отрицательной")
        self._credit_limit = credit_limit
        self._credit_rate = credit_rate

    def calculate_credit_interest(self) -> float:
        if self._balance >= 0:
            return 0.0
        debt = abs(self._balance)
        interest = debt * (self._credit_rate / 100)
        return interest

    def withdraw(self, amount: float) -> float:
        Validator.validate_positive_amount(amount, "Снятие")
        Validator.validate_account_status(self._is_active, "Снятие")
        new_balance = self._balance - amount
        if new_balance < -self._credit_limit:
            raise ValueError(f"Превышен кредитный лимит. Доступно: {self._credit_limit + self._balance:.2f} руб.")
        self._balance = new_balance
        return self._balance

    def __str__(self) -> str:
        base_str = super().__str__()
        return base_str + f"\n  Кредитный лимит: {self._credit_limit:.2f} руб., Кред. ставка: {self._credit_rate}%"

    def __repr__(self) -> str:
        return (f"CreditAccount(owner_name='{self._owner_name}', balance={self._balance}, "
                f"interest_rate={self._interest_rate}, credit_limit={self._credit_limit}, "
                f"credit_rate={self._credit_rate})")