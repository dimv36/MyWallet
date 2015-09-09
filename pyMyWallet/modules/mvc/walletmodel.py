from PyQt5.QtCore import QCoreApplication, Qt, QDate, QObject, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlRecord
from modules.enums import WalletItemModelType


class WalletModelException(Exception):
    pass


class WalletModel(QSqlTableModel):
    WALLET_SQL_QUERY = 'SELECT day, month, year, ' \
                       'incoming, expense, saving, ' \
                       'loan, debt, description FROM wallet_data ' \
                       'WHERE month = %d AND year = %d ORDER BY day;'

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
        self.__init_model()
        self.read_wallet()

    def __init_model(self):
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
        wallet_data_query = 'SELECT ' \
                            '(SELECT balance_at_start FROM wallet_month_data ' \
                            'WHERE month = $MONTH AND year = $YEAR) AS balance_at_start, ' \
                            '(SELECT sum(incoming) FROM wallet_data ' \
                            'WHERE month = $MONTH AND year = $YEAR) AS incoming, ' \
                            '(SELECT sum(expense) FROM wallet_data WHERE month = $MONTH AND year = $YEAR) AS expense, '\
                            '(SELECT sum(saving) FROM wallet_data) AS saving, ' \
                            '(SELECT sum(loan) FROM wallet_data) AS loan, ' \
                            '(SELECT sum(debt) FROM wallet_data) AS debt ' \
                            'FROM (SELECT 1);'
        wallet_data_query = wallet_data_query.replace('$MONTH', str(QDate.currentDate().month()))
        wallet_data_query = wallet_data_query.replace('$YEAR', str(QDate.currentDate().year()))
        if not query.exec(wallet_data_query):
            raise WalletModelException('Could not execute query \'%s\'', wallet_data_query)
        elif query.next():
            record = query.record()
            wallet_data.balance_at_start = convert_to_float(query, record, 'balance_at_start')
            wallet_data.incoming = convert_to_float(query, record, 'incoming')
            wallet_data.expense = convert_to_float(query, record, 'expense')
            wallet_data.savings = convert_to_float(query, record, 'saving')
            wallet_data.loan = convert_to_float(query, record, 'loan')
            wallet_data.debt = convert_to_float(query, record, 'debt')
        return wallet_data

    def create_new_wallet(self, wallet_path):
        self.__wallet = wallet_path
        # Устанавливаем новое имя базы данных
        self.__db.setDatabaseName(self.__wallet)
        if not self.__db.open():
            raise WalletModelException(QCoreApplication.translate('WalletModel',
                                                                  'Can\'t connect to wallet %s') % self.__wallet)
        else:
            # Создаем таблицы

            create_query = ['DROP TABLE IF EXISTS wallet_data;',
                            'DROP TABLE IF EXISTS wallet_month_data;',
                            'CREATE TABLE IF NOT EXISTS wallet_data(ID INTEGER PRIMARY KEY,'
                                                                   'day INTEGER,'
                                                                   'month INTEGER,'
                                                                   'year INTEGER,'
                                                                   'incoming REAL,'
                                                                   'expense REAL,'
                                                                   'saving REAL,'
                                                                   'loan REAL,'
                                                                   'debt REAL,'
                                                                   'description TEXT);',
                            'CREATE TABLE IF NOT EXISTS wallet_month_data(ID INTEGER PRIMARY KEY,'
                                                                         'month INTEGER,'
                                                                         'year INTEGER,'
                                                                         'balance_at_start REAL,'
                                                                         'balance_at_end REAL);'
                            ]
            query = QSqlQuery()
            for cq in create_query:
                if not query.exec(cq):
                    raise WalletModelException('Could not initialize database \'%s\' '
                                               'when execute query \'%s\'' % (self.__wallet, cq))
        self.read_wallet()

    def read_wallet(self):
        if self.__db is not None:
            if self.__db.isOpen():
                self.__db.close()
        self.__db.setDatabaseName(self.__wallet)
        if not self.__db.open():
            raise WalletModelException(QCoreApplication.translate('WalletModel',
                                                                  'Can\'t connect to wallet %s') % self.__wallet)
        self.setQuery(QSqlQuery(self.WALLET_SQL_QUERY % (QDate.currentDate().month(),
                                                         QDate.currentDate().year())))
