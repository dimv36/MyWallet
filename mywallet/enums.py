__author__ = 'dimv36'
from enum import Enum


class WalletModelColumns:
    (INDEX_DATE,
     INDEX_INCOMING,
     INDEX_EXPENSE,
     INDEX_SAVINGS,
     INDEX_DEBT,
     INDEX_DESCRIPTION) = range(0, 6)


class WalletMetaDataType:
    (INDEX_BALANCE_AT_START,
     INDEX_BALANCE_AT_END,
     INDEX_INCOMING,
     INDEX_EXPENSE,
     INDEX_SAVINGS,
     INDEX_DEBT) = range(0, 6)


class MonthName(Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12
