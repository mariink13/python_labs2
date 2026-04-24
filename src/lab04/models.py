import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../lab01'))
from validate import Validator, TransactionValidator

from interfaces import Printable, Comparable

# ------------------------------------------------------------
# Базовый класс BankAccount
# ------------------------------------------------------------
class BankAccount(Printable, Comparable):
    _next_account_number = 1000

    def __init__(self, owner_name: str, initial_balance: float = 0.0, interest_rate: float = 1.0):
        Validator.validate_owner_name(owner_name)
        Validator.validate_balance(initial_balance)
        Validator.validate_interest_rate(interest_rate)

        self._account_number = str(BankAccount._generate_account_number())
        self._owner_name = owner_name.strip()
        self._balance = float(initial_balance)
        self._interest_rate = float(interest_rate)
        self._is_active = True

    @classmethod
    def _generate_account_number(cls):
        cls._next_account_number += 1
        return cls._next_account_number

    # ----- свойства -----
    @property
    def account_number(self) -> str:
        return self._account_number
    @property
    def owner_name(self) -> str:
        return self._owner_name
    @property
    def balance(self) -> float:
        return self._balance
    @property
    def interest_rate(self) -> float:
        return self._interest_rate
    @property
    def is_active(self) -> bool:
        return self._is_active

    @owner_name.setter
    def owner_name(self, new_name: str):
        Validator.validate_owner_name(new_name)
        self._owner_name = new_name.strip()
    @interest_rate.setter
    def interest_rate(self, new_rate: float):
        Validator.validate_interest_rate(new_rate)
        self._interest_rate = new_rate

    # ----- бизнес-методы -----
    def deposit(self, amount: float) -> float:
        TransactionValidator.validate_deposit(self, amount)
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        TransactionValidator.validate_withdrawal(self, amount)
        self._balance -= amount
        return self._balance

    def apply_interest(self) -> float:
        Validator.validate_account_status(self._is_active, "Начисление процентов")
        interest = self._balance * (self._interest_rate / 100)
        self._balance += interest
        return interest

    def close_account(self):
        if not self._is_active:
            raise ValueError("Счёт уже закрыт")
        self._is_active = False

    def activate_account(self):
        self._is_active = True

    def transfer_to(self, target: 'BankAccount', amount: float) -> str:
        TransactionValidator.validate_transfer(self, target, amount)
        self.withdraw(amount)
        target.deposit(amount)
        return f"Перевод {amount:.2f} на счёт {target.account_number} выполнен"

    # ----- магические методы -----
    def __str__(self):
        status = "✅ Активен" if self._is_active else "❌ Закрыт"
        return (f"┌────────────────────────────────┐\n"
                f"│ Счёт №{self._account_number:<18} │\n"
                f"├────────────────────────────────┤\n"
                f"│ Владелец: {self._owner_name:<19} │\n"
                f"│ Баланс: {self._balance:>16,.2f} руб. │\n"
                f"│ Ставка: {self._interest_rate:>16}% │\n"
                f"│ Статус: {status:<21} │\n"
                f"└────────────────────────────────┘")
    def __repr__(self):
        return f"BankAccount(owner_name='{self._owner_name}', balance={self._balance}, rate={self._interest_rate})"
    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number
    def __lt__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance < other._balance

    # ----- реализация интерфейсов -----
    def to_string(self) -> str:
        return str(self)

    def compare_to(self, other) -> int:
        if not isinstance(other, BankAccount):
            raise TypeError("Можно сравнивать только BankAccount")
        if self.balance < other.balance:
            return -1
        elif self.balance > other.balance:
            return 1
        else:
            return 0


# ------------------------------------------------------------
# Сберегательный счёт
# ------------------------------------------------------------
class SavingsAccount(BankAccount):
    def __init__(self, owner_name: str, initial_balance: float = 0.0,
                 interest_rate: float = 1.0, min_balance: float = 1000.0,
                 interest_bonus: float = 0.5):
        super().__init__(owner_name, initial_balance, interest_rate)
        if min_balance < 0:
            raise ValueError("Минимальный остаток не может быть отрицательным")
        if interest_bonus < 0:
            raise ValueError("Бонус не может быть отрицательным")
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

    def __str__(self):
        base = super().__str__()
        return base + f"\n  Мин. остаток: {self._min_balance:.2f} руб., Бонус: {self._interest_bonus}%"


# ------------------------------------------------------------
# Кредитный счёт
# ------------------------------------------------------------
class CreditAccount(BankAccount):
    def __init__(self, owner_name: str, initial_balance: float = 0.0,
                 interest_rate: float = 1.0, credit_limit: float = 100000.0,
                 credit_rate: float = 15.0):
        # Обходим валидацию отрицательного баланса
        super().__init__(owner_name, 0.0, interest_rate)
        self._balance = initial_balance
        if credit_limit < 0:
            raise ValueError("Лимит не может быть отрицательным")
        if credit_rate < 0:
            raise ValueError("Кредитная ставка не может быть отрицательной")
        self._credit_limit = credit_limit
        self._credit_rate = credit_rate

    def calculate_credit_interest(self) -> float:
        if self._balance >= 0:
            return 0.0
        return abs(self._balance) * (self._credit_rate / 100)

    def withdraw(self, amount: float) -> float:
        Validator.validate_positive_amount(amount, "Снятие")
        Validator.validate_account_status(self._is_active, "Снятие")
        new_balance = self._balance - amount
        if new_balance < -self._credit_limit:
            raise ValueError(f"Превышен кредитный лимит. Доступно: {self._credit_limit + self._balance:.2f} руб.")
        self._balance = new_balance
        return self._balance

    def __str__(self):
        base = super().__str__()
        return base + f"\n  Кредитный лимит: {self._credit_limit:.2f} руб., Ставка: {self._credit_rate}%"