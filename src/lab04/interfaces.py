from abc import ABC, abstractmethod

class Printable(ABC):
    """Интерфейс для объектов, которые могут быть преобразованы в строку."""
    
    @abstractmethod
    def to_string(self) -> str:
        """Вернуть строковое представление объекта."""
        pass

class Comparable(ABC):
    """Интерфейс для объектов, поддерживающих сравнение."""
    
    @abstractmethod
    def compare_to(self, other: 'Comparable') -> int:
        """
        Сравнить текущий объект с другим.
        Возвращает:
            отрицательное число, если self < other
            0, если self == other
            положительное число, если self > other
        """
        pass