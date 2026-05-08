import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lab03'))
sys.path.insert(0, os.path.dirname(__file__))   # для локальных модулей

from models import BankAccount, SavingsAccount, CreditAccount
from collection import BankAccountCollection
import strategies as st

def print_separator(title: str = ""):
    print(f"\n{'='*55}")
    if title:
        print(f" {title} ".center(55, '='))
    print(f"{'='*55}")

# ========== СЦЕНАРИЙ 1: Цепочка фильтр → сортировка → apply ==========
def scenario_1_chain():
    print_separator("СЦЕНАРИЙ 1: ЦЕПОЧКА (filter→sort→apply)")

    # Создаём коллекцию
    coll = BankAccountCollection()
    coll.add(BankAccount("Сьюзан Майер", 500))
    coll.add(SavingsAccount("Бри Ван де Камп", 2000, min_balance=500))
    coll.add(CreditAccount("Габриэль Солис", 10000, credit_limit=30000))
    coll.add(BankAccount("Линетт Скаво", 150))
    coll.add(SavingsAccount("Иди Бритт", 8000, min_balance=1000))

    print("Исходная коллекция:")
    print(coll)

    # Цепочка: фильтрация (баланс > 1000), сортировка по имени, применение скидки 10%
    result = (coll
              .filter_by(st.is_balance_above(1000))
              .sort_by(st.by_owner_name)
              .apply(st.apply_discount(10)))

    print("\nПосле цепочки (баланс > 1000, сортировка по имени, скидка 10%):")
    print(result)

# ========== СЦЕНАРИЙ 2: Замена стратегии без изменения кода ==========
def scenario_2_strategy_replace():
    print_separator("СЦЕНАРИЙ 2: ЗАМЕНА СТРАТЕГИИ СОРТИРОВКИ")

    coll = BankAccountCollection()
    coll.add(BankAccount("Анна", 3000))
    coll.add(SavingsAccount("Иван", 1000, min_balance=200))
    coll.add(CreditAccount("Мария", 500, credit_limit=2000))

    print("Исходная коллекция:")
    print(coll)

    print("Сортировка по имени (стратегия by_owner_name):")
    coll.sort_by(st.by_owner_name)
    print(coll)

    print("Сортировка по балансу (стратегия by_balance):")
    coll.sort_by(st.by_balance)
    print(coll)

    print("Сортировка по имени, затем по балансу (стратегия кортежа):")
    coll.sort_by(st.by_owner_name_then_balance)
    print(coll)

# ========== СЦЕНАРИЙ 3: Callable-стратегия (паттерн Стратегия) ==========
def scenario_3_callable_strategy():
    print_separator("СЦЕНАРИЙ 3: CALLABLE-СТРАТЕГИЯ (снятие денег)")

    account = SavingsAccount("Тест", 5000, min_balance=500)
    print("Счёт:", account.owner_name, "баланс:", account.balance)

    # Используем стратегию StandardWithdrawStrategy
    standard = st.StandardWithdrawStrategy()
    try:
        standard(account, 4700)   # останется 300
        print("Стандартная стратегия: сняли 4700, новый баланс:", account.balance)
    except ValueError as e:
        print("Ошибка (стандартная):", e)

    # Пытаемся снять больше — ошибка
    try:
        standard(account, 1000)    # 300 - 1000 = -700 (недостаточно)
    except ValueError as e:
        print("Стандартная стратегия: ошибка (недостаточно средств)")

    # Восстановим баланс
    account = SavingsAccount("Тест2", 5000, min_balance=500)
    print("\nНовый счёт:", account.owner_name, "баланс:", account.balance)

    # Безопасная стратегия с учётом минимального остатка
    safe = st.SafeWithdrawStrategy()
    try:
        safe(account, 4700)    # баланс станет 300 – ниже min_balance? min_balance=500
    except ValueError as e:
        print("Безопасная стратегия:", e)

    # Попробуем снять только 4000 (останется 1000 => выше min_balance)
    account = SavingsAccount("Тест3", 5000, min_balance=500)
    safe(account, 4000)
    print("Безопасная стратегия: сняли 4000, новый баланс:", account.balance)

if __name__ == "__main__":
    scenario_1_chain()
    scenario_2_strategy_replace()
    scenario_3_callable_strategy()