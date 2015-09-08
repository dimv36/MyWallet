from PyQt5.QtCore import QCoreApplication, Qt, QDate, QObject, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlRecord
from modules.enums import WalletItemModelType


class WalletModelException(Exception):
    pass


class WalletModel(QSqlTableModel):
    WALLET_SQL_QUERY = 'SELECT day, month, year, ' \
                       'incoming, expense, saving, ' \
                       'loan, debt, description FROM wallet_data ' \
                       'WHERE month = %d AND year = %d;'

    class Communicate(QObject):
        signal_model_was_changed = pyqtSignal()

    class WalletData:
        def __init__(self):
            self.balance_at_start = float()
            self.incoming = float()
            self.expense = float()
            self.savings = float()
            self.loan = float()
            self.debt = float()

    def __init__(self, wallet_file_path):
        super().__init__()
        self.__wallet = wallet_file_path
        self.__db = QSqlDatabase.addDatabase('QSQLITE')
        self.__db.setDatabaseName(self.__wallet)
        if not self.__db.open():
            raise WalletModelException(QCoreApplication.translate('WalletModel',
                                                                  'Can\'t connect to wallet %s') % self.__wallet)
        self.setQuery(QSqlQuery(self.WALLET_SQL_QUERY % (QDate.currentDate().month(),
                                                         QDate.currentDate().year())))
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

    def get_wallet_info(self):
        def convert_to_float(_query, _record, _field):
            result = float()
            try:
                result = float(_query.value(_record.indexOf(_field)))
            except ValueError:
                pass
            return result

        wallet_data = self.WalletData()
        query = QSqlQuery()
        # Получаем баланс на начало месяца
        balance_at_start_query = 'SELECT balance_at_start FROM wallet_month_data WHERE month = %d AND year = %d' % \
                                 (
                                     QDate.currentDate().month(), QDate.currentDate().year()
                                 )
        if not query.exec(balance_at_start_query):
            raise WalletModelException('Could not execute query \'%s\'', query)
        elif query.next():
            record = query.record()
            wallet_data.balance_at_start = convert_to_float(query, record, 'balance_at_start')
        # Получаем информацию о доходах и расходах
        wallet_info_query = 'SELECT sum(incoming) AS incoming, ' \
                            'sum(expense) AS expense FROM wallet_data WHERE month = %d AND year = %d;' % \
                            (
                                QDate.currentDate().month(), QDate.currentDate().year()
                            )
        if not query.exec(wallet_info_query):
            raise WalletModelException('Could not execute query \'%s\'' % wallet_info_query)
        elif query.next():
            record = query.record()
            wallet_data.incoming = convert_to_float(query, record, 'incoming')
            wallet_data.expense = convert_to_float(query, record, 'expense')
        # Получаем информацию о накоплениях, долгах, займах
        summary_query = 'SELECT sum(saving) AS saving, sum(loan) AS loan, sum(debt) AS debt FROM wallet_data;'
        if not query.exec(summary_query):
            raise WalletModelException('Could not execute query \'%s\'' % summary_query)
        elif query.next():
            record = query.record()
            wallet_data.savings = convert_to_float(query, record, 'saving')
            wallet_data.loan = convert_to_float(query, record, 'loan')
            wallet_data.debt = convert_to_float(query, record, 'debt')
        return wallet_data
