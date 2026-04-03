
from model import BankAccount
from collection import BankAccountCollection


def print_separator(title: str = "", char: str = "=") -> None:
    """Выводит разделитель с заголовком."""
    print(f"\n{char * 50}")
    if title:
        print(f" {title} ".center(50, char))
    print(f"{char * 50}")


def scenario_1_basic_operations():
    """
    Сценарий 1: Базовые операции с коллекцией.
    Добавление, удаление, получение всех элементов.
    """
    print_separator("СЦЕНАРИЙ 1: ОСНОВНЫЕ ОПЕРАЦИИ")

    # Создаем коллекцию
    collection = BankAccountCollection()

    # Создаем счета
    susan = BankAccount("Сьюзан Майер", 1500, 2.5)
    gabrielle = BankAccount("Габриэль Солис", 5000, 3.0)
    bree = BankAccount("Бри Ван де Камп", 10000, 4.0)

    # Добавляем в коллекцию
    print("Добавление счетов:")
    collection.add(susan)
    collection.add(gabrielle)
    collection.add(bree)
    print(f"Добавлено 3 счета. Всего: {len(collection)}")

    # Выводим все счета
    print("\nВсе счета:")
    print(collection)

    # Удаляем один счет
    print("Удаление счета Габриэль...")
    collection.remove(gabrielle)
    print(f"После удаления. Всего: {len(collection)}")
    print(collection)

    # Проверка на дубликаты
    print("\nПопытка добавить дубликат:")
    try:
        collection.add(susan)
    except ValueError as e:
        print(f"❌ {e}")

    # Проверка типа
    print("\nПопытка добавить неверный тип:")
    try:
        collection.add("не счет")  # type: ignore
    except TypeError as e:
        print(f"❌ {e}")


def scenario_2_search_and_iteration():
    """
    Сценарий 2: Поиск и итерация.
    Поиск по имени, балансу, использование for и len().
    """
    print_separator("СЦЕНАРИЙ 2: ПОИСК И ИТЕРАЦИЯ")

    # Создаем коллекцию
    collection = BankAccountCollection()

    # Создаем и добавляем счета
    accounts = [
        BankAccount("Сьюзан Майер", 1500, 2.5),
        BankAccount("Габриэль Солис", 5000, 3.0),
        BankAccount("Бри Ван де Камп", 10000, 4.0),
        BankAccount("Линетт Скаво", 3000, 3.5),
        BankAccount("Иди Бритт", 2000, 2.0),
    ]

    for acc in accounts:
        collection.add(acc)

    print(f"Создано {len(collection)} счетов:")

    # Итерация через for
    print("\nОбход коллекции через for:")
    for acc in collection:
        print(f"  {acc.account_number} | {acc.owner_name} | {acc.balance:.2f} руб.")

    # Поиск по имени
    print("\nПоиск по имени 'Сьюзан':")
    found = collection.find_by_owner_name("Сьюзан")
    for acc in found:
        print(f"  {acc.owner_name} | {acc.balance:.2f} руб.")

    # Поиск по диапазону баланса
    print("\nПоиск счетов с балансом от 2000 до 5000:")
    found = collection.find_by_balance_range(2000, 5000)
    for acc in found:
        print(f"  {acc.owner_name} | {acc.balance:.2f} руб.")

    # Использование len()
    print(f"\nКоличество счетов в коллекции: {len(collection)}")


def scenario_3_sorting_and_indexing():
    """
    Сценарий 3: Сортировка и индексация.
    Сортировка по разным критериям, доступ по индексу.
    """
    print_separator("СЦЕНАРИЙ 3: СОРТИРОВКА И ИНДЕКСАЦИЯ")

    # Создаем коллекцию
    collection = BankAccountCollection()

    accounts = [
        BankAccount("Зоя Петрова", 500, 2.0),
        BankAccount("Анна Иванова", 3000, 3.0),
        BankAccount("Иван Сидоров", 1000, 2.5),
        BankAccount("Борис Смирнов", 2000, 1.5),
    ]

    for acc in accounts:
        collection.add(acc)

    print("Исходная коллекция:")
    print(collection)

    # Сортировка по балансу
    print("Сортировка по балансу (возрастание):")
    collection.sort_by_balance()
    print(collection)

    # Сортировка по имени
    print("Сортировка по имени владельца:")
    collection.sort_by_owner_name()
    print(collection)

    # Доступ по индексу
    print("Доступ по индексам:")
    print(f"  Первый счет: {collection[0].owner_name}")
    print(f"  Второй счет: {collection[1].owner_name}")

    # Замена по индексу
    print("\nЗамена счета по индексу 0:")
    new_account = BankAccount("Новый Клиент", 9999, 5.0)
    collection[0] = new_account
    print(f"  После замены: {collection[0].owner_name}")

    # Удаление по индексу
    print("\nУдаление по индексу 1:")
    collection.remove_at(1)
    print(f"  Осталось счетов: {len(collection)}")
    print(collection)


def scenario_4_filtering():
    """
    Сценарий 4: Фильтрация и логические операции.
    Получение подколлекций по условию.
    """
    print_separator("СЦЕНАРИЙ 4: ФИЛЬТРАЦИЯ")

    # Создаем коллекцию
    collection = BankAccountCollection()

    accounts = [
        BankAccount("Активный 1", 10000, 3.0),
        BankAccount("Активный 2", 2000, 2.5),
        BankAccount("Активный 3", 500, 1.0),
    ]

    for acc in accounts:
        collection.add(acc)

    # Закрываем один счет для демонстрации
    accounts[1].close_account()

    print("Исходная коллекция:")
    print(collection)

    # Активные счета
    print("Активные счета:")
    active = collection.get_active()
    print(active)

    # Закрытые счета
    print("Закрытые счета:")
    closed = collection.get_closed()
    print(closed)

    # Счета с балансом выше 1000
    print("Счета с балансом выше 1000 руб.:")
    rich = collection.get_with_balance_above(1000)
    print(rich)


def main():
    """Главная функция демонстрации."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " БАНК ВИСТЕРИЯ ЛЕЙН - КОЛЛЕКЦИЯ СЧЕТОВ ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    scenario_1_basic_operations()
    scenario_2_search_and_iteration()
    scenario_3_sorting_and_indexing()
    scenario_4_filtering()

    print_separator("ВСЕ СЦЕНАРИИ ВЫПОЛНЕНЫ", "★")
    print("✅ Коллекция банковских счетов успешно протестирована!")


if __name__ == "__main__":
    main()