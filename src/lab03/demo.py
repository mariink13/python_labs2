# demo.py
# Демонстрация наследования, полиморфизма и работы с коллекцией.


import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../lab02'))
from collection import BankAccountCollection
from base import BankAccount
from models import SavingsAccount, CreditAccount


def print_separator(title: str = ""):
    print(f"\n{'='*50}")
    if title:
        print(f" {title} ".center(50, '='))
    print(f"{'='*50}")


def filter_to_new_collection(collection, class_type):
    """Фильтрует коллекцию и возвращает новую коллекцию того же типа."""
    new_coll = BankAccountCollection()
    for item in collection:
        if isinstance(item, class_type):
            new_coll.add(item)
    return new_coll


# ========== СЦЕНАРИЙ 1: Наследование и super() ==========
def scenario_1_inheritance():
    print_separator("СЦЕНАРИЙ 1: НАСЛЕДОВАНИЕ И super()")

    # Обычный счёт — Сьюзан Майер
    ordinary = BankAccount("Сьюзан Майер", 5000, 2.0)

    # Сберегательный счёт — Бри Ван де Камп (любит порядок и накопления)
    savings = SavingsAccount("Бри Ван де Камп", 10000, 2.0,
                             min_balance=2000, interest_bonus=0.5)

    # Кредитный счёт — Габриэль Солис (любит тратить, может уходить в минус)
    credit = CreditAccount("Габриэль Солис", 5000, 1.0,
                           credit_limit=50000, credit_rate=12.0)

    print("Обычный счёт (Сьюзан):")
    print(ordinary)
    print("\nСберегательный счёт (Бри):")
    print(savings)
    print("\nКредитный счёт (Габриэль):")
    print(credit)

    print("\n--- Бонусные проценты (только для сберегательного счёта Бри) ---")
    savings.apply_bonus_interest()
    print(f"{savings.owner_name}: баланс после бонуса = {savings.balance:.2f} руб.")

    print("\n--- Кредитный счёт (Габриэль): снятие в минус и расчёт кредитных процентов ---")
    credit.withdraw(10000)
    credit_interest = credit.calculate_credit_interest()
    print(f"{credit.owner_name}: баланс = {credit.balance:.2f} руб.")
    print(f"Проценты за использование кредитных средств: {credit_interest:.2f} руб.")


# ========== СЦЕНАРИЙ 2: Полиморфизм ==========
def scenario_2_polymorphism():
    print_separator("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ (withdraw, apply_interest)")

    accounts = [
        BankAccount("Линетт Скаво", 2000, 1.5),           # обычный счёт
        SavingsAccount("Бри Ван де Камп", 2000, 1.5, min_balance=1000, interest_bonus=0.3),
        CreditAccount("Габриэль Солис", 2000, 1.5, credit_limit=30000, credit_rate=15.0)
    ]

    print("Попытка снять 1500 руб. с каждого счёта:")
    for acc in accounts:
        print(f"\n{acc.owner_name} (баланс: {acc.balance:.2f})")
        try:
            acc.withdraw(1500)
            print(f"  ✅ После снятия: {acc.balance:.2f}")
        except ValueError as e:
            print(f"  ❌ Ошибка: {e}")

    print("\n--- Начисление процентов на остаток ---")
    for acc in accounts:
        before = acc.balance
        acc.apply_interest()
        print(f"{acc.owner_name}: {before:.2f} → {acc.balance:.2f} (+{acc.balance - before:.2f})")


# ========== СЦЕНАРИЙ 3: Коллекция + фильтрация по типу ==========
def scenario_3_collection_and_filtering():
    print_separator("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ И ФИЛЬТРАЦИЯ ПО ТИПУ")

    coll = BankAccountCollection()

    # Добавляем разных персонажей
    coll.add(BankAccount("Сьюзан Майер", 1000))
    coll.add(SavingsAccount("Бри Ван де Камп", 5000, min_balance=1000))
    coll.add(CreditAccount("Габриэль Солис", -2000, credit_limit=10000, credit_rate=15.0))
    coll.add(SavingsAccount("Линетт Скаво", 3000, min_balance=500))
    coll.add(CreditAccount("Иди Бритт", 1000, credit_limit=20000, credit_rate=18.0))

    print("Все счета в коллекции:")
    for acc in coll:
        print(f"  {acc.owner_name} | {type(acc).__name__} | {acc.balance:.2f}")

    # Фильтруем только сберегательные счета
    savings_coll = filter_to_new_collection(coll, SavingsAccount)
    print("\nТолько сберегательные счета:")
    for acc in savings_coll:
        print(f"  {acc.owner_name} | баланс {acc.balance:.2f} | мин. остаток {acc._min_balance}")

    # Фильтруем только кредитные счета
    credit_coll = filter_to_new_collection(coll, CreditAccount)
    print("\nТолько кредитные счета:")
    for acc in credit_coll:
        print(f"  {acc.owner_name} | баланс {acc.balance:.2f} | лимит {acc._credit_limit}")

    # Проверка типов через isinstance()
    print("\nПроверка типов (isinstance):")
    for acc in coll:
        if isinstance(acc, SavingsAccount):
            print(f"{acc.owner_name} – сберегательный, бонус {acc._interest_bonus}%")
        elif isinstance(acc, CreditAccount):
            print(f"{acc.owner_name} – кредитный, ставка {acc._credit_rate}%")
        else:
            print(f"{acc.owner_name} – обычный счёт")


if __name__ == "__main__":
    scenario_1_inheritance()
    scenario_2_polymorphism()
    scenario_3_collection_and_filtering()