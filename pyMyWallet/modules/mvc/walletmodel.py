__author__ = 'dimv36'
from PyQt5.QtCore import QCoreApplication, QAbstractTableModel, Qt, QDate, QObject, pyqtSignal, pyqtSlot
from lxml import etree

from modules.mvc.walletitem import WalletRow, WalletItem
from modules.enums import WalletItemModelType, WalletItemType


class WalletModelException(Exception):
    pass


class WalletModel(QAbstractTableModel):
    DATE_FORMAT = 'dd.MM.yyyy'

    class Communicate(QObject):
        signal_model_was_changed = pyqtSignal()

    class WalletData:
        def __init__(self):
            self.incoming = float()
            self.expense = float()
            self.loan = float()
            self.debt = float()
            self.balance = float()

    def __init__(self, wallet_file_path):
        super().__init__()
        tr = QCoreApplication.translate
        self.__header_data = [tr('WalletModel', 'Date'),
                              tr('WalletModel', 'Incoming'),
                              tr('WalletModel', 'State of incoming'),
                              tr('WalletModel', 'Expense'), tr('WalletModel', 'State of expense'),
                              tr('WalletModel', 'Loan'), tr('WalletModel', 'State of loan'),
                              tr('WalletModel', 'Debt'), tr('WalletModel', 'State of debt')]
        self.__items = []
        self.__wallet = wallet_file_path
        self.signals = self.Communicate()
        self.__wallet_data = self.WalletData()
        self.__init_signals_slots()

    def __init_signals_slots(self):
        self.signals.signal_model_was_changed.connect(self.__on_model_changed)

    @pyqtSlot()
    def __on_model_changed(self):
        self.sort()

    def sort(self, column=None, order=None):
        self.__items = sorted(self.__items)
        if order == Qt.DescendingOrder:
            self.__items.reverse()

    def data(self, index, role=None):
        if not index.isValid():
            raise WalletModelException('Invalid index')
        if index.row() >= len(self.__items):
            raise WalletModelException('Incorrect item number: %d' % index.row())
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == WalletItemModelType.INDEX_DATE.value:
                return self.__items[index.row()].date()
            elif index.column() == WalletItemModelType.INDEX_INCOMING.value:
                return self.__items[index.row()].incoming().value()
            elif index.column() == WalletItemModelType.INDEX_INCOMING_DESCRIPTION.value:
                return self.__items[index.row()].incoming().description()
            elif index.column() == WalletItemModelType.INDEX_EXPENSE.value:
                return self.__items[index.row()].expense().value()
            elif index.column() == WalletItemModelType.INDEX_EXPENSE_DESCRIPTION.value:
                return self.__items[index.row()].expense().description()
            elif index.column() == WalletItemModelType.INDEX_LOAN.value:
                return self.__items[index.row()].loan().value()
            elif index.column() == WalletItemModelType.INDEX_LOAN_DESCRIPTION.value:
                return self.__items[index.row()].loan().description()
            elif index.column() == WalletItemModelType.INDEX_DEBT.value:
                return self.__items[index.row()].debt().value()
            elif index.column() == WalletItemModelType.INDEX_DEBT_DESCRIPTION.value:
                return self.__items[index.row()].debt().description()

    def setData(self, index, value, role=None):
        if index.isValid() and role == Qt.EditRole:
            if index.column() == WalletItemModelType.INDEX_DATE.value:
                self.__items[index.row()].set_date(value)
            elif index.column() == WalletItemModelType.INDEX_INCOMING.value:
                self.__items[index.row()].incoming().set_value(value)
            elif index.column() == WalletItemModelType.INDEX_INCOMING_DESCRIPTION.value:
                self.__items[index.row()].incoming().set_description(value)
            elif index.column() == WalletItemModelType.INDEX_EXPENSE.value:
                self.__items[index.row()].expense().set_value(value)
            elif index.column() == WalletItemModelType.INDEX_EXPENSE_DESCRIPTION.value:
                self.__items[index.row()].expense().set_description(value)
            elif index.column() == WalletItemModelType.INDEX_LOAN.value:
                self.__items[index.row()].loan().set_value(value)
            elif index.column() == WalletItemModelType.INDEX_LOAN_DESCRIPTION.value:
                self.__items[index.row()].loan().set_description(value)
            elif index.column() == WalletItemModelType.INDEX_DEBT.value:
                self.__items[index.row()].debt().set_value(value)
            elif index.column() == WalletItemModelType.INDEX_DEBT_DESCRIPTION.value:
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

    def __append_entries_from_xml(self, date, entries, entry_type):
        for entry in entries:
            amount = entry.attrib['value']
            description = entry.attrib['description']
            self.append_entry(date, amount, description, entry_type, add_to_xml=False)

    def append_entry(self, date, amount, description, entry_type, add_to_xml=True):
        item = WalletItem(amount, description)
        row = WalletRow()
        # Тег элемента, который может быть записан в XML
        tag = str()
        if entry_type == WalletItemType.INCOMING:
            row.set_incoming(date, item)
            tag = 'incoming'
            self.__wallet_data.incoming += float(amount)
        elif entry_type == WalletItemType.EXPENSE:
            row.set_expense(date, item)
            tag = 'expense'
            self.__wallet_data.expense += float(amount)
        elif entry_type == WalletItemType.LOAN:
            row.set_loan(date, item)
            tag = 'loan'
            self.__wallet_data.loan += float(amount)
        elif entry_type == WalletItemType.DEBT:
            row.set_debt(date, item)
            tag = 'debt'
            self.__wallet_data.debt += float(amount)
        self.__items.append(row)
        self.signals.signal_model_was_changed.emit()
        if add_to_xml:
            self.__add_item_to_xml(date, item, tag)

    def remove_entry(self, date, amount, description, entry_type):
        item = WalletItem(amount, description)
        row = WalletRow()
        # Тег элемента, который должен быть удалён из XML
        tag = str()
        if entry_type == WalletItemType.INCOMING:
            row.set_incoming(date, item)
            tag = 'incoming'
            self.__wallet_data.incoming -= float(amount)
        elif entry_type == WalletItemType.EXPENSE:
            row.set_expense(date, item)
            tag = 'expense'
            self.__wallet_data.expense -= float(amount)
        elif entry_type == WalletItemType.LOAN:
            row.set_loan(date, item)
            tag = 'loan'
            self.__wallet_data.loan -= float(amount)
        elif entry_type == WalletItemType.DEBT:
            row.set_debt(date, item)
            tag = 'debt'
            self.__wallet_data.debt -= float(amount)
        self.__items.remove(row)
        self.__remove_item_from_xml(date, item, tag)

    def wallet_data(self):
        return self.__wallet_data

    def __read_wallet(self):
        # Очищаем модель
        self.__items.clear()
        # Сбрасываем состояние доходов/расходов
        self.__wallet_data = self.WalletData()
        # Разбираем XML с данными
        tree = etree.parse(self.__wallet)
        if tree:
            root = tree.getroot()
            current_date = QDate.currentDate()
            # Получаем узел с текущим годом
            try:
                year = root.findall('year')[-1]
                # Получаем узел с последнем месяцем, данные по которому содержатся в XML
                month = year.findall('month')[-1]
                if int(year.attrib['value']) == current_date.year() and \
                        int(month.attrib['value']) == current_date.month():
                    # Получаем остаток на начало месяца
                    try:
                        self.__wallet_data.balance = float(month.attrib['rest'])
                    except KeyError:
                        self.__wallet_data.balance = float()
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
                        self.__append_entries_from_xml(day_date, incoming_entries, WalletItemType.INCOMING)
                        self.__append_entries_from_xml(day_date, expenses_entries, WalletItemType.EXPENSE)
                        self.__append_entries_from_xml(day_date, loan_entries, WalletItemType.LOAN)
                        self.__append_entries_from_xml(day_date, debt_entries, WalletItemType.DEBT)
            except IndexError:
                pass

    def __add_item_to_xml(self, date, item, tag):
        def get_current_xml_item(parent, tag_name, value):
            items = parent.findall(tag_name)
            if not items:
                # Создаем элемент
                found_item = etree.SubElement(parent, tag_name, {'value': value})
            else:
                found_item = sorted(items, key=lambda x: x.attrib['value'])[-1]
            if not found_item.attrib['value'] == value:
                # Нашли узел в XML, но не совпадает атрибут value, создаем новый
                found_item = etree.SubElement(parent, tag_name, {'value': value})
            # TODO: Выполнить сортировку узлов по аттрибуту value
            return found_item

        item_day = date.split('.')[0]
        item_month = date.split('.')[1]
        item_year = date.split('.')[2]
        parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
        tree = etree.parse(self.__wallet, parser)
        if tree:
            root = tree.getroot()
            year = get_current_xml_item(root, 'year', item_year)
            month = get_current_xml_item(year, 'month', item_month)
            day = get_current_xml_item(month, 'day', item_day)
            # Записываем данные
            etree.SubElement(day, tag, attrib={'value': item.value(), 'description': item.description()})
            tree.write(self.__wallet)

    def __remove_item_from_xml(self, date, item, tag):
        tree = etree.parse(self.__wallet)
        item_day = date.split('.')[0]
        item_month = date.split('.')[1]
        item_year = date.split('.')[2]
        if tree:
            items = tree.xpath('//%s[@value=\'%s\']' % (tag, item.value()))
            item = sorted(items, key=lambda x: x.attrib['value'])[-1]
            if item is not None:
                day = item.getparent()
                month = day.getparent()
                year = month.getparent()
                if day.attrib['value'] == item_day \
                        and month.attrib['value'] == item_month \
                        and year.attrib['value'] == item_year:
                    day.remove(item)
                    tree.write(self.__wallet)