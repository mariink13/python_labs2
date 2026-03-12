# python_labs2

## Лабораторная работа 1
## Тема
Банковская система — класс BankAccount


## Цель работы
Освоить объявление пользовательских классов, разобраться с инкапсуляцией, реализовать свойства и магические методы.

### model.py 

**`model.py`** — главный файл лабораторной. Реализует:
- Класс `BankAccount` с закрытыми атрибутами
- Свойства (`@property`) для доступа к данным
- Бизнес-методы (операции со счетом)
- Магические методы `__str__`, `__repr__`, `__eq__`

```python


from validate import Validator, TransactionValidator


class BankAccount:
    """
    Класс, представляющий банковский счет.
    
    Атрибуты класса:
        _next_account_number (int): Счетчик для генерации номеров счетов
        
    Атрибуты экземпляра:
        _account_number (str): Номер счета (закрытый)
        _owner_name (str): Имя владельца (закрытый)
        _balance (float): Баланс счета (закрытый)
        _interest_rate (float): Процентная ставка (закрытый)
        _is_active (bool): Статус счета (активен/закрыт)
    """
    
    # Атрибут класса
    _next_account_number = 1000
    
    def __init__(self, owner_name: str, initial_balance: float = 0.0, interest_rate: float = 1.0):
        """
        Конструктор класса BankAccount.
        
        Args:
            owner_name: Имя владельца счета
            initial_balance: Начальный баланс (по умолчанию 0)
            interest_rate: Процентная ставка (по умолчанию 1.0)
            
        Raises:
            ValueError: При некорректных входных данных
        """
        # Валидация входных данных через отдельный модуль
        Validator.validate_owner_name(owner_name)
        Validator.validate_balance(initial_balance)
        Validator.validate_interest_rate(interest_rate)
        
        # Инициализация закрытых атрибутов
        self._account_number = str(BankAccount._generate_account_number())
        self._owner_name = owner_name.strip()
        self._balance = float(initial_balance)
        self._interest_rate = float(interest_rate)
        self._is_active = True
        
    @classmethod
    def _generate_account_number(cls):
        """Генерирует уникальный номер счета."""
        cls._next_account_number += 1
        return cls._next_account_number
    
    # Свойства (геттеры)
    @property
    def account_number(self) -> str:
        """Возвращает номер счета (только для чтения)."""
        return self._account_number
    
    @property
    def owner_name(self) -> str:
        """Возвращает имя владельца."""
        return self._owner_name
    
    @property
    def balance(self) -> float:
        """Возвращает текущий баланс."""
        return self._balance
    
    @property
    def interest_rate(self) -> float:
        """Возвращает процентную ставку."""
        return self._interest_rate
    
    @property
    def is_active(self) -> bool:
        """Возвращает статус счета."""
        return self._is_active
    
    # Сеттер для имени владельца
    @owner_name.setter
    def owner_name(self, new_name: str) -> None:
        """
        Устанавливает новое имя владельца с валидацией.
        
        Args:
            new_name: Новое имя владельца
            
        Raises:
            ValueError: Если имя некорректно
        """
        Validator.validate_owner_name(new_name)
        self._owner_name = new_name.strip()
    
    # Сеттер для процентной ставки
    @interest_rate.setter
    def interest_rate(self, new_rate: float) -> None:
        """
        Устанавливает новую процентную ставку с валидацией.
        
        Args:
            new_rate: Новая процентная ставка
            
        Raises:
            ValueError: Если ставка некорректна
        """
        Validator.validate_interest_rate(new_rate)
        self._interest_rate = new_rate
    
    # Бизнес-методы
    def deposit(self, amount: float) -> float:
        """
        Вносит средства на счет.
        
        Args:
            amount: Сумма для внесения
            
        Returns:
            float: Новый баланс
            
        Raises:
            ValueError: При некорректной сумме или неактивном счете
        """
        # Используем специализированный валидатор
        TransactionValidator.validate_deposit(self, amount)
        
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount: float) -> float:
        """
        Снимает средства со счета.
        
        Args:
            amount: Сумма для снятия
            
        Returns:
            float: Новый баланс
            
        Raises:
            ValueError: При некорректной сумме, недостаточном балансе или неактивном счете
        """
        # Используем специализированный валидатор
        TransactionValidator.validate_withdrawal(self, amount)
        
        self._balance -= amount
        return self._balance
    
    def apply_interest(self) -> float:
        """
        Начисляет проценты на остаток по счету.
        
        Returns:
            float: Сумма начисленных процентов
            
        Raises:
            ValueError: Если счет неактивен
        """
        Validator.validate_account_status(self._is_active, "Начисление процентов")
        
        interest = self._balance * (self._interest_rate / 100)
        self._balance += interest
        return interest
    
    def close_account(self) -> None:
        """
        Закрывает счет (переводит в неактивное состояние).
        
        Raises:
            ValueError: Если счет уже закрыт
        """
        if not self._is_active:
            raise ValueError("Счет уже закрыт")
        
        self._is_active = False
    
    def activate_account(self) -> None:
        """Активирует закрытый счет."""
        self._is_active = True
    
    def transfer_to(self, target_account: 'BankAccount', amount: float) -> str:
        """
        Переводит средства на другой счет.
        
        Args:
            target_account: Счет получателя
            amount: Сумма перевода
            
        Returns:
            str: Сообщение о результате операции
            
        Raises:
            ValueError: При некорректных параметрах
        """
        # Комплексная проверка перевода
        TransactionValidator.validate_transfer(self, target_account, amount)
        
        # Снятие со своего счета
        self.withdraw(amount)
        
        # Внесение на счет получателя
        target_account.deposit(amount)
        
        return f"Перевод {amount:.2f} на счет {target_account.account_number} выполнен успешно"
    
    def get_account_info(self) -> dict:
        """
        Возвращает информацию о счете в виде словаря.
        
        Returns:
            dict: Словарь с данными счета
        """
        return {
            'account_number': self._account_number,
            'owner_name': self._owner_name,
            'balance': self._balance,
            'interest_rate': self._interest_rate,
            'is_active': self._is_active
        }
    
    # Магические методы
    def __str__(self) -> str:
        """
        Строковое представление для пользователей.
        
        Returns:
            str: Информация о счете в читаемом формате
        """
        status = "✅ Активен" if self._is_active else "❌ Закрыт"
        return (f"┌────────────────────────────────┐\n"
                f"│ Счет №{self._account_number:<18} │\n"
                f"├────────────────────────────────┤\n"
                f"│ Владелец: {self._owner_name:<19} │\n"
                f"│ Баланс: {self._balance:>16,.2f} руб. │\n"
                f"│ Ставка: {self._interest_rate:>16}% │\n"
                f"│ Статус: {status:<21} │\n"
                f"└────────────────────────────────┘")
    
    def __repr__(self) -> str:
        """
        Официальное строковое представление для разработчиков.
        
        Returns:
            str: Представление для отладки
        """
        return (f"BankAccount(owner_name='{self._owner_name}', "
                f"balance={self._balance:.2f}, "
                f"interest_rate={self._interest_rate})")
    
    def __eq__(self, other) -> bool:
        """
        Сравнивает два счета по номеру счета.
        
        Args:
            other: Другой объект для сравнения
            
        Returns:
            bool: True если счета имеют одинаковый номер
        """
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number
    
    def __lt__(self, other) -> bool:
        """
        Сравнивает счета по балансу (для сортировки).
        
        Args:
            other: Другой объект для сравнения
            
        Returns:
            bool: True если баланс текущего счета меньше
        """
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance < other._balance

```

### validate.py
**`validate.py`** — отдельный модуль с логикой проверки данных (валидация имени, баланса, процентной ставки, статуса счета).
```python


class Validator:

    # Константы для валидации
    MIN_BALANCE = 0.0
    MAX_INTEREST_RATE = 10.0
    MIN_INTEREST_RATE = 0.0
    
    @staticmethod
    def validate_owner_name(name: str) -> None:
        """
        Проверяет корректность имени владельца счета.
        
        Args:
            name: Имя владельца для проверки
            
        Raises:
            TypeError: Если имя не является строкой
            ValueError: Если имя пустое или содержит только пробелы
            
        Примеры:
            >>> Validator.validate_owner_name("Иван Петров")
            >>> Validator.validate_owner_name("")  # Возбудит ValueError
        """
        if not isinstance(name, str):
            raise TypeError(f"Имя владельца должно быть строкой, получен {type(name).__name__}")
        
        if not name or not name.strip():
            raise ValueError("Имя владельца не может быть пустым")
        
        # Дополнительная проверка на минимальную длину
        if len(name.strip()) < 2:
            raise ValueError("Имя владельца должно содержать минимум 2 символа")
    
    @staticmethod
    def validate_balance(balance: float) -> None:
        """
        Проверяет корректность баланса счета.
        
        Args:
            balance: Баланс для проверки
            
        Raises:
            TypeError: Если баланс не является числом
            ValueError: Если баланс меньше минимального допустимого
            
        Примеры:
            >>> Validator.validate_balance(1000.50)
            >>> Validator.validate_balance(-100)  # Возбудит ValueError
        """
        if not isinstance(balance, (int, float)):
            raise TypeError(f"Баланс должен быть числом, получен {type(balance).__name__}")
        
        if balance < Validator.MIN_BALANCE:
            raise ValueError(f"Баланс не может быть меньше {Validator.MIN_BALANCE}")
    
    @staticmethod
    def validate_interest_rate(rate: float) -> None:
        """
        Проверяет корректность процентной ставки.
        
        Args:
            rate: Процентная ставка для проверки
            
        Raises:
            TypeError: Если ставка не является числом
            ValueError: Если ставка вне допустимого диапазона
            
        Примеры:
            >>> Validator.validate_interest_rate(5.5)
            >>> Validator.validate_interest_rate(15)  # Возбудит ValueError
        """
        if not isinstance(rate, (int, float)):
            raise TypeError(f"Процентная ставка должна быть числом, получен {type(rate).__name__}")
        
        if rate < Validator.MIN_INTEREST_RATE or rate > Validator.MAX_INTEREST_RATE:
            raise ValueError(
                f"Процентная ставка должна быть от {Validator.MIN_INTEREST_RATE} "
                f"до {Validator.MAX_INTEREST_RATE}%"
            )
    
    @staticmethod
    def validate_positive_amount(amount: float, operation_name: str = "Операция") -> None:
        """
        Проверяет, что сумма операции положительная.
        
        Args:
            amount: Сумма для проверки
            operation_name: Название операции (для сообщения об ошибке)
            
        Raises:
            TypeError: Если сумма не является числом
            ValueError: Если сумма меньше или равна нулю
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Сумма должна быть числом, получен {type(amount).__name__}")
        
        if amount <= 0:
            raise ValueError(f"{operation_name}: сумма должна быть положительной")
    
    @staticmethod
    def validate_account_status(is_active: bool, operation_name: str = "Операция") -> None:
        """
        Проверяет, что счет активен.
        
        Args:
            is_active: Статус счета
            operation_name: Название операции (для сообщения об ошибке)
            
        Raises:
            ValueError: Если счет неактивен
        """
        if not is_active:
            raise ValueError(f"{operation_name} невозможна: счет закрыт")
    
    @staticmethod
    def validate_sufficient_balance(balance: float, amount: float) -> None:
        """
        Проверяет, что на счете достаточно средств.
        
        Args:
            balance: Текущий баланс
            amount: Запрашиваемая сумма
            
        Raises:
            ValueError: Если недостаточно средств
        """
        if amount > balance:
            raise ValueError(
                f"Недостаточно средств. Доступно: {balance:.2f}, "
                f"запрошено: {amount:.2f}"
            )
    
    @staticmethod
    def validate_transfer_target(target) -> None:
        """
        Проверяет, что целевой объект является банковским счетом.
        
        Args:
            target: Объект для проверки
            
        Raises:
            TypeError: Если target не является BankAccount
        """
        # Импортируем здесь, чтобы избежать циклического импорта
        from model import BankAccount
        
        if not isinstance(target, BankAccount):
            raise TypeError(
                f"Получатель должен быть банковским счетом (BankAccount), "
                f"получен {type(target).__name__}"
            )
    
    @staticmethod
    def format_validation_error(error: Exception) -> str:
        """
        Форматирует сообщение об ошибке валидации.
        
        Args:
            error: Исключение валидации
            
        Returns:
            str: Отформатированное сообщение об ошибке
        """
        return f"❌ Ошибка валидации: {error}"


# Дополнительный класс для специфических проверок банковских операций
class TransactionValidator:
    """
    Класс для валидации банковских транзакций.
    """
    
    @staticmethod
    def validate_deposit(account, amount: float) -> None:
        """
        Комплексная проверка для операции депозита.
        
        Args:
            account: Банковский счет
            amount: Сумма депозита
        """
        Validator.validate_account_status(account.is_active, "Депозит")
        Validator.validate_positive_amount(amount, "Депозит")
    
    @staticmethod
    def validate_withdrawal(account, amount: float) -> None:
        """
        Комплексная проверка для операции снятия.
     
        """
        Validator.validate_account_status(account.is_active, "Снятие")
        Validator.validate_positive_amount(amount, "Снятие")
        Validator.validate_sufficient_balance(account.balance, amount)
    
    @staticmethod
    def validate_transfer(sender, receiver, amount: float) -> None:
        """
        Комплексная проверка для перевода между счетами.
        
        Args:
            sender: Счет отправителя
            receiver: Счет получателя
            amount: Сумма перевода
        """
        Validator.validate_account_status(sender.is_active, "Перевод (отправитель)")
        Validator.validate_account_status(receiver.is_active, "Перевод (получатель)")
        Validator.validate_positive_amount(amount, "Перевод")
        Validator.validate_sufficient_balance(sender.balance, amount)
        Validator.validate_transfer_target(receiver)
```


### demo.py

**`demo.py`** — демонстрационный файл. Показывает:
- Создание счетов и базовые операции
- Работу свойств и валидации
- Обработку ошибок (try/except)
- Изменение состояния счета (активен/закрыт)
- Сравнение и сортировку объектов
- Переводы между счетами

```python
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
```





## Теория

### Класс и объект
**Класс** — это шаблон для создания объектов. Он определяет структуру и поведение будущих объектов.
**Объект (экземпляр)** — конкретная реализация класса, обладающая своими данными.

### Инкапсуляция
Это принцип сокрытия внутренних данных объекта от прямого доступа извне. В Python реализуется через:
- Защищенные поля с одним подчеркиванием: `_balance`
- Приватные поля с двумя подчеркиваниями: `__pin`

Доступ к данным осуществляется через специальные методы.

### Свойства @property
Механизм, позволяющий управлять доступом к атрибутам:
- **Геттер** — для чтения значения
- **Сеттер** — для установки значения с проверкой
- **Делитер** — для удаления атрибута

### Магические методы
Специальные методы с двумя подчеркиваниями в начале и конце:
- `__init__` — конструктор, вызывается при создании объекта
- `__str__` — строковое представление для пользователей
- `__repr__` — официальное представление для разработчиков
- `__eq__` — определяет поведение оператора ==
- `__lt__` — определяет поведение оператора < (для сортировки)

### Атрибуты класса и экземпляра
**Атрибуты класса** — принадлежат самому классу, общие для всех объектов.
**Атрибуты экземпляра** — принадлежат конкретному объекту, у каждого объекта свои значения.

### Валидация данных
Процесс проверки корректности входных данных:
- Проверка типа данных (число, строка)
- Проверка диапазона (положительное число, не больше максимума)
- Проверка логической корректности (достаточно средств на счете)

### Состояние объекта
Объект может находиться в разных состояниях (активен/закрыт), которые влияют на доступность операций.


## Класс BankAccount

### Атрибуты (закрытые)
- `_account_number` — номер счета (генерируется автоматически)
- `_owner_name` — имя владельца счета
- `_balance` — текущий баланс
- `_interest_rate` — процентная ставка
- `_is_active` — статус счета (активен/закрыт)

### Атрибут класса
- `_next_account_number` — счетчик для генерации уникальных номеров счетов

### Свойства
- `account_number` — только для чтения
- `balance` — только для чтения
- `owner_name` — чтение и запись с валидацией
- `interest_rate` — чтение и запись с валидацией
- `is_active` — только для чтения

### Магические методы
- `__str__` — красивое отображение счета для пользователя
- `__repr__` — представление для разработчиков (отладка)
- `__eq__` — сравнение счетов по номеру
- `__lt__` — сравнение по балансу (для сортировки)

### Бизнес-методы
- `deposit(amount)` — внесение средств на счет
- `withdraw(amount)` — снятие средств со счета
- `apply_interest()` — начисление процентов на остаток
- `transfer_to(target_account, amount)` — перевод средств на другой счет
- `close_account()` — закрытие счета
- `activate_account()` — активация счета

## Модуль validate.py

### Класс Validator
Статические методы для базовой валидации:
- `validate_owner_name(name)` — проверка имени владельца
- `validate_balance(balance)` — проверка баланса
- `validate_interest_rate(rate)` — проверка процентной ставки
- `validate_positive_amount(amount)` — проверка положительности суммы
- `validate_account_status(is_active)` — проверка активности счета
- `validate_sufficient_balance(balance, amount)` — проверка достаточности средств

### Класс TransactionValidator
Специализированные методы для комплексной проверки транзакций:
- `validate_deposit(account, amount)` — проверка депозита
- `validate_withdrawal(account, amount)` — проверка снятия
- `validate_transfer(sender, receiver, amount)` — проверка перевода

## Демонстрация работы

В файле `demo.py` демонстрируются:
1. Создание счетов с различными параметрами
2. Выполнение операций (депозит, снятие, начисление процентов)
3. Работа свойств и валидации
4. Обработка ошибочных ситуаций через try/except
5. Изменение состояния счета (активация/закрытие)
6. Сравнение и сортировка объектов
7. Переводы между счетами

## Вывод
В ходе лабораторной работы реализован класс `BankAccount` с инкапсуляцией, свойствами `@property`, магическими методами и бизнес-логикой. Валидация вынесена в отдельный модуль. Цели работы достигнуты.