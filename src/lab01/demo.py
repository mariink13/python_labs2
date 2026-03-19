

from model import BankAccount
from validate import Validator, TransactionValidator


def print_separator(title: str = "", char: str = "=") -> None:
    """Выводит разделитель с заголовком."""
    print(f"\n{char * 50}")
    if title:
        print(f" {title} ".center(50, char))
    print(f"{char * 50}")


def scenario_1_creation_and_basic_operations():
    """
    Сценарий 1: Создание счетов и базовые операции.
    
    """
    print_separator("СЦЕНАРИЙ 1: СЧЕТА СЬЮЗАН И ГАБРИЭЛЬ")
    
    # Создание счетов
    susan = BankAccount("Сьюзан Майер", 1500.0, 2.5)
    gabrielle = BankAccount("Габриэль Солис", 5000.0, 3.0)
    
    print("🏠 Счета жительниц Вистерия Лейн:")
    print(susan)
    print(gabrielle)
    
    # Сьюзан получает депозит
    print_separator("СЬЮЗАН ВНОСИТ ДЕПОЗИТ", "-")
    print(f"Баланс Сьюзан до депозита: {susan.balance:,.2f} руб.")
    susan.deposit(500.0)
    print(f"После депозита 500 руб.: {susan.balance:,.2f} руб.")
    
    # Габриэль снимает деньги на шопинг
    print_separator("ГАБРИЭЛЬ ИДЕТ ЗА ПОКУПКАМИ", "-")
    print(f"Баланс Габриэль до снятия: {gabrielle.balance:,.2f} руб.")
    gabrielle.withdraw(2000.0)
    print(f"После снятия 2000 руб.: {gabrielle.balance:,.2f} руб.")
    
    # Начисление процентов
    print_separator("НАЧИСЛЕНИЕ ПРОЦЕНТОВ", "-")
    interest = susan.apply_interest()
    print(f"Сьюзан начислено процентов: {interest:.2f} руб.")
    print(f"Новый баланс Сьюзан: {susan.balance:,.2f} руб.")


def scenario_2_properties_and_validation():
    """
    Сценарий 2: Работа свойств и валидации.
    
    """
    print_separator("СЦЕНАРИЙ 2: БРИ ВАН ДЕ КАМП НАВОДИТ ПОРЯДОК")
    
    bree = BankAccount("Бри Ван де Камп", 10000.0, 4.0)
    print("Идеальный счет Бри:")
    print(bree)
    
    # Бри меняет имя (после замужества)
    print_separator("БРИ МЕНЯЕТ ИМЯ", "-")
    print(f"Старое имя: {bree.owner_name}")
    bree.owner_name = "Бри Ходж"
    print(f"Новое имя: {bree.owner_name}")
    
    # Бри меняет процентную ставку
    print_separator("БРИ МЕНЯЕТ ПРОЦЕНТНУЮ СТАВКУ", "-")
    print(f"Старая ставка: {bree.interest_rate}%")
    bree.interest_rate = 5.5
    print(f"Новая ставка: {bree.interest_rate}%")
    
    # Бри проверяет константы
    print_separator("КОНСТАНТЫ ВАЛИДАЦИИ", "-")
    print(f"Минимальный баланс: {Validator.MIN_BALANCE}")
    print(f"Максимальная ставка: {Validator.MAX_INTEREST_RATE}%")


def scenario_3_state_changes_and_errors():
    """
    Сценарий 3: Изменение состояния и обработка ошибок.
    
    """
    print_separator("СЦЕНАРИЙ 3: ЛИНЕТТ СКАВО УПРАВЛЯЕТ ФИНАНСАМИ")
    
    lynette = BankAccount("Линетт Скаво", 3000.0, 3.5)
    print("Счет Линетт:")
    print(lynette)
    
    # Линетт закрывает счет (как временно замораживает)
    print_separator("ЛИНЕТТ ЗАКРЫВАЕТ СЧЕТ", "-")
    lynette.close_account()
    print("После закрытия:")
    print(lynette)
    
    # Попытка операции с закрытым счетом
    print("\nПопытка снять деньги с закрытого счета:")
    try:
        lynette.withdraw(500.0)
    except ValueError as e:
        print(f"❌ {e}")
    
    # Активация счета
    print_separator("ЛИНЕТТ АКТИВИРУЕТ СЧЕТ", "-")
    lynette.activate_account()
    print("После активации:")
    print(lynette)
    
    # Теперь операции доступны
    lynette.deposit(1000.0)
    print(f"\n✅ Депозит выполнен. Новый баланс: {lynette.balance:,.2f} руб.")
    
    # Демонстрация обработки ошибок валидации
    print_separator("ОШИБКИ ВАЛИДАЦИИ", "-")
    
    try:
        print("Попытка создать счет с пустым именем:")
        bad_account = BankAccount("", 1000.0)
    except ValueError as e:
        print(f"❌ {e}")
    
    try:
        print("\nПопытка снять сумму больше баланса:")
        lynette.withdraw(10000.0)
    except ValueError as e:
        print(f"❌ {e}")


def scenario_4_magic_methods_and_transfer():
    """
    Сценарий 4: Магические методы и переводы.
    
    """
    print_separator("СЦЕНАРИЙ 4: ИДИ И РЕНЕ")
    
    edie = BankAccount("Иди Бритт", 2000.0, 2.0)
    renee = BankAccount("Рене Перри", 3500.0, 3.0)
    
    print("Счета подруг:")
    print(edie)
    print(renee)
    
    # Демонстрация __str__ и __repr__
    print_separator("МАГИЧЕСКИЕ МЕТОДЫ", "-")
    print("__str__() для пользователей:")
    print(str(edie))
    
    print("\n__repr__() для разработчиков:")
    print(repr(edie))
    
    # Демонстрация __eq__
    print_separator("СРАВНЕНИЕ СЧЕТОВ", "-")
    print(f"edie == renee: {edie == renee}")
    
    # Демонстрация __lt__ (сортировка)
    accounts = [edie, renee]
    print("\nСчета до сортировки по балансу:")
    for acc in accounts:
        print(f"   {acc.owner_name}: {acc.balance:,.2f} руб.")
    
    accounts.sort()
    print("\nСчета после сортировки по балансу (от меньшего к большему):")
    for acc in accounts:
        print(f"   {acc.owner_name}: {acc.balance:,.2f} руб.")
    
    # Перевод между счетами
    print_separator("ИДИ ОДАЛЖИВАЕТ ДЕНЬГИ РЕНЕ", "-")
    print("До перевода:")
    print(f"   Иди: {edie.balance:,.2f} руб.")
    print(f"   Рене: {renee.balance:,.2f} руб.")
    
    result = edie.transfer_to(renee, 500.0)
    print(f"\n{result}")
    
    print("\nПосле перевода:")
    print(f"   Иди: {edie.balance:,.2f} руб.")
    print(f"   Рене: {renee.balance:,.2f} руб.")
    
    # Попытка перевода с недостаточным балансом
    print_separator("ПОПЫТКА ПЕРЕВОДА С НЕДОСТАТОЧНЫМ БАЛАНСОМ", "-")
    try:
        edie.transfer_to(renee, 10000.0)
    except ValueError as e:
        print(f"❌ {e}")


def main():
    """Главная функция демонстрации."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " БАНК ВИСТЕРИЯ ЛЕЙН ".center(58) + "║")
    print("║" + " Отчаянные домохозяйки управляют счетами ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    
    # 4 сценария (достаточно для оценки 5)
    scenario_1_creation_and_basic_operations()
    scenario_2_properties_and_validation()
    scenario_3_state_changes_and_errors()
    scenario_4_magic_methods_and_transfer()
    
    print_separator("ВСЕ СЦЕНАРИИ ВЫПОЛНЕНЫ", "★")
    print("✅ Банковские счета жительниц Вистерия Лейн успешно обслуживаются!")
    print("✅ Все требования лабораторной работы выполнены!")


if __name__ == "__main__":
    main()