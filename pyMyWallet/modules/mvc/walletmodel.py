__author__ = 'dimv36'
from PyQt5.QtCore import Qt, QAbstractTableModel
from modules.mvc.walletdatabase import *
from modules.enums import *


class WalletModelException(Exception):
    pass


class WalletModel(QAbstractTableModel):
    __HEADERS = {
        WalletItemModelType.INDEX_DATE.value: tr('WalletModel', 'Date'),
        WalletItemModelType.INDEX_INCOMING.value: tr('WalletModel', 'Incoming'),
        WalletItemModelType.INDEX_EXPENSE.value: tr('WalletModel', 'Expense'),
        WalletItemModelType.INDEX_SAVINGS.value: tr('WalletModel', 'Savings'),
        WalletItemModelType.INDEX_DEBT.value: tr('WalletModel', 'Debt'),
        WalletItemModelType.INDEX_DESCRIPTION.value: tr('WalletModel', 'Description')
    }
    __signal_data_changed = pyqtSignal()
    signal_wallet_metadata_changed = pyqtSignal([WalletData])

    def __init__(self):
        super().__init__()
        self.__data = []
        self.__db = WalletDatabase()
        # Инициализация сигналов и слотов
        self.__signal_data_changed.connect(self.__on_update)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.__HEADERS)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.__HEADERS.get(section, None)
            if not header:
                raise Warning('Unexpected section: %d', section)
            return header
        elif orientation == Qt.Vertical:
            return section
        return None

    def data(self, index, role=None):
        if (not index.isValid() or
            len(self.__data) <= index.row() or
                not role == Qt.DisplayRole):
            return None
        return self.__data[index.row()][index.column()]

    @pyqtSlot()
    def __on_update(self):
        result = self.__db.get_metadata()
        self.signal_wallet_metadata_changed.emit(result)

    def set_wallet_path(self, directory, wallet):
        path = '%s/%s' % (directory, wallet)
        if path and not self.__db.connection_path() == path:
            try:
                self.beginResetModel()
                self.__db.connect(path)
                self.__data = self.__db.get_data()
                self.endResetModel()
            except WalletDatabaseException as e:
                raise WalletModelException(e)
            # Отправляем сигнал на изменение данных
            self.__signal_data_changed.emit()

    @staticmethod
    def create_new_wallet(wallet_path):
        """
        Создание нового бумажника
        :param wallet_path: str
        :return: None
        """
        try:
            WalletDatabase.create_wallet(wallet_path)
        except WalletDatabaseException as e:
            raise WalletModelException(tr('WalletModel', 'Could not create new wallet: %s' % e))

    def add_entry(self, item):
        """
        Добавить запись в бумажник
        :param item: dict
        :return: None
        """
        self.beginResetModel()
        try:
            row = self.__db.add_data(item)
            self.__data.append(row)
        except WalletDatabaseException as e:
            raise WalletModelException(tr('WalletModel', '%s' % e))
        # Сортируем строки
        self.__data = sorted(self.__data)
        self.endResetModel()
        self.__signal_data_changed.emit()

    def remove_entry(self, item):
        """
        Удалить запись из бумажника
        :param item: dict
        :return: None
        """
        self.beginResetModel()
        try:
            row = self.__db.remove_data(item)
            self.__data.remove(row)
        except WalletDatabaseException as e:
            raise WalletModelException(tr('WalletModel', '%s' % e))
        self.endResetModel()
        self.__signal_data_changed.emit()

    def change_balance_at_start_of_month(self, balance):
        """
        Изменить баланс на начало месяца текущего месяца
        :param balance: float
        :return: None
        """
        try:
            self.__db.change_balance_at_start_of_month(balance)
        except WalletDatabaseException as e:
            raise WalletModelException(tr('WalletModel', e))
        self.__signal_data_changed.emit()

    def get_metadata(self):
        return self.__db.get_metadata()

    # Следующие методы используются при построении статистики в классе StatisticDialog
    def get_statistic_items(self):
        """
        Получить периоды отображения статистики
        :return: dict {year: {month: WalletData}}
        """
        try:
            return self.__db.get_statistic_items()
        except WalletDatabaseException as e:
            raise WalletModelException(tr('WalletModel', e))
