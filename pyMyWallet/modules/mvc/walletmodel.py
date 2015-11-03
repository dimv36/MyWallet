from PyQt5.QtCore import QCoreApplication, Qt, QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from modules.enums import WalletItemModelType, WalletItemType


class WalletModelException(Exception):
    pass


class WalletModel(QSqlQueryModel):
    __WALLET_SELECT_SQL_QUERY = 'SELECT day, month, year, ' \
                                'incoming, expense, saving, ' \
                                'loan, debt, description FROM wallet_data ' \
                                'WHERE month = %d AND year = %d ORDER BY day;'

    class WalletData:
        def __init__(self):
            self.balance_at_start = float()
            self.balance_at_end = float()
            self.incoming = float()
            self.expense = float()
            self.savings = float()
            self.loan = float()
            self.debt = float()

    def __init__(self, wallet_file_path):
        super().__init__()
        self.__wallet = wallet_file_path
        self.__db = None
        self.read_wallet()

    def __set_headers(self):
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
        self.setHeaderData(WalletItemModelType.INDEX_DESCRIPTION.value,
                           Qt.Horizontal,
                           QCoreApplication.translate('WalletModel', 'Description'))

    def __close_db(self):
        """
        Метод закрытия базы данных (бумажника)
        :return: None
        """
        QSqlDatabase.removeDatabase(self.__wallet)

    def __connect_to_db(self, name):
        """
        Подключение к базе данных (бумажнику)
        :param name: str
        :return: None
        """
        if QSqlDatabase.contains():
            self.__db = QSqlDatabase.database()
        else:
            self.__db = QSqlDatabase.addDatabase('QSQLITE')
        self.__db.setDatabaseName(name)
        if not self.__db.open():
            raise WalletModelException(QCoreApplication.translate('WalletModel',
                                                                  'Can not open database: %s') %
                                       self.__db.lastError().text())

    def __set_query(self, date=None):
        """
        Устанавливает поисковый запрос для отображения данных
        :param date: QDate
        :return:
        """
        if not date:
            date = QDate.currentDate()
        self.clear()
        self.setQuery(QSqlQuery(self.__WALLET_SELECT_SQL_QUERY % (date.month(), date.year())))
        self.__set_headers()

    def __update_balance_at_end(self, date):
        """
        Обновить остаток на начало месяца
        Этот метод должен быть вызван во всех методах, где производится модификация данных кошелька
        :param date: QDate
        :return:
        """
        wallet_info = self.get_wallet_info(date)
        balance_at_end = wallet_info.balance_at_start + wallet_info.incoming - wallet_info.expense + wallet_info.savings
        sql = 'UPDATE wallet_month_data SET balance_at_end = %f WHERE month = %d AND year = %d;' % (balance_at_end,
                                                                                                    date.month(),
                                                                                                    date.year())
        query = QSqlQuery()
        if not query.exec(sql):
            raise WalletModelException('Could not set balance at end by query \'%s\'' % query)

    def get_wallet_info(self, date=None):
        """
        Получить данные по доходам/расходам/накоплениям/долгам/займам за период времени
        :param date: QDate
        :return: None
        """
        def convert_to_float(_query, _record, _field):
            result = float()
            try:
                result = float(_query.value(_record.indexOf(_field)))
            except ValueError:
                pass
            return result

        if not date:
            date = QDate.currentDate()
        wallet_data = self.WalletData()
        query = QSqlQuery()
        wallet_data_query = 'SELECT ' \
                            '(SELECT balance_at_start FROM wallet_month_data ' \
                            'WHERE month = $MONTH AND year = $YEAR) AS balance_at_start, ' \
                            '(SELECT balance_at_end FROM wallet_month_data ' \
                            'WHERE month = $MONTH AND year = $YEAR) AS balance_at_end, ' \
                            '(SELECT sum(incoming) FROM wallet_data ' \
                            'WHERE month = $MONTH AND year = $YEAR) AS incoming, ' \
                            '(SELECT sum(expense) FROM wallet_data WHERE month = $MONTH AND year = $YEAR) AS expense, '\
                            '(SELECT sum(saving) FROM wallet_data WHERE month <= $MONTH AND year <= $YEAR) AS saving, '\
                            '(SELECT sum(loan) FROM wallet_data WHERE month <= $MONTH AND year <= $YEAR) AS loan, ' \
                            '(SELECT sum(debt) FROM wallet_data WHERE month <= $MONTH AND year <= $YEAR) AS debt ' \
                            'FROM (SELECT 1);'
        wallet_data_query = wallet_data_query.replace('$MONTH', str(date.month()))
        wallet_data_query = wallet_data_query.replace('$YEAR', str(date.year()))
        if not query.exec(wallet_data_query):
            raise WalletModelException('Could not execute query \'%s\': %s' % (wallet_data_query,
                                                                               self.__db.lastError().text()))
        elif query.next():
            record = query.record()
            wallet_data.balance_at_start = convert_to_float(query, record, 'balance_at_start')
            if not wallet_data.balance_at_start:
                # Пытаемся получить баланс на начало месяца на основе данных предыдущего
                sql = 'SELECT ' \
                      '(SELECT sum(saving) FROM wallet_data WHERE month <= $MONTH AND year <= $YEAR) AS saving, '\
                      '(SELECT balance_at_end FROM wallet_month_data WHERE month = $MONTH - 1 AND YEAR = $YEAR) ' \
                      'AS balance_at_end '\
                      'FROM (SELECT 1);'
                sql = sql.replace('$MONTH', str(date.month())).replace('$YEAR', str(date.year()))
                if not query.exec(sql):
                    raise WalletModelException('Could not execute query \'%s\': %s' % (sql,
                                                                                       self.__db.lastError().text()))
                elif query.next():
                    query_record = query.record()
                    wallet_data.balance_at_start = convert_to_float(query, query_record, 'balance_at_end') - \
                                                   convert_to_float(query, query_record, 'saving')
                    self.change_current_month_balance(wallet_data.balance_at_start)
            wallet_data.balance_at_end = convert_to_float(query, record, 'balance_at_end')
            wallet_data.incoming = convert_to_float(query, record, 'incoming')
            wallet_data.expense = convert_to_float(query, record, 'expense')
            wallet_data.savings = convert_to_float(query, record, 'saving')
            wallet_data.loan = convert_to_float(query, record, 'loan')
            wallet_data.debt = convert_to_float(query, record, 'debt')
        return wallet_data

    def create_new_wallet(self, wallet_path):
        """
        Создание нового бумажника
        :param wallet_path: str
        :return: None
        """
        self.__wallet = wallet_path
        # Устанавливаем новое имя базы данных
        self.__connect_to_db(wallet_path)
        # Создаем таблицы
        create_query = ['DROP TABLE IF EXISTS wallet_data;',
                        'DROP TABLE IF EXISTS wallet_month_data;',
                        'CREATE TABLE IF NOT EXISTS wallet_data(ID INTEGER PRIMARY KEY, '
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
                raise WalletModelException(QCoreApplication.translate('WalletModel',
                                                                      'Could not initialize database \'%s\''
                                                                      'when execute query \'%s\': %s') %
                                                                      (self.__wallet,
                                                                       cq,
                                                                       self.__db.lastError().text()))
        self.__set_query()

    def read_wallet(self, wallet=None):
        """
        Чтение бумажника
        :param wallet: имя (путь) к бумажнику str
        :return: None
        """
        self.__close_db()
        if wallet:
            self.__wallet = wallet
        self.beginResetModel()
        self.clear()
        self.__connect_to_db(self.__wallet)
        self.endResetModel()
        self.__set_query()

    def add_entry(self, date, item, wallet_type):
        """
        Добавить запись в бумажник
        :param date: QDate
        :param item: list
        :param wallet_type: enum.WalletItemType
        :return: None
        """
        self.beginResetModel()
        values = 'NULL, %d, %d, %d,' % (date.day(), date.month(), date.year())
        if wallet_type == WalletItemType.INCOMING:
            values += ' %s, NULL, NULL, NULL, NULL, \'%s\'' % (item[0], item[1])
        elif wallet_type == WalletItemType.EXPENSE:
            values += ' NULL, %s, NULL, NULL, NULL, \'%s\'' % (item[0], item[1])
        elif wallet_type == WalletItemType.SAVING:
            values += ' %s, NULL, %s, NULL, NULL, \'%s\'' % (-1 * float(item[0]), item[0], item[1])
        elif wallet_type == WalletItemType.LOAN:
            values += ' NULL, NULL, NULL, %s, NULL, \'%s\'' % (item[0], item[1])
        elif wallet_type == WalletItemType.DEBT:
            values += ' %s, NULL, NULL, NULL, %s, \'%s\'' % (item[0], item[0], item[1])
        else:
            raise WalletModelException('Unexpected type: %s' % wallet_type)
        insert_query = 'INSERT INTO wallet_data VALUES(%s);' % values
        query = QSqlQuery()
        if not query.exec(insert_query):
            raise WalletModelException('Could not insert data: \'%s\': %s' % (insert_query,
                                                                              self.__db.lastError().text()))
        self.__update_balance_at_end(date)
        self.endResetModel()
        self.__set_query()

    def remove_entry(self, date, item, wallet_type):
        """
        Удалить запись из бумажника
        :param date: QDate
        :param item: list
        :param wallet_type: enum.WalletItemType
        :return: None
        """
        self.beginResetModel()
        sql = 'SELECT id FROM wallet_data WHERE day = %d AND month = %d AND year = %d AND '
        if wallet_type == WalletItemType.INCOMING:
            sql += 'incoming = %f'
        elif wallet_type == WalletItemType.EXPENSE:
            sql += 'expense = %f'
        elif wallet_type == WalletItemType.SAVING:
            sql += 'saving = %f'
        elif wallet_type == WalletItemType.LOAN:
            sql += 'loan = %f'
        elif wallet_type == WalletItemType.DEBT:
            sql += 'debt = %f AND incoming = %f'
        else:
            raise WalletModelException('Unexpected type: %s', wallet_type)
        sql += ' AND description = \'%s\' LIMIT 1;'
        query = QSqlQuery()
        if wallet_type == WalletItemType.DEBT:
            sql = sql % (date.day(),
                         date.month(),
                         date.year(),
                         item[0],
                         item[1],
                         item[2])
        else:
            sql = sql % (date.day(),
                         date.month(),
                         date.year(),
                         item[-2],
                         item[-1])
        if not query.exec(sql):
            raise WalletModelException('Could not execute query: \'%s\': %s' % (sql,
                                                                                self.__db.lastError().text()))
        elif query.next():
            record = query.record()
            record_id = int(record.value(record.indexOf('id')))
            sql = 'DELETE FROM wallet_data WHERE id = %d' % record_id
            if not query.exec(sql):
                raise WalletModelException('Could not delete item by query: \'%s\': %s' % (sql,
                                                                                           self.__db.lastError().text()
                                                                                           ))
        self.__update_balance_at_end(date)
        self.endResetModel()
        self.__set_query()

    def change_current_month_balance(self, balance):
        """
        Изменить баланс на начало месяца текущего месяца
        :param balance: float
        :return: None
        """
        self.beginResetModel()
        current_date = QDate.currentDate()
        query = QSqlQuery()
        sql = 'SELECT 1 AS count FROM wallet_month_data WHERE month = %d AND year = %d;' % (current_date.month(),
                                                                                            current_date.year())
        if not query.exec(sql):
            raise WalletModelException('Could not execute query \'%s\': %s' % (sql,
                                                                               self.__db.lastError().text()))
        elif not query.next():
            sql = 'INSERT INTO wallet_month_data VALUES (NULL, %d, %d, %f, NULL);' % (
                current_date.month(),
                current_date.year(),
                balance
            )
        else:
            sql = 'UPDATE wallet_month_data SET balance_at_start = %f WHERE month = %d AND year = %d;' % (
                balance,
                current_date.month(),
                current_date.year()
            )
        if not query.exec(sql):
            raise WalletModelException('Could not update balance by query \'%s\': %s' % (sql,
                                                                                         self.__db.lastError().text()))
        self.__update_balance_at_end(current_date)
        self.endResetModel()

    # Следующие методы используются при построении статистики в классе StatisticDialog
    def get_statistic_periods_items(self):
        """
        Получить периоды отображения статистики
        :return: dict {year: [months}
        """
        year_query = QSqlQuery()
        statistic_items = {}
        year_sql = 'SELECT DISTINCT year AS year FROM wallet_data;'
        if not year_query.exec(year_sql):
            raise WalletModelException('Could not get years items by query \'%s\': %s' % (
                year_sql, self.__db.lastError().text())
            )
        while year_query.next():
            year_record = year_query.record()
            year = int(year_record.value(year_record.indexOf('year')))
            months = []
            month_query = QSqlQuery()
            month_sql = 'SELECT DISTINCT month AS month FROM wallet_data WHERE year = %d' % year
            if not month_query.exec(month_sql):
                raise WalletModelException('Could not get months items by query \'%s\': %s' % (
                    month_sql,
                    self.__db.lastError().text()))
            while month_query.next():
                month_record = month_query.record()
                month = int(month_record.value(month_record.indexOf('month')))
                months.append(month)
            statistic_items[year] = months
        return statistic_items
