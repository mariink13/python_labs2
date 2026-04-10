

import sys
import os

# Добавляем путь к папке lab01 (относительно расположения этого файла)
sys.path.append(os.path.join(os.path.dirname(__file__), '../lab01'))

# Импортируем настоящий класс BankAccount
from model import BankAccount

# Экспортируем его как часть интерфейса этого модуля
__all__ = ['BankAccount']

