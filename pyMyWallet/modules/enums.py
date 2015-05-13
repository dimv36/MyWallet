__author__ = 'dimv36'
from enum import Enum


class WalletItemType(Enum):
    INCOMING = 0
    EXPENSE = 1
    LOAN = 2
    DEBT = 3


class WalletItemModelType(Enum):
    INDEX_DATE = 0
    INDEX_INCOMING = 1
    INDEX_INCOMING_DESCRIPTION = 2
    INDEX_EXPENSE = 3
    INDEX_EXPENSE_DESCRIPTION = 4
    INDEX_LOAN = 5
    INDEX_LOAN_DESCRIPTION = 6
    INDEX_DEBT = 7
    INDEX_DEBT_DESCRIPTION = 8
