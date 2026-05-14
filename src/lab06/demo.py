

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lab03'))

from models import BankAccount, SavingsAccount, CreditAccount
from container import TypedCollection, Displayable, Scorable, D, S

# ----- Добавляем недостающие методы для протоколов (monkey patching) -----
def _display(self) -> str:
    return str(self)

def _score(self) -> float:
    return self.balance

for cls in (BankAccount, SavingsAccount, CreditAccount):
    cls.display = _display
    cls.score = _score
# --------------------------------------------------

def print_separator(title: str = ""):
    print(f"\n{'='*60}")
    if title:
        print(f" {title} ".center(60, '='))
    print(f"{'='*60}")

def scenario_1_basic():
    print_separator("СЦЕНАРИЙ 1: TYPEDCOLLECTION С АННОТАЦИЯМИ")
    accounts: TypedCollection[BankAccount] = TypedCollection()
    acc1 = BankAccount("Сьюзан Майер", 5000)
    acc2 = SavingsAccount("Бри Ван де Камп", 10000, min_balance=2000)
    acc3 = CreditAccount("Габриэль Солис", 5000, credit_limit=30000)

    accounts.add(acc1)
    accounts.add(acc2)
    accounts.add(acc3)

    print("Все добавленные счета:")
    for acc in accounts.get_all():
        print(f"  {acc.owner_name}: баланс {acc.balance:.2f}")

    # Демонстрация проверки типа
    try:
        accounts.add("не счёт")  # type: ignore
    except TypeError as e:
        print(f"\nОшибка при добавлении неверного типа: {e}")

    print("\nВывод коллекции через __str__:")
    print(accounts)

def scenario_2_find_filter_map():
    print_separator("СЦЕНАРИЙ 2: FIND, FILTER, MAP")
    accounts = TypedCollection[BankAccount]()
    accounts.add(BankAccount("Анна Иванова", 3000))
    accounts.add(SavingsAccount("Борис Петров", 1500, min_balance=500))
    accounts.add(CreditAccount("Виктор Смирнов", 8000, credit_limit=20000))
    accounts.add(BankAccount("Галина Соколова", 4000))

    found = accounts.find(lambda acc: acc.balance > 5000)
    print(f"Найден счёт с балансом > 5000: {found.owner_name} (баланс {found.balance})" if found else "Не найден")
    none_found = accounts.find(lambda acc: acc.balance > 10000)
    print(f"Поиск баланса > 10000: результат – {none_found}")

    low_balance = accounts.filter(lambda acc: acc.balance < 3000)
    print("\nСчета с балансом < 3000:")
    for acc in low_balance:
        print(f"  {acc.owner_name}: {acc.balance:.2f}")

    names = accounts.map(lambda acc: acc.owner_name)
    print(f"\nИмена всех владельцев: {names}")

    def apply_discount(acc: BankAccount) -> BankAccount:
        acc._balance = acc.balance * 0.95
        return acc

    discounted = accounts.map(apply_discount)
    print("Балансы после скидки 5%:")
    for acc in discounted:
        print(f"  {acc.owner_name}: {acc.balance:.2f}")

def scenario_3_protocols():
    print_separator("СЦЕНАРИЙ 3: ПРОТОКОЛЫ (Displayable, Scorable)")
    displayable_coll: TypedCollection[D] = TypedCollection()
    displayable_coll.add(BankAccount("Сьюзан Майер", 5000))
    displayable_coll.add(SavingsAccount("Бри Ван де Камп", 10000, min_balance=2000))
    displayable_coll.add(CreditAccount("Габриэль Солис", 5000, credit_limit=30000))

    print("Коллекция Displayable объектов – вызов display():")
    for item in displayable_coll:
        print(item.display())

    scorable_coll: TypedCollection[S] = TypedCollection()
    scorable_coll.add(BankAccount("Иван Петров", 7000))
    scorable_coll.add(SavingsAccount("Мария Сидорова", 12000, min_balance=3000))
    scorable_coll.add(CreditAccount("Алексей Козлов", -2000, credit_limit=50000))

    print("\nКоллекция Scorable объектов – сумма score (балансов):")
    total_score = sum(item.score() for item in scorable_coll)
    print(f"Общий баланс всех счетов: {total_score:.2f}")

if __name__ == "__main__":
    scenario_1_basic()
    scenario_2_find_filter_map()
    scenario_3_protocols()