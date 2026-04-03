"""
Модуль для валидации данных банковского счета.
Содержит класс Validator с набором статических методов для проверки данных.
"""

class Validator:
    """
    Класс с методами валидации для банковского счета.
    Все методы являются статическими и не требуют создания экземпляра.
    """
    
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
        """
        if not isinstance(name, str):
            raise TypeError(f"Имя владельца должно быть строкой, получен {type(name).__name__}")
        
        if not name or not name.strip():
            raise ValueError("Имя владельца не может быть пустым")
        
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
        from model import BankAccount
        
        if not isinstance(target, BankAccount):
            raise TypeError(
                f"Получатель должен быть банковским счетом (BankAccount), "
                f"получен {type(target).__name__}"
            )


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
        
        Args:
            account: Банковский счет
            amount: Сумма снятия
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