__author__ = 'dimv36'
from PyQt5.QtCore import QCoreApplication, QAbstractTableModel, Qt, QDate, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from modules.enums import WalletItemModelType


class WalletModelException(Exception):
    pass


class WalletModel(QSqlTableModel):
    WALLET_DATA_TABLE = 'wallet_data'
    WALLET_SQL_QUERY = 'SELECT day, month, year,' \
                       ' incoming, expense, saving, ' \
                       'loan, debt, description FROM wallet_data;'

    class Communicate(QObject):
        signal_model_was_changed = pyqtSignal()

    class WalletData:
        def __init__(self):
            self.incoming = float()
            self.expense = float()
            self.savings = float()
            self.loan = float()
            self.debt = float()
            self.balance = float()

    def __init__(self, wallet_file_path):
        super().__init__()
        print(wallet_file_path)
        # self.__header_data = [QCoreApplication.translate('WalletModel', 'Date'),
        #                       QCoreApplication.translate('WalletModel', 'Incoming'),
        #                       QCoreApplication.translate('WalletModel', 'State of incoming'),
        #                       QCoreApplication.translate('WalletModel', 'Expense'),
        #                       QCoreApplication.translate('WalletModel', 'State of expense'),
        #                       QCoreApplication.translate('WalletModel', 'Savings'),
        #                       QCoreApplication.translate('WalletModel', 'State of savings'),
        #                       QCoreApplication.translate('WalletModel', 'Loan'),
        #                       QCoreApplication.translate('WalletModel', 'State of loan'),
        #                       QCoreApplication.translate('WalletModel', 'Debt'),
        #                       QCoreApplication.translate('WalletModel', 'State of debt')]
        self.__wallet = wallet_file_path
        self.__db = QSqlDatabase.addDatabase('QSQLITE')
        self.__db.setDatabaseName(self.__wallet)
        if not self.__db.open():
            raise WalletModelException(QCoreApplication.translate('WalletModel',
                                                                  'Can\'t connect to wallet %s') % self.__wallet)
        self.setQuery(QSqlQuery(self.WALLET_SQL_QUERY))
        self.setHeaderData(WalletItemModelType.INDEX_DAY.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Day'))
        self.setHeaderData(WalletItemModelType.INDEX_MONTH.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Month'))
        self.setHeaderData(WalletItemModelType.INDEX_YEAR.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Year'))
        self.setHeaderData(WalletItemModelType.INDEX_INCOMING.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Incoming'))
        self.setHeaderData(WalletItemModelType.INDEX_EXPENSE.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Expense'))
        self.setHeaderData(WalletItemModelType.INDEX_SAVINGS.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Savings'))
        self.setHeaderData(WalletItemModelType.INDEX_LOAN.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Loan'))
        self.setHeaderData(WalletItemModelType.INDEX_DEBT.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Debt'))