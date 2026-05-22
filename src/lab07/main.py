import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../lab05'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../lab03'))

from storage import load, save
from collection import BankAccountCollection
from app import BankApp
from cli import ConsoleInterface

DATA_FILE = "bank_data.json"

def main():
    collection = load(DATA_FILE)
    app = BankApp(collection)
    cli = ConsoleInterface(app)
    cli.run()
    save(collection, DATA_FILE)
    print(f"Данные сохранены в {DATA_FILE}")

if __name__ == "__main__":
    main()