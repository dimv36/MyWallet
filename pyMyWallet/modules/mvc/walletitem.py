__author__ = 'dimv36'
from enum import Enum


class WalletItem:
    def __init__(self):
        self._sum = ''
        self._description = ''

    def sum(self):
        return self._sum

    def description(self):
        return self._description

    def set_sum(self, value):
        self._sum = value

    def set_description(self, value):
        self._description = value


class WalletException(Exception):
    pass


class WalletItemType(Enum):
    INCOMING = 0
    EXPENSE = 1
    LOAN = 2
    DEBT = 3


class WalletRow:
    def __init__(self):
        self._date = None
        self._incoming = WalletItem()
        self._expense = WalletItem()
        self._debt = WalletItem()
        self._loan = WalletItem()
        self._type = WalletItem()

    def __set_item(self, date, item, item_type):
        if date and item:
            self._date = date
            self._type = item_type
            if self._type == WalletItemType.INCOMING:
                self._incoming = item
            elif self._type == WalletItemType.EXPENSE:
                self._expense = item
            elif self._type == WalletItemType.LOAN:
                self._loan = item
            elif self._type == WalletItemType.DEBT:
                self._expense = item
            else:
                raise WalletException('Unknown wallet type item: %d' % self._type)
        else:
            raise WalletException('Error when adding item at model')

    def date(self):
        return self._date

    def incoming(self):
        return self._incoming

    def expense(self):
        return self._expense

    def loan(self):
        return self._loan

    def debt(self):
        return self._debt

    def type(self):
        return self._type

    def set_date(self, date):
        self._date = date

    def set_incoming(self, date, item):
        self.__set_item(date, item, WalletItemType.INCOMING)

    def set_expense(self, date, item):
        self.__set_item(date, item, WalletItemType.EXPENSE)

    def set_loan(self, date, item):
        self.__set_item(date, item, WalletItemType.LOAN)

    def set_debt(self, date, item):
        self.__set_item(date, item, WalletItemType.DEBT)