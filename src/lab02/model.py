"""
Модуль для работы с банковским счетом.
Использует отдельный модуль валидации validate.py.
"""

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

