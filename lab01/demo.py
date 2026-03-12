from model import BankAccount
from validate import Validator, TransactionValidator


def print_separator(title: str = "", char: str = "=") -> None:
    """Выводит разделитель с заголовком."""
    print(f"\n{char * 50}")
    if title:
        print(f" {title} ".center(50, char))
    print(f"{char * 50}")


def demonstrate_validation_module() -> None:
    """Демонстрирует работу модуля валидации."""
    print_separator("ДЕМОНСТРАЦИЯ МОДУЛЯ ВАЛИДАЦИИ")
    
    print("1. Проверка корректных данных:")
    try:
        Validator.validate_owner_name("Иван Петров")
        Validator.validate_balance(1000.50)
        Validator.validate_interest_rate(5.5)
        print("   ✅ Все проверки пройдены успешно")
    except (TypeError, ValueError) as e:
        print(f"   {Validator.format_validation_error(e)}")
    
    print("\n2. Проверка некорректных данных:")
    
    # Проверка имени
    try:
        Validator.validate_owner_name("")
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")
    
    # Проверка баланса
    try:
        Validator.validate_balance(-100)
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")
    
    # Проверка ставки
    try:
        Validator.validate_interest_rate(15)
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")


def demonstrate_creation_and_basic_operations() -> None:
    """Демонстрирует создание счетов и базовые операции."""
    print_separator("СОЗДАНИЕ СЧЕТОВ И БАЗОВЫЕ ОПЕРАЦИИ")
    
    # Создание счетов
    print("Создание счетов:")
    account1 = BankAccount("Иван Петров", 1000.0, 2.5)
    account2 = BankAccount("Мария Сидорова", 500.0, 3.0)
    
    print("\nСчет 1:")
    print(account1)
    print("\nСчет 2:")
    print(account2)
    
    # Депозит
    print_separator("ОПЕРАЦИИ ДЕПОЗИТА", "-")
    print(f"Баланс до депозита: {account1.balance:,.2f} руб.")
    account1.deposit(500.0)
    print(f"После депозита 500 руб.: {account1.balance:,.2f} руб.")
    
    # Снятие средств
    print_separator("ОПЕРАЦИИ СНЯТИЯ", "-")
    print(f"Баланс до снятия: {account2.balance:,.2f} руб.")
    account2.withdraw(200.0)
    print(f"После снятия 200 руб.: {account2.balance:,.2f} руб.")
    
    # Начисление процентов
    print_separator("НАЧИСЛЕНИЕ ПРОЦЕНТОВ", "-")
    print(f"Баланс до начисления: {account1.balance:,.2f} руб.")
    interest = account1.apply_interest()
    print(f"Начислено процентов: {interest:.2f} руб.")
    print(f"Баланс после начисления: {account1.balance:,.2f} руб.")


def demonstrate_properties_and_validation() -> None:
    """Демонстрирует работу свойств и валидацию."""
    print_separator("СВОЙСТВА И ВАЛИДАЦИЯ")
    
    account = BankAccount("Алексей Смирнов", 1000.0, 5.0)
    print("Исходный счет:")
    print(account)
    
    # Изменение имени через setter
    print_separator("ИЗМЕНЕНИЕ ИМЕНИ ВЛАДЕЛЬЦА", "-")
    print(f"Старое имя: {account.owner_name}")
    account.owner_name = "Алексей Иванов"
    print(f"Новое имя: {account.owner_name}")
    
    # Изменение процентной ставки
    print_separator("ИЗМЕНЕНИЕ ПРОЦЕНТНОЙ СТАВКИ", "-")
    print(f"Старая ставка: {account.interest_rate}%")
    account.interest_rate = 7.5
    print(f"Новая ставка: {account.interest_rate}%")
    
    # Демонстрация констант валидации
    print_separator("КОНСТАНТЫ ВАЛИДАЦИИ", "-")
    print(f"Минимальный баланс: {Validator.MIN_BALANCE}")
    print(f"Максимальная ставка: {Validator.MAX_INTEREST_RATE}%")


def demonstrate_error_handling() -> None:
    """Демонстрирует обработку ошибок при создании и операциях."""
    print_separator("ОБРАБОТКА ОШИБОК ВАЛИДАЦИИ")
    
    test_cases = [
        ("Пустое имя", "", 1000.0, 1.0),
        ("Отрицательный баланс", "Тест", -500.0, 1.0),
        ("Ставка > максимума", "Тест", 1000.0, 15.0),
        ("Имя не строка", 123, 1000.0, 1.0),
    ]
    
    for i, (description, name, balance, rate) in enumerate(test_cases, 1):
        print(f"\n{i}. Попытка создания счета ({description}):")
        try:
            account = BankAccount(name, balance, rate)
            print(f"   Счет создан: {account.account_number}")
        except (TypeError, ValueError) as e:
            print(f"   {Validator.format_validation_error(e)}")
    
    # Демонстрация ошибок при операциях
    account = BankAccount("Тестовый Счет", 500.0)
    print(f"\nСоздан счет с балансом: {account.balance:,.2f} руб.")
    
    print("\n4. Попытка снять сумму больше баланса:")
    try:
        account.withdraw(1000.0)
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")
    
    print("\n5. Попытка внести отрицательную сумму:")
    try:
        account.deposit(-100.0)
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")


def demonstrate_state_changes() -> None:
    """Демонстрирует изменение состояния счета."""
    print_separator("ИЗМЕНЕНИЕ СОСТОЯНИЯ СЧЕТА")
    
    account = BankAccount("Сергей Петров", 1000.0, 3.0)
    print("Начальное состояние:")
    print(account)
    
    # Закрытие счета
    print_separator("ЗАКРЫТИЕ СЧЕТА", "-")
    account.close_account()
    print("После закрытия:")
    print(account)
    
    # Попытка операции с закрытым счетом
    print("\nПопытка внести депозит на закрытый счет:")
    try:
        account.deposit(500.0)
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")
    
    # Активация счета
    print_separator("АКТИВАЦИЯ СЧЕТА", "-")
    account.activate_account()
    print("После активации:")
    print(account)
    
    # Теперь операции снова доступны
    account.deposit(500.0)
    print(f"\nДепозит после активации выполнен. Новый баланс: {account.balance:,.2f} руб.")


def demonstrate_magic_methods() -> None:
    """Демонстрирует работу магических методов."""
    print_separator("МАГИЧЕСКИЕ МЕТОДЫ")
    
    # Создание счетов
    account1 = BankAccount("Клиент 1", 1000.0, 2.0)
    account2 = BankAccount("Клиент 2", 2000.0, 3.0)
    account3 = BankAccount("Клиент 1", 500.0, 2.5)
    
    # __str__
    print("1. __str__() метод (пользовательское представление):")
    print(str(account1))
    
    # __repr__
    print("\n2. __repr__() метод (представление для разработчиков):")
    print(repr(account1))
    
    # __eq__
    print_separator("СРАВНЕНИЕ СЧЕТОВ (__eq__)", "-")
    print(f"account1 == account2: {account1 == account2}")
    print(f"account1 == account3: {account1 == account3}")
    
    # __lt__
    accounts = [account1, account2, account3]
    print("\n3. Счета до сортировки по балансу (__lt__):")
    for acc in accounts:
        print(f"   {acc.owner_name}: {acc.balance:,.2f} руб.")
    
    accounts.sort()
    print("\n   Счета после сортировки по балансу:")
    for acc in accounts:
        print(f"   {acc.owner_name}: {acc.balance:,.2f} руб.")


def demonstrate_transfer() -> None:
    """Демонстрирует перевод между счетами."""
    print_separator("ПЕРЕВОД МЕЖДУ СЧЕТАМИ")
    
    sender = BankAccount("Отправитель", 5000.0, 2.0)
    receiver = BankAccount("Получатель", 1000.0, 3.0)
    
    print("До перевода:")
    print(f"   Отправитель: {sender.balance:,.2f} руб.")
    print(f"   Получатель: {receiver.balance:,.2f} руб.")
    
    # Выполнение перевода
    print_separator("ВЫПОЛНЕНИЕ ПЕРЕВОДА", "-")
    result = sender.transfer_to(receiver, 1500.0)
    print(f"   {result}")
    
    print("\nПосле перевода:")
    print(f"   Отправитель: {sender.balance:,.2f} руб.")
    print(f"   Получатель: {receiver.balance:,.2f} руб.")
    
    # Попытка перевода с недостаточным балансом
    print_separator("ПОПЫТКА ПЕРЕВОДА С НЕДОСТАТОЧНЫМ БАЛАНСОМ", "-")
    try:
        sender.transfer_to(receiver, 10000.0)
    except ValueError as e:
        print(f"   {Validator.format_validation_error(e)}")


def demonstrate_transaction_validator() -> None:
    """Демонстрирует работу специализированного валидатора транзакций."""
    print_separator("ДЕМОНСТРАЦИЯ TransactionValidator")
    
    account = BankAccount("Тестовый Счет", 1000.0, 2.0)
    
    print("1. Проверка корректной транзакции:")
    try:
        TransactionValidator.validate_deposit(account, 500.0)
        print("   ✅ Депозит 500 руб. разрешен")
    except ValueError as e:
        print(f"   {e}")
    
    print("\n2. Проверка транзакции с некорректной суммой:")
    try:
        TransactionValidator.validate_deposit(account, -100.0)
    except ValueError as e:
        print(f"   {e}")
    
    print("\n3. Проверка снятия с недостаточным балансом:")
    try:
        TransactionValidator.validate_withdrawal(account, 2000.0)
    except ValueError as e:
        print(f"   {e}")
    
    print("\n4. Проверка перевода между счетами:")
    receiver = BankAccount("Получатель", 500.0, 1.0)
    try:
        TransactionValidator.validate_transfer(account, receiver, 300.0)
        print("   ✅ Перевод 300 руб. разрешен")
    except ValueError as e:
        print(f"   {e}")


def main() -> None:
    """Главная функция демонстрации."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА BankAccount ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Последовательная демонстрация всех возможностей
    demonstrate_validation_module()
    demonstrate_creation_and_basic_operations()
    demonstrate_properties_and_validation()
    demonstrate_error_handling()
    demonstrate_state_changes()
    demonstrate_magic_methods()
    demonstrate_transfer()
    demonstrate_transaction_validator()
    
    print_separator("ЗАВЕРШЕНИЕ ДЕМОНСТРАЦИИ", "★")
    print("✅ Все возможности класса BankAccount успешно продемонстрированы!")
    print("✅ Модуль валидации работает корректно!")


if __name__ == "__main__":
    main()