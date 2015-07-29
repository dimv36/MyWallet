__author__ = 'dimv36'
from enum import Enum


class WalletItemType(Enum):
    INCOMING = 0
    EXPENSE = 1
    SAVING = 2
    LOAN = 3
    DEBT = 4


class WalletItemModelType(Enum):
    INDEX_DATE = 0
    INDEX_INCOMING = 1
    INDEX_INCOMING_DESCRIPTION = 2
    INDEX_EXPENSE = 3
    INDEX_EXPENSE_DESCRIPTION = 4
    INDEX_SAVINGS = 5
    INDEX_SAVINGS_DESCRIPTION = 6
    INDEX_LOAN = 7
    INDEX_LOAN_DESCRIPTION = 8
    INDEX_DEBT = 9
    INDEX_DEBT_DESCRIPTION = 10
