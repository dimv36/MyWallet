__author__ = 'dimv36'
from enum import Enum


class WalletItemModelType(Enum):
    INDEX_DATE = 0
    INDEX_INCOMING = 1
    INDEX_EXPENSE = 2
    INDEX_SAVINGS = 3
    INDEX_DEBT = 4
    INDEX_DESCRIPTION = 5


class WalletMetaDataType(Enum):
    INDEX_BALANCE_AT_START = 0
    INDEX_BALANCE_AT_END = 1
    INDEX_INCOMING = 2
    INDEX_EXPENSE = 3
    INDEX_SAVINGS = 4
    INDEX_DEBT = 5