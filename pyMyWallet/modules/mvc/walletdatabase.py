__author__ = 'dimv36'
from PyQt5.QtCore import QDate, QFileInfo, QObject, pyqtSignal, pyqtSlot
import sqlite3
from modules import *
from modules.enums import *


class WalletData:
    def __init__(self):
        self.balance_at_start = float()
        self.balance_at_end = float()
        self.incoming = float()
        self.expense = float()
        self.savings = float()
        self.debt = float()


class WalletDatabaseException(Exception):
    pass


class WalletDatabase(QObject):
    __signal_data_changed = pyqtSignal(dict, bool)

    class WalletDatabaseConvertor:
        WALLET_DATE_DB_FORMAT = 'yyyy-MM-dd'
        WALLET_DATE_VIEW_FORMAT = 'dd MMMM yyyy'

        @staticmethod
        def convert_from_database(row):
            results = {}
            for column in range(0, len(row)):
                element = row[column]
                if column == WalletItemModelType.INDEX_DATE.value:
                    date = QDate.fromString(element, WalletDatabase.WalletDatabaseConvertor.WALLET_DATE_DB_FORMAT)
                    data = date.toString(WalletDatabase.WalletDatabaseConvertor.WALLET_DATE_VIEW_FORMAT)
                elif column == WalletItemModelType.INDEX_DESCRIPTION.value:
                    data = element
                elif (column == WalletItemModelType.INDEX_INCOMING.value or
                      column == WalletItemModelType.INDEX_EXPENSE.value or
                      column == WalletItemModelType.INDEX_SAVINGS.value or
                      column == WalletItemModelType.INDEX_DEBT.value):
                    data = str() if element is None else STR_FLOAT_FORMAT % element
                else:
                    raise Warning('Unexpected Column type: %d' % column)
                results[column] = data
            return tuple(results[e] for e in results)

        @staticmethod
        def convert_to_database(item):
            elements = {}
            for column in range(0, max(item.keys()) + 1):
                data = 'NULL'
                element = item.get(column, 'NULL')
                if column == WalletItemModelType.INDEX_DATE.value and element:
                    if isinstance(element, QDate):
                        data = '\'%s\'' % element.toString(WalletDatabase.WalletDatabaseConvertor.WALLET_DATE_DB_FORMAT)
                    elif isinstance(element, str):
                        date = QDate.fromString(element, WalletDatabase.WalletDatabaseConvertor.WALLET_DATE_VIEW_FORMAT)
                        data = '\'%s\'' % date.toString(WalletDatabase.WalletDatabaseConvertor.WALLET_DATE_DB_FORMAT)
                elif column == WalletItemModelType.INDEX_DESCRIPTION.value and element:
                    data = '\'%s\'' % element
                elif (column == WalletItemModelType.INDEX_INCOMING.value or
                      column == WalletItemModelType.INDEX_EXPENSE.value or
                      column == WalletItemModelType.INDEX_SAVINGS.value or
                      column == WalletItemModelType.INDEX_DEBT.value) and element:
                    data = '%s' % element
                elements[column] = data
            # Обработка исключительных ситуаций
            value = item.get(WalletItemModelType.INDEX_SAVINGS.value, None)
            if value:
                elements[WalletItemModelType.INDEX_INCOMING.value] = str(-1 * float(value))
            value = item.get(WalletItemModelType.INDEX_DEBT.value, None)
            if value:
                elements[WalletItemModelType.INDEX_INCOMING.value] = str(value)
            return elements

    __WALLET_GET_DATA_QUERY_TEMPLATE = 'SELECT date, ' \
                                       '   incoming, expense, saving, ' \
                                       '   debt, description FROM wallet_data ' \
                                       'WHERE date BETWEEN $START AND $END ORDER BY date;'
    __WALLET_GET_INSERTED_DATA_QUERY = 'SELECT date, ' \
                                       '    incoming, expense, saving, ' \
                                       '    debt, description ' \
                                       'FROM wallet_data ORDER BY id DESC LIMIT 1;'
    __WALLET_GET_REMOVABLE_DATA_QUERY_TEMPLATE = 'SELECT * ' \
                                                 ' FROM wallet_data ' \
                                                 ' WHERE %s LIMIT 1;'
    __WALLET_REMOVE_DATA_QUERY_TEMPLATE = 'DELETE FROM wallet_data WHERE id = %d;'
    __WALLET_INSERT_DATA_QUERY_TEMPLATE = 'INSERT INTO wallet_data VALUES(%s);'
    __WALLET_INIT_WALLET_QUERY = ['DROP TABLE IF EXISTS wallet_data;',
                                  'DROP TABLE IF EXISTS wallet_month_data;',
                                  'DROP TABLE IF EXISTS wallet_categories;',
                                  'CREATE TABLE wallet_data'
                                  '   (ID INTEGER PRIMARY KEY, '
                                  '     date TEXT, '
                                  '     incoming REAL, '
                                  '     expense REAL, '
                                  '     saving REAL, '
                                  '     debt REAL, '
                                  '     description TEXT); ',
                                  'CREATE TABLE wallet_month_data'
                                  '   (ID INTEGER PRIMARY KEY, '
                                  '    date TEXT,'
                                  '    balance_at_start REAL, '
                                  '    balance_at_end REAL);',
                                  'CREATE TABLE wallet_categories'
                                  '   (ID INTEGER PRIMARY KEY, '
                                  '    wallet_item_type INTEGER, '
                                  '    description TEXT);'
                                  ]
    __WALLET_UPDATE_BALANCE_AT_END_QUERY_TEMPLATE = 'UPDATE wallet_month_data ' \
                                                    '    SET balance_at_end = balance_at_end + \'%f\' ' \
                                                    'WHERE date = date(\'now\', \'start of month\');'
    __WALLET_GET_FIRST_DATE_QUERY = 'SELECT date FROM wallet_data WHERE id = 1;'
    __WALLET_GET_METADATA_ROW_ON_CURRENT_MONTH_QUERY = 'SELECT * FROM wallet_month_data ' \
                                                       'WHERE date = date(\'now\', \'start of month\');'
    __WALLET_INSERT_METADATA_QUERY_TEMPLATE = 'INSERT INTO wallet_month_data VALUES ' \
                                              '    (NULL, date(\'now\', \'start of month\'), %f, 0.0);'
    __WALLET_UPDATE_METADATA_BALANCE_AT_START_QUERY_TEMPLATE = 'UPDATE wallet_month_data ' \
                                                               'SET balance_at_start = \'%f\'' \
                                                               'WHERE date = date(\'now\', \'start of month\');'
    __WALLET_GET_WALLET_METADATA_QUERY_TEMPLATE = 'SELECT ' \
                                                  ' (SELECT balance_at_start FROM wallet_month_data ' \
                                                  '     WHERE date BETWEEN $START AND $END), ' \
                                                  ' (SELECT balance_at_end FROM wallet_month_data ' \
                                                  '     WHERE date BETWEEN $START AND $END), ' \
                                                  ' (SELECT sum(incoming) FROM wallet_data ' \
                                                  '     WHERE date BETWEEN $START AND $END), ' \
                                                  ' (SELECT sum(expense) FROM wallet_data ' \
                                                  '     WHERE date BETWEEN $START AND $END), ' \
                                                  ' (SELECT sum(saving) FROM wallet_data ' \
                                                  '     WHERE date BETWEEN $EARLY AND $END), ' \
                                                  ' (SELECT sum(debt) FROM wallet_data ' \
                                                  '     WHERE date BETWEEN $EARLY AND $END) ' \
                                                  'FROM (SELECT 1);'
    __WALLET_GET_BALANCE_AT_END_OF_PREVIOUS_MONTH_QUERY = 'SELECT balance_at_end FROM wallet_month_data WHERE ' \
                                                          'date = date(\'now\', \'start of month\', \'-1 month\');'

    __WALLET_DATA_COLUMNS = {
        WalletItemModelType.INDEX_DATE.value: 'date',
        WalletItemModelType.INDEX_INCOMING.value: 'incoming',
        WalletItemModelType.INDEX_EXPENSE.value: 'expense',
        WalletItemModelType.INDEX_SAVINGS.value: 'saving',
        WalletItemModelType.INDEX_DEBT.value: 'debt',
        WalletItemModelType.INDEX_DESCRIPTION.value: 'description'
    }

    def __init__(self):
        super().__init__()
        self.__database = None
        self.__connection = None
        self.__data_range = None
        self.__metadata = None
        self.__signal_data_changed.connect(self.__on_update_balance_at_end)

    def __del__(self):
        if getattr(self, '_WalletDatabase__connection', None):
            self.disconnect()

    @pyqtSlot(dict, bool)
    def __on_update_balance_at_end(self, item, is_remove):
        print('__on_update_balance_at_end: %s' % item)
        convertor = lambda elem: float(elem) if not elem == 'NULL' else float()
        data = {}
        for i in range(WalletItemModelType.INDEX_INCOMING.value,
                       WalletItemModelType.INDEX_DESCRIPTION.value):
            data[i] = -1 * convertor(item[i]) if i == WalletItemModelType.INDEX_EXPENSE.value else convertor(item[i])
        delta = sum(elem for elem in data.values()) - data.get(WalletItemModelType.INDEX_DEBT.value)
        delta *= -1 if is_remove else 1
        query = self.__WALLET_UPDATE_BALANCE_AT_END_QUERY_TEMPLATE % delta
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query)
            self.__connection.commit()
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalletDatabase', 'Failed to update balance at end: %s' % e))
        if is_remove:
            self.__metadata.incoming -= data.get(WalletItemModelType.INDEX_INCOMING.value)
            self.__metadata.expense -= data.get(WalletItemModelType.INDEX_EXPENSE.value)
            self.__metadata.savings -= data.get(WalletItemModelType.INDEX_SAVINGS.value)
            self.__metadata.debt -= data.get(WalletItemModelType.INDEX_DEBT.value)
        else:
            self.__metadata.incoming += data.get(WalletItemModelType.INDEX_INCOMING.value)
            self.__metadata.expense += data.get(WalletItemModelType.INDEX_EXPENSE.value)
            self.__metadata.savings += data.get(WalletItemModelType.INDEX_SAVINGS.value)
            self.__metadata.debt += data.get(WalletItemModelType.INDEX_DEBT.value)
        self.__metadata.balance_at_end += delta

    def connect(self, database):
        if not database:
            raise WalletDatabaseException(tr('WalletDatabase', 'Could not connect to database: database path is empty'))
        if not QFileInfo(database).exists() and database:
            raise WalletDatabaseException(tr('WalletDatabase', 'Wallet \'%s\' does not exists' % database))
        if self.__connection:
            self.__connection.close()
        self.__database = database
        self.__connection = sqlite3.connect(database)

    def connection_path(self):
        return self.__database if self.__database is not None else None

    def disconnect(self):
        if self.__connection:
            self.__connection.close()

    @staticmethod
    def create_wallet(database):
        db = sqlite3.connect(database)
        cursor = db.cursor()
        try:
            for cq in WalletDatabase.__WALLET_INIT_WALLET_QUERY:
                cursor.execute(cq)
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalletDatabase', 'Failed to create wallet: %s' % e))
        db.commit()
        db.close()

    def get_data(self, data_range=None):
        # TODO: сделать реализацию получения данных по диапазону дат
        if not self.__connection:
            raise WalletDatabaseException(tr('WalletDatabase', 'Database connection is not open'))
        query = None
        if not data_range:
            query = self.__WALLET_GET_DATA_QUERY_TEMPLATE
            query = query.replace('$START', 'date(\'now\', \'start of month\')')
            query = query.replace('$END', 'date(\'now\')')
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalletDatabase', 'Could not get data: %s' % e))
        data = [self.WalletDatabaseConvertor.convert_from_database(row) for row in data]
        return data

    def get_metadata(self, data_range=None):
        if self.__data_range == data_range and self.__metadata:
            return self.__metadata
        # TODO: сделать реализацию получения данных по диапазону дат
        if not self.__connection:
            raise WalletDatabaseException(tr('WalletDatabase', 'Database connection is not open'))
        query = None
        cursor = self.__connection.cursor()
        if not data_range:
            # Проверяем наличие записи за текущий месяц
            cursor.execute(self.__WALLET_GET_METADATA_ROW_ON_CURRENT_MONTH_QUERY)
            if cursor.fetchone() is None:
                # Запись за последний месяц не найдена
                # Тогда добавляем запись в таблицу wallet_month_data на основе balance_at_end прошлого месяца
                # (если есть), иначе 0.0
                cursor.execute(self.__WALLET_GET_BALANCE_AT_END_OF_PREVIOUS_MONTH_QUERY)
                balance_at_end = float() if cursor.fetchone() is None else cursor.fetchone()
                try:
                    query = self.__WALLET_INSERT_METADATA_QUERY_TEMPLATE % balance_at_end
                    cursor.execute(query)
                    self.__connection.commit()
                except sqlite3.Error as e:
                    raise WalletDatabaseException(tr('WalletDatabase', 'Failed to insert metadata: %s' % e))
            # Получаем метаданные
            query = self.__WALLET_GET_WALLET_METADATA_QUERY_TEMPLATE
            cursor.execute(self.__WALLET_GET_FIRST_DATE_QUERY)
            first_id_tuple = cursor.fetchone()
            query = query.replace('$START', 'date(\'now\', \'start of month\')')
            query = query.replace('$END', 'date(\'now\')')
            query = query.replace('$EARLY', ('\'%s\'' % first_id_tuple[0]
                                             if first_id_tuple
                                             else 'date(\'now\', \'start of month\')'))
        try:
            cursor.execute(query)
            metadata = cursor.fetchone()
            metadata = tuple(float(e) if e else float() for e in metadata)
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalledDatabase', 'Could not get metadata: %s' % e))
        result = WalletData()
        result.balance_at_start = metadata[WalletMetaDataType.INDEX_BALANCE_AT_START.value]
        result.balance_at_end = metadata[WalletMetaDataType.INDEX_BALANCE_AT_END.value]
        result.incoming = metadata[WalletMetaDataType.INDEX_INCOMING.value]
        result.expense = metadata[WalletMetaDataType.INDEX_EXPENSE.value]
        result.savings = metadata[WalletMetaDataType.INDEX_SAVINGS.value]
        result.debt = metadata[WalletMetaDataType.INDEX_DEBT.value]
        self.__data_range = data_range
        self.__metadata = result
        return result

    def add_data(self, item):
        values = self.WalletDatabaseConvertor.convert_to_database(item)
        data = ', '.join([str(values[e]) for e in values])
        data = 'NULL, %s' % data
        insert_query = self.__WALLET_INSERT_DATA_QUERY_TEMPLATE % data
        cursor = self.__connection.cursor()
        try:
            cursor.execute(insert_query)
            self.__connection.commit()
            cursor.execute(self.__WALLET_GET_INSERTED_DATA_QUERY)
            row = cursor.fetchone()
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalletDatabase', 'Could not insert data: %s' % e))
        self.__signal_data_changed.emit(values, False)
        return self.WalletDatabaseConvertor.convert_from_database(row)

    def remove_data(self, item):
        values = self.WalletDatabaseConvertor.convert_to_database(item)
        key_values = {}
        for i in range(0, len(values)):
            column = self.__WALLET_DATA_COLUMNS[i]
            value = values[i]
            separator = 'IS' if value == 'NULL' else '='
            key_values[i] = '%s %s %s' % (column, separator, value)
        where_clause = ' AND '.join(key_values.values())
        query = self.__WALLET_GET_REMOVABLE_DATA_QUERY_TEMPLATE % where_clause
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            if not row:
                raise WalletDatabaseException(tr('WalletDatabase', 'Could not get removable data: is database broken?'))
            row_id = row[0]
            removed = self.WalletDatabaseConvertor.convert_from_database(row[1:])
            # Удаляем данные
            query = self.__WALLET_REMOVE_DATA_QUERY_TEMPLATE % row_id
            cursor.execute(query)
            self.__connection.commit()
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalletDatabase', 'Could not remove data: %s' % e))
        self.__signal_data_changed.emit(values, True)
        return removed

    def change_balance_at_start_of_month(self, balance):
        # Запись о балансе на начало месяца уже должна быть вставлена
        # в методе get_metadata, поэтому тут используется UPDATE запрос
        cursor = self.__connection.cursor()
        try:
            query = self.__WALLET_UPDATE_METADATA_BALANCE_AT_START_QUERY_TEMPLATE % balance
            cursor.execute(query)
            self.__connection.commit()
        except sqlite3.Error as e:
            raise WalletDatabaseException(tr('WalletDatabase', 'Could not update balance at start of month: %s' % e))
        # Определяем разницу, на сколько изменился баланс на начало месяца
        delta = balance - self.__metadata.balance_at_start
        # Устанавливаем баланс на начало месяца в новое значение,
        # а баланс на конец месяца - с добавлением расчитанной разницы
        self.__metadata.balance_at_start = balance
        self.__metadata.balance_at_end += delta