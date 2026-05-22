import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../lab03'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../lab05'))

from models import BankAccount, SavingsAccount, CreditAccount
from collection import BankAccountCollection
from app import NoFee, FlatFee, PercentFee, TieredFee

def _account_to_dict(account):
    data = {
        'type': account.__class__.__name__,
        'owner': account._owner_name,
        'balance': account.balance,
    }
    if isinstance(account, SavingsAccount):
        data['interest_rate'] = account._interest_rate
    elif isinstance(account, CreditAccount):
        data['credit_limit'] = account._credit_limit
    return data

def _dict_to_account(data):
    typ = data['type']
    owner = data['owner']
    balance = data['balance']
    if typ == 'SavingsAccount':
        return SavingsAccount(owner, balance, data.get('interest_rate', 0.0))
    elif typ == 'CreditAccount':
        return CreditAccount(owner, balance, data.get('credit_limit', 0))
    else:
        return BankAccount(owner, balance)

def save(collection, filepath):
    data = [_account_to_dict(acc) for acc in collection.get_all()]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return BankAccountCollection()
    coll = BankAccountCollection()
    for item in data:
        try:
            acc = _dict_to_account(item)
            coll.add(acc)
        except Exception:
            continue
    return coll