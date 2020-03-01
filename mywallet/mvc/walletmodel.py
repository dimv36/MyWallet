__author__ = 'dimv36'
import sqlite3
from PySide2.QtCore import Qt, QAbstractTableModel, QDate, QFileInfo, Signal, Slot
from PySide2.QtWidgets import QItemDelegate
from mywallet.enums import *


__all__ = ['WalletDateRange', 'WalletData', 'WalletModelException',
           'WalletModel', 'WalletItemDelegate']


class WalletDateRange:
    __WALLET_DATABASE_RANGE_FORMAT = 'date(\'{}\')'

    def __init__(self, start=None, end=None):
        now = QDate.currentDate()
        if start is None:
            default_date = QDate(now.year(), now.month(), 1)
            self.start = default_date
        else:
            self.start = start
        if end is None:
            self.end = now
        else:
            self.end = end

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__,
                                   self.start, self.end)

    def to_sqlite3_tuple(self):
        return WalletDateRange.to_sqlite3(self.start, self.end)

    @staticmethod
    def to_sqlite3(first, second):
        def convert(date):
            conv = date.toString(WalletModel.SQLITE_DATE_FORMAT)
            return conv

        return convert(first), convert(second)

    @staticmethod
    def from_sqlite3(first, second):
        def convert(str_date):
            return QDate.fromString(str_date, WalletModel.SQLITE_DATE_FORMAT)

        date_range = WalletDateRange(convert(first), convert(second))
        return date_range


class WalletData:
    def __init__(self):
        self.balance_at_start = float()
        self.balance_at_end = float()
        self.incoming = float()
        self.expense = float()
        self.savings = float()
        self.debt = float()
        self.date_range = WalletDateRange()

    def __repr__(self):
        return 'WalletData({}, {}, {}, {}, {}, {}) at {}'\
            .format(
                self.balance_at_start,
                self.balance_at_end,
                self.incoming,
                self.expense,
                self.savings,
                self.debt,
                self.date_range)

    @staticmethod
    def from_raw(items, date_range):
        result = WalletData()
        result.balance_at_start = items[WalletMetaDataType.INDEX_BALANCE_AT_START]
        result.balance_at_end = items[WalletMetaDataType.INDEX_BALANCE_AT_END]
        result.incoming = items[WalletMetaDataType.INDEX_INCOMING]
        result.expense = items[WalletMetaDataType.INDEX_EXPENSE]
        result.savings = items[WalletMetaDataType.INDEX_SAVINGS]
        result.debt = items[WalletMetaDataType.INDEX_DEBT]
        result.date_range = date_range
        return result


class WalletModelException(Exception):
    pass


class WalletModel(QAbstractTableModel):
    __HEADERS = {}
    _data_changed = Signal(WalletDateRange)
    wallet_metadata_changed = Signal([WalletData])
    DATE_VIEW_FORMAT = 'dd MMMM yyyy'
    SQLITE_DATE_FORMAT = 'yyyy-MM-dd'

    def __init__(self):
        super().__init__()
        self.__data = []
        self.__wallet_path = None
        self.__connection = None
        self.__init_headers()
        self.__init_signal_slots()

    def __init_headers(self):
        self.__HEADERS = {
            WalletModelColumns.INDEX_DATE: self.tr('Date'),
            WalletModelColumns.INDEX_INCOMING: self.tr('Incoming'),
            WalletModelColumns.INDEX_EXPENSE: self.tr('Expense'),
            WalletModelColumns.INDEX_SAVINGS: self.tr('Savings'),
            WalletModelColumns.INDEX_DEBT: self.tr('Debt'),
            WalletModelColumns.INDEX_DESCRIPTION: self.tr('Description')
        }

    def __init_signal_slots(self):
        # Инициализация сигналов и слотов
        self._data_changed.connect(self._on_update)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.__HEADERS)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.__HEADERS.get(section + 1, None)
            if not header:
                raise Warning('Unexpected section: {}'.format(section))
            return header
        elif orientation == Qt.Vertical:
            return section
        return None

    def data(self, index, role=None):
        if (not index.isValid() or
            len(self.__data) <= index.row() or
                not role == Qt.DisplayRole):
            return None
        return self.__data[index.row()][index.column() + 1]

    @Slot()
    def _on_update(self, date_range):
        self.wallet_metadata_changed.emit(self.metadata(date_range))

    @property
    def available_data_range(self):
        try:
            cursor = self.__connection.cursor()
            query = '''
                    SELECT min(date),
                           max(date)
                    FROM wallet_data;
                    '''
            cursor.execute(query)
            return WalletDateRange.from_sqlite3(*cursor.fetchall()[0])
        except sqlite3.Error as e:
            raise WalletModelException(e)

    def collect_items(self, date_range=WalletDateRange()):
        try:
            self.beginResetModel()
            cursor = self.__connection.cursor()
            date_range_query = WalletDateRange.to_sqlite3(date_range.start,
                                                          date_range.end)
            query = '''
                    SELECT id,
                           date,
                           CASE incoming IS NULL WHEN 0 THEN incoming ELSE '' END,
                           CASE expense  IS NULL WHEN 0 THEN expense  ELSE '' END,
                           CASE saving   IS NULL WHEN 0 THEN saving   ELSE '' END,
                           CASE debt     IS NULL WHEN 0 THEN debt     ELSE '' END,
                           description
                    FROM wallet_data
                    WHERE date BETWEEN ? AND ?
                    ORDER BY date;
                    '''
            cursor.execute(query, date_range_query)
            self.__data = cursor.fetchall()
            self.endResetModel()
        except sqlite3.Error as e:
            raise WalletModelException(e)
        # Отправляем сигнал на изменение данных
        self._data_changed.emit(date_range)

    def metadata_by_range(self, date_range):
        if not self.__connection:
            raise WalletModelException(self.tr('Database connection is not open'))
        try:
            cursor = self.__connection.cursor()
            query = '''
                    SELECT
                            (SELECT balance_at_start FROM wallet_month_data
                                  WHERE date BETWEEN ? AND ?),
                            (SELECT balance_at_end FROM wallet_month_data
                                  WHERE date BETWEEN ? AND ?),
                            (SELECT sum(incoming) FROM wallet_data
                                  WHERE date BETWEEN ? AND ?),
                            (SELECT sum(expense) FROM wallet_data
                                  WHERE date BETWEEN ? AND ?),
                            (SELECT sum(saving) FROM wallet_data
                                  WHERE date BETWEEN ? AND ?),
                            (SELECT sum(debt) FROM wallet_data
                                  WHERE date BETWEEN ? AND ?)
                    FROM (SELECT 1);
                    '''
            cursor.execute(query, date_range.to_sqlite3_tuple() * 6)
            metadata = cursor.fetchone()
            metadata = tuple(float(e) if e else float() for e in metadata)
            result = WalletData.from_raw(metadata, date_range)
        except sqlite3.Error as e:
            raise WalletModelException(self.tr('Could not get metadata: {}').format(e))
        return result

    def metadata(self, date_range=WalletDateRange()):
        if not self.__connection:
            raise WalletModelException(self.tr('Database connection is not open'))
        cursor = self.__connection.cursor()
        query = '''
                SELECT
                        (SELECT balance_at_start FROM wallet_month_data
                              WHERE date BETWEEN date('now', 'start of month') AND date('now')),
                        (SELECT balance_at_end FROM wallet_month_data
                              WHERE date BETWEEN date('now', 'start of month') AND date('now')),
                        (SELECT sum(incoming) FROM wallet_data
                              WHERE date BETWEEN date('now', 'start of month') AND date('now')),
                        (SELECT sum(expense) FROM wallet_data
                              WHERE date BETWEEN date('now', 'start of month') AND date('now')),
                        (SELECT sum(saving) FROM wallet_data
                              WHERE date BETWEEN ? AND date('now')),
                        (SELECT sum(debt) FROM wallet_data
                              WHERE date BETWEEN ? AND date('now'))
                FROM (SELECT 1);
                '''
        # Проверяем наличие записи за текущий месяц
        check_query = '''
                      SELECT *
                      FROM wallet_month_data
                      WHERE date = date('now', 'start of month');
                      '''
        cursor.execute(check_query)
        if cursor.fetchone() is None:
            # Запись за последний месяц не найдена
            # Тогда добавляем запись в таблицу wallet_month_data на основе balance_at_end прошлого месяца
            # (если есть), иначе 0.0
            previous_month_balance_query = '''
                                           SELECT
                                                  (SELECT balance_at_end FROM wallet_month_data
                                                   WHERE date = date('now', 'start of month', '-1 month')),
                                                  (SELECT sum(saving) FROM wallet_data)
                                            FROM (SELECT 1);
                                           '''
            cursor.execute(previous_month_balance_query)
            row = cursor.fetchone()
            balance_at_end = float() if row[0] is None else row[0]
            savings = float() if row[1] is None else row[1]
            balance_at_start = balance_at_end - savings
            try:
                # Формируем новую запись в таблице wallet_month_data, указав в качестве баланса на начало месяца
                # данные на конец предыдущего месяца за вычетов накоплений, а в качестве остатка на конец месяца -
                # баланс на конец месяца
                insert_query = '''
                               INSERT INTO wallet_month_data
                               VALUES (NULL, date('now', 'start of month'), ?, ?);
                               '''
                cursor.execute(insert_query, (balance_at_start, balance_at_start + savings))
                self.__connection.commit()
            except sqlite3.Error as e:
                raise WalletModelException(self.tr('Failed to insert metadata: {}').format(e))
        # Получаем метаданные
        cursor.execute('SELECT date FROM wallet_data WHERE id = 1;')
        first_id_tuple = cursor.fetchone()
        query_items = ('\'{}\''.format(first_id_tuple[0])
                       if first_id_tuple else 'date(\'now\', \'start of month\')'
                       for i in range(2))
        try:
            cursor.execute(query, tuple(query_items))
            metadata = cursor.fetchone()
            metadata = tuple(float(e) if e else float() for e in metadata)
        except sqlite3.Error as e:
            raise WalletModelException(self.tr('Could not get metadata: {}').format(e))
        result = WalletData.from_raw(metadata, date_range)
        return result

    def open_wallet(self, path):
        if path and not path == self.__wallet_path:
            try:
                if self.__connection:
                    self.__connection.close()
                self.__connection = sqlite3.connect(path)
                self.__wallet_path = path
                self.collect_items()
            except Exception as e:
                raise WalletModelException(e)

    @staticmethod
    def create_new_wallet(wallet_path):
        """
        Создание нового бумажника
        :param wallet_path: str
        :return: None
        """
        try:
            target_dir = QFileInfo(wallet_path).absoluteDir()
            if not target_dir.exists():
                QDir().mkdir(target_dir.absolutePath())
            db = sqlite3.connect(wallet_path)
            cursor = db.cursor()
            init_query = '''
                DROP TABLE IF EXISTS wallet_data;
                DROP TABLE IF EXISTS wallgvnet_month_data;
                DROP TABLE IF EXISTS wallet_categories;
                CREATE TABLE wallet_data(
                    ID INTEGER PRIMARY KEY,
                    date TEXT,
                    incoming REAL,
                    expense REAL,
                    saving REAL,
                    debt REAL,
                    description TEXT
                );
                CREATE TABLE wallet_month_data(
                    ID INTEGER PRIMARY KEY,
                    date TEXT,
                    balance_at_start REAL,
                    balance_at_end REAL
                );
                CREATE TABLE wallet_categories(
                    ID INTEGER PRIMARY KEY,
                    wallet_item_type INTEGER,
                    description TEXT
                );
            '''
            cursor.executescript(init_query)
            db.commit()
            db.close()
        except sqlite3.Error as e:
            raise WalletModelException(self.tr('Failed to create wallet: {}').format(e))

    def _run_query(self, query, data):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, data)
        except sqlite3.Error as e:
            raise WalletModelException(self.tr('Execution \'{}\' failure: {}').format(query, e))
        else:
            self.__connection.commit()

    def _update_metadata(self, item, remove=False):
        current_metadata = self.metadata()
        multiple = 1 if not remove else -1
        if item[WalletModelColumns.INDEX_INCOMING]:
            current_metadata.balance_at_end += multiple * item[WalletModelColumns.INDEX_INCOMING]
        elif item[WalletModelColumns.INDEX_EXPENSE]:
            current_metadata.balance_at_end -= multiple * item[WalletModelColumns.INDEX_EXPENSE]
        # TODO: Savings?
        update_metadata_query = '''UPDATE wallet_month_data
                                   SET balance_at_end = ?
                                   WHERE date = date('now', 'start of month');
                                '''
        self._run_query(update_metadata_query, (current_metadata.balance_at_end,))

    def add_entry(self, item):
        """
        Добавить запись в бумажник
        :param item: dict
        :return: None
        """
        def to_sqlite3(row):
            items = []
            for i in range(WalletModelColumns.INDEX_DATE, WalletModelColumns.INDEX_DESCRIPTION + 1):
                value = row.get(i, None)
                if i == WalletModelColumns.INDEX_DATE:
                    value = value.toString(self.SQLITE_DATE_FORMAT)
                items.append(value)
            return tuple(i for i in items)

        try:
            query = 'INSERT INTO wallet_data VALUES(NULL, ?, ?, ?, ?, ?, ?);'
            self._run_query(query, to_sqlite3(item))
        except WalletModelException as e:
            raise WalletModelException(self.tr('Failed to insert item: {}').format(e))
        self._update_metadata(item)
        self.collect_items()

    def remove_entry(self, idx):
        """
        Удалить запись из бумажника
        :param item: dict
        :return: None
        """
        try:
            item = self.__data[idx]
            row_id, *unused = item
        except Exception as e:
            raise WalletModelException(self.tr('Failed to determine row ID: {}').format(e))
        try:
            query = 'DELETE FROM wallet_data WHERE id = ?;'
            self._run_query(query, (row_id,))
        except WalletModelException as e:
            raise WalletModelException(self.tr('Failed to remove item: {}').format(e))
        self._update_metadata(item, remove=True)
        self.collect_items()

    def change_balance_at_start_of_month(self, balance):
        """
        Изменить баланс на начало месяца текущего месяца
        :param balance: float
        :return: None
        """
        # Запись о балансе на начало месяца уже должна быть вставлена
        # в методе get_metadata, поэтому тут используется UPDATE запрос
        try:
            cursor = self.__connection.cursor()
            balance_at_start_query = '''UPDATE wallet_month_data
                                        SET balance_at_start = ?
                                        WHERE date = date('now', 'start of month');
                                     '''
            cursor.execute(balance_at_start_query, (balance,))
            # Одну таблицу обновили - теперь вторую
            # Определяем разницу, на сколько изменился баланс на начало месяца
            metadata = self.metadata()
            delta = balance - metadata.balance_at_start
            # Устанавливаем баланс на начало месяца в новое значение,
            # а баланс на конец месяца - с добавлением расчитанной разницы
            metadata.balance_at_start = balance
            metadata.balance_at_end += delta
            # Обновляем баланс на конец месяца
            balance_at_end_query = '''UPDATE wallet_month_data
                                      SET balance_at_end = ?
                                      WHERE date = date('now', 'start of month');
                                   '''
            cursor.execute(balance_at_end_query, (metadata.balance_at_end,))
        except sqlite3.Error as e:
            raise WalletModelException(self.tr('Failed to update balance at start of month: {}').format(e))
        else:
            self.__connection.commit()
            self._data_changed.emit(WalletDateRange())

    # Следующие методы используются при построении статистики в классе StatisticDialog
    def get_statistic_items(self):
        """
        Получить периоды отображения статистики
        :return: dict {year: {month: WalletData}}
        """
        try:
            return self.__db.get_statistic_items()
        except WalletDatabaseException as e:
            raise WalletModelException(e)


class WalletItemDelegate(QItemDelegate):
    import re
    _DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
    _FLOAT_RE = re.compile(r'\d+[.\d]?')

    def drawDisplay(self, painter, option, rect, text):
        if self._DATE_RE.match(text):
            date = QDate.fromString(text, WalletModel.SQLITE_DATE_FORMAT)
            displayed = date.toString(WalletModel.DATE_VIEW_FORMAT)
        elif self._FLOAT_RE.match(text):
            value = float(text)
            displayed = '{0:.2f}'.format(value)
        else:
            displayed = text
        super(WalletItemDelegate, self).drawDisplay(painter, option, rect, displayed)
