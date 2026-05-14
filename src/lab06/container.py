

from typing import TypeVar, Generic, Callable, Optional, Protocol, get_args

# ---------- Протоколы для структурной типизации ----------
class Displayable(Protocol):
    def display(self) -> str:
        ...

class Scorable(Protocol):
    def score(self) -> float:
        ...

# ---------- TypeVar с ограничениями ----------
D = TypeVar('D', bound=Displayable)   # только объекты с display()
S = TypeVar('S', bound=Scorable)      # только объекты с score()
T = TypeVar('T')                      # без ограничений
R = TypeVar('R')                      # для map – тип результата

# ---------- Generic-коллекция ----------
class TypedCollection(Generic[T]):
    """
    Обобщённая коллекция, хранящая элементы типа T.
    Реализует интерфейс с методами add, remove, get_all, find, filter, map.
    """

    def __init__(self) -> None:
        self._items: list[T] = []
        # Определяем ожидаемый тип T (работает в Python 3.12+)
        if hasattr(self, '__orig_class__'):
            self._item_type = get_args(self.__orig_class__)[0]
        else:
            self._item_type = None

    def add(self, item: T) -> None:
        """Добавляет элемент, проверяя тип (если тип известен)."""
        if self._item_type is not None and not isinstance(item, self._item_type):
            raise TypeError(f"Ожидается объект типа {self._item_type.__name__}, получен {type(item).__name__}")
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._items.remove(item)

    def get_all(self) -> list[T]:
        return self._items.copy()

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        return [transform(item) for item in self._items]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def __str__(self) -> str:
        if not self._items:
            return "TypedCollection (empty)"
        lines = [f"TypedCollection with {len(self._items)} items:"]
        for idx, item in enumerate(self._items, 1):
            lines.append(f"--- Item {idx} ---")
            lines.append(str(item))
        return "\n".join(lines)