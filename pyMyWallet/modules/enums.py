__author__ = 'dimv36'
from enum import Enum


class WalletItemType(Enum):
    INCOMING = 0
    EXPENSE = 1
    SAVING = 2
    LOAN = 3
    DEBT = 4


class WalletItemModelType(Enum):
    INDEX_DAY = 0
    INDEX_MONTH = 1
    INDEX_YEAR = 2
    INDEX_INCOMING = 3
    INDEX_EXPENSE = 4
    INDEX_SAVINGS = 5
    INDEX_LOAN = 6
    INDEX_DEBT = 7
    INDEX_DESCRIPTION = 8
