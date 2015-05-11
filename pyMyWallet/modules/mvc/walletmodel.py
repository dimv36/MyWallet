__author__ = 'dimv36'
from PyQt5.QtCore import QCoreApplication, QAbstractTableModel, Qt, QDate
from lxml import etree

from modules.mvc.walletitem import WalletRow, WalletItem, WalletItemType


class WalletModelException(Exception):
    pass


class WalletModel(QAbstractTableModel):
    DATE_FORMAT = 'dd.MM.yyyy'

    def __init__(self, wallet_file_path):
        super().__init__()
        tr = QCoreApplication.translate
        self.__header_data = [tr('WalletModel', 'Date'), tr('WalletModel', 'Incoming'),
                              tr('WalletModel', 'State of incoming'),
                              tr('WalletModel', 'Expense'), tr('WalletModel', 'State of expense'),
                              tr('WalletModel', 'Loan'), tr('WalletModel', 'State of loan'),
                              tr('WalletModel', 'Debt'), tr('WalletModel', 'State of debt')]
        self.__items = []
        self.__wallet = wallet_file_path
        self.__read_wallet()

    def data(self, index, role=None):
        if not index.isValid():
            raise WalletModelException('Invalid index')
        if index.row() >= len(self.__items):
            raise WalletModelException('Incorrect item number: %d' % index.row())
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return self.__items[index.row()].date()
            elif index.column() == 1:
                return self.__items[index.row()].incoming().value()
            elif index.column() == 2:
                return self.__items[index.row()].incoming().description()
            elif index.column() == 3:
                return self.__items[index.row()].expense().value()
            elif index.column() == 4:
                return self.__items[index.row()].expense().description()
            elif index.column() == 5:
                return self.__items[index.row()].loan().value()
            elif index.column() == 6:
                return self.__items[index.row()].loan().description()
            elif index.column() == 7:
                return self.__items[index.row()].debt().value()
            elif index.column() == 8:
                return self.__items[index.row()].debt().description()

    def setData(self, index, value, role=None):
        if index.isValid() and role == Qt.EditRole:
            if index.column() == 0:
                self.__items[index.row()].set_date(value)
            elif index.column() == 1:
                self.__items[index.row()].incoming().set_value(value)
            elif index.column() == 2:
                self.__items[index.row()].incoming().set_description(value)
            elif index.column() == 3:
                self.__items[index.row()].expense().set_value(value)
            elif index.column() == 4:
                self.__items[index.row()].expense().set_description(value)
            elif index.column() == 5:
                self.__items[index.row()].loan().set_value(value)
            elif index.column() == 6:
                self.__items[index.row()].loan().set_description(value)
            elif index.column() == 7:
                self.__items[index.row()].debt().set_value(value)
            elif index.column() == 8:
                self.__items[index.row()].debt().set_description(value)

    def rowCount(self, index=None, *args, **kwargs):
        return len(self.__items)

    def columnCount(self, index=None, *args, **kwargs):
        return len(self.__header_data)

    def headerData(self, section, orientation, role=None):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__header_data[section]
        else:
            return '%s' % (section + 1)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return super().flags(index) or Qt.ItemIsEditable

    def create_new_wallet(self, wallet_path):
        self.__wallet = wallet_path
        root = etree.Element('mywallet')
        tree = etree.ElementTree(root)
        tree.write(self.__wallet)

    def read_wallet(self, wallet_path=None):
        if wallet_path is not None:
            self.__wallet = wallet_path
        self.__read_wallet()

    def __append_entry(self, date, entries, entry_type):
        for entry in entries:
            item = WalletItem(entry.attrib['value'], entry.attrib['description'])
            row = WalletRow()
            if entry_type == WalletItemType.INCOMING:
                row.set_incoming(date, item)
            elif entry_type == WalletItemType.EXPENSE:
                row.set_expense(date, item)
            elif entry_type == WalletItemType.LOAN:
                row.set_loan(date, item)
            elif entry_type == WalletItemType.DEBT:
                row.set_debt(date, item)
            self.__items.append(row)

    def __read_wallet(self):
        if self.__items:
            for item in self.__items:
                self.__items.remove(item)
        print(self.__wallet)
        tree = etree.parse(self.__wallet)
        if tree:
            root = tree.getroot()
            current_date = QDate.currentDate()
            # Получаем узел с текущим годом
            try:
                year = root.findall('year')[-1]
                # Получаем узел с последнем месяцем, данные по которому содержатся в XML
                month = year.findall('month')[-1]
                if int(year.attrib['value']) == current_date.year() and int(month.attrib['value']) == current_date.month():
                    # Получаем список узлов текущего месяца
                    days = month.findall('day')
                    for day in days:
                        incoming_entries = day.findall('incoming')
                        expenses_entries = day.findall('expense')
                        loan_entries = day.findall('loan')
                        debt_entries = day.findall('debt')
                        # Создаём сущность даты элемента, которому соответствуют данные
                        day_date = QDate(int(year.attrib['value']), int(month.attrib['value']),
                                         int(day.attrib['value'])).toString(self.DATE_FORMAT)
                        # Добавляем данные в модель
                        self.__append_entry(day_date, incoming_entries, WalletItemType.INCOMING)
                        self.__append_entry(day_date, expenses_entries, WalletItemType.EXPENSE)
                        self.__append_entry(day_date, loan_entries, WalletItemType.LOAN)
                        self.__append_entry(day_date, debt_entries, WalletItemType.DEBT)
            except IndexError:
                pass
            print(self.__items)

    def write_wallet(self):
        pass