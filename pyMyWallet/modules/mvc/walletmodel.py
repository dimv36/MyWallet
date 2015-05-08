__author__ = 'dimv36'
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QAbstractTableModel, Qt

from modules.mvc.walletitem import WalletRow


class WalletModelException(Exception):
    pass


class WalletModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        tr = QCoreApplication.translate
        self.__header_data = [tr('WalletModel', 'Date'), tr('WalletModel', 'Incoming'),
                              tr('WalletModel', 'State of incoming'),
                              tr('WalletModel', 'Expense'), tr('WalletModel', 'State of expense'),
                              tr('WalletModel', 'Loan'), tr('WalletModel', 'State of loan'),
                              tr('WalletModel', 'Debt'), tr('WalletModel', 'State of debt')]
        self.__items = [WalletRow(), WalletRow()]

    def data(self, index, role=None):
        if not index.isValid():
            raise WalletModelException('Invalid index')
        if index.row() >= len(self.__items):
            raise WalletModelException('Incorrect item number: %d' % index.row())
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return self.__items[index.row()].date()
            elif index.column() in range(1, 3):
                return self.__items[index.row()].incoming()
            elif index.column() in range(3, 5):
                return self.__items[index.row()].expense()
            elif index.column() in range(5, 7):
                return self.__items[index.row()].loan()
            elif index.column() in range(7, 9):
                return self.__items[index.row()].debt()

    def setData(self, index, value, role=None):
        if index.isValid() and role == Qt.EditRole:
            if index.column() == 0:
                self.__items[index.row()].set_date(value)
            elif index.column() == 1:
                self.__items[index.row()].incoming().set_sum(value)
            elif index.column() == 2:
                self.__items[index.row()].incoming().set_description(value)
            elif index.column() == 3:
                self.__items[index.row()].expense().set_sum(value)
            elif index.column() == 4:
                self.__items[index.row()].expense().set_description(value)
            elif index.column() == 5:
                self.__items[index.row()].loan().set_sum(value)
            elif index.column() == 6:
                self.__items[index.row()].loan().set_description(value)
            elif index.column() == 7:
                self.__items[index.row()].debt().set_sum(value)
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