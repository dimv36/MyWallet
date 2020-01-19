__author__ = 'dimv36'
import sys
from platform import system

from PySide2.QtWidgets import (
    QMainWindow, QDialog, QMessageBox, QFileDialog
)
from PySide2.QtCore import (
    QSettings, QDir, QFileInfo, QDate, Slot
)

from mywallet import *
from .mvc.walletmodel import *
from .dialogs import *
from .enums import WalletModelColumns
from .ui.ui_mainwindow import Ui_MainWindow
from .version import MY_WALLET_VERSION_STR


class MainWindow(QMainWindow):
    MAIN_SETTINGS = 'mywallet'

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__current_path = None
        self.__wallet_name = None
        self.__model = WalletModel()

        self.ui.view.setItemDelegate(WalletItemDelegate())
        # Подключаем необходимые сигналы ко слотам
        self.init_signal_slots()
        # Читаем настройки из конфигурационного файла
        self.read_settings()
        # Открываем бумажник
        self.__open_wallet()

    def init_signal_slots(self):
        for (action, handler) in ((self.ui.action_exit, self._on_exit),
                                  (self.ui.action_settings, self._on_settings),
                                  (self.ui.action_open_wallet, self._on_open_wallet),
                                  (self.ui.action_new_wallet, self._on_new_wallet),
                                  (self.ui.action_about, self._on_about),
                                  (self.ui.action_change_balance, self._on_change_balance),
                                  (self.ui.action_add_item, self._on_add_item),
                                  (self.ui.action_delete_item, self._on_delete_item),
                                  (self.ui.action_show_statistic, self._on_statistic_show),
                                  (self.ui.action_pay_debt_off, self._on_pay_debt_off),
                                  (self.ui.action_savings_to_incoming, self._on_savings_to_incoming)):
            action.triggered.connect(handler)
        self.__model.wallet_metadata_changed.connect(self._on_update)
        for widget in (self.ui.start_date_edit, self.ui.end_date_edit):
            widget.dateChanged.connect(self._on_date_range_changed)

    def set_current_path(self, path):
        if not path.endswith('/'):
            path += '/'
        self.__current_path = path

    def __open_wallet(self):
        try:
            if self.__wallet_name and self.__current_path:
                self.__model.open_wallet('{}/{}'.format(self.__current_path, self.__wallet_name))
                self.__update_date_range(self.__model.available_data_range)
            self.ui.view.setModel(self.__model)
            self.ui.view.resizeColumnsToContents()
            self.ui.view.scrollToBottom()
        except WalletModelException as e:
            QMessageBox.critical(self,
                                 self.tr('Could not open wallet'),
                                 str(e))
            self.__current_path = None
            self.__wallet_name = None
            self.write_settings()

    def __update_date_range(self, date_range):
        start, end = date_range.start, date_range.end
        for widget in (self.ui.start_date_edit,
                       self.ui.end_date_edit):
            widget.blockSignals(True)
            widget.setMinimumDate(start)
            widget.setMaximumDate(end)
            widget.blockSignals(False)

    def read_settings(self):
        settings = QSettings('MyWallet')
        if system() == 'Windows':
            self.set_current_path(QDir.home().path() + '/MyWallet/')
            settings = QSettings(self.__current_path + 'mywallet.conf', QSettings.IniFormat)
        settings.beginGroup(self.MAIN_SETTINGS)
        if settings.contains('size'):
            value = settings.value('size')
            if value:
                self.resize(value)
        if settings.contains('position'):
            value = settings.value('position')
            if value:
                self.move(value)
        if settings.contains('path') and settings.value('wallet_name'):
            self.set_current_path(settings.value('path'))
            self.__wallet_name = settings.value('wallet_name')
        else:
            if system() == 'Windows':
                self.set_current_path(QDir.home().path() + '/MyWallet/')
            elif system() == 'Linux':
                self.set_current_path(QDir.home().path() + '/.MyWallet/')
            self.__wallet_name = None
        settings.endGroup()

    def write_settings(self):
        settings = QSettings('MyWallet')
        if system() == 'Windows' and self.__current_path:
            settings = QSettings(self.__current_path + 'mywallet.conf', QSettings.IniFormat)
        settings.beginGroup(self.MAIN_SETTINGS)
        settings.setValue('size', self.size())
        settings.setValue('position', self.pos())
        if self.__current_path:
            settings.setValue('path', self.__current_path)
        if self.__wallet_name:
            settings.setValue('wallet_name', self.__wallet_name)
        settings.endGroup()

    def closeEvent(self, event):
        self.write_settings()
        super().closeEvent(event)

    # Слот закрытия приложения
    @Slot()
    def _on_exit(self):
        self.write_settings()
        sys.exit(0)

    # Слот настроек
    @Slot()
    def _on_settings(self):
        dialog = SettingsDialog(self.__current_path, self.__wallet_name)
        if dialog.exec() == QDialog.Accepted:
            directory = dialog.directory()
            wallet_name = dialog.wallet_name()
            old_directory = self.__current_path
            old_wallet = self.__wallet_name
            if not directory == self.__current_path or not wallet_name == self.__wallet_name:
                self.set_current_path(directory)
                self.__wallet_name = wallet_name
                wallet_path = self.__current_path + self.__wallet_name
                try:
                    self.read_wallet_and_update_view(wallet_path)
                    pass
                except OSError:
                    QMessageBox.warning(self,
                                        self.tr('MyWallet'),
                                        self.tr('File \'{}\' does not exist').format(wallet_path))
                    self.set_current_path(old_directory)
                    self.__wallet_name = old_wallet
                    self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот окрытия кошелька
    @Slot()
    def _on_open_wallet(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                self.tr('Choose file'),
                                                self.__current_path,
                                                self.tr('DB-files (*.db)'))[0]
        if not file_name:
            return
        directory = QFileInfo(file_name).dir().path()
        wallet_name = QFileInfo(file_name).fileName()
        self.set_current_path(QFileInfo(file_name).dir().path())
        self.__wallet_name = QFileInfo(file_name).fileName()
        self.__model.set_wallet_path(directory, wallet_name)

    # Слот обновления данных доходов/расходов/займов/долгов/остатка на начало месяца приложения
    @Slot(WalletData)
    def _on_update(self, data):
        # Обновляем заголовок окна
        self.setWindowTitle(self.__current_path + self.__wallet_name + ' [MyWallet]')
        start, end = data.date_range.start, data.date_range.end
        self.ui.start_date_edit.setDate(start)
        self.ui.end_date_edit.setDate(end)
        self.ui.label_incoming_value.setText(STR_FLOAT_FORMAT % data.incoming)
        self.ui.label_expense_value.setText(STR_FLOAT_FORMAT % data.expense)
        self.ui.label_saving_value.setText(STR_FLOAT_FORMAT % data.savings)
        self.ui.label_debt_value.setText(STR_FLOAT_FORMAT % data.debt)
        self.ui.label_balance_value.setText(STR_FLOAT_FORMAT % data.balance_at_start)
        if data.balance_at_end >= 0:
            self.ui.label_total_value.setStyleSheet('QLabel { color : green }')
        else:
            self.ui.label_total_value.setStyleSheet('QLabel { color : red }')
        self.ui.label_total_value.setText(STR_FLOAT_FORMAT % data.balance_at_end)
        self.ui.view.resizeColumnsToContents()
        self.ui.view.scrollToBottom()

    # Слот создания нового бумажника
    @Slot()
    def _on_new_wallet(self):
        # TODO: Было бы круто использовать стандартные методы
        dialog = NewWalletDialog(self.__current_path)
        if dialog.exec() == QDialog.Accepted:
            directory = dialog.directory()
            wallet_name = dialog.wallet_name()
            if not wallet_name:
                return
            file_name = '{}/{}'.format(directory, wallet_name)
            if QFileInfo.exists(file_name):
                result = QMessageBox.question(self,
                                              self.tr('Create new wallet'),
                                              self.tr('Wallet \'{}\' already exists. Rewrite?').format(wallet_name))
                if result == QMessageBox.No:
                    return
            if not wallet_name.endswith('.db'):
                file_name = '{}.db'.format(file_name)
            try:
                WalletModel.create_new_wallet(file_name)
            except WalletModelException as e:
                QMessageBox.critical(self, self.tr('Create new wallet'), str(e))
            else:
                QMessageBox.information(self,
                                        self.tr('Create new wallet'),
                                        self.tr('Wallet \'{}\' was created').format(wallet_name))

    # Слот добавления источников данных
    @Slot()
    def _on_add_item(self):
        dialog = AddSourcesDialog()
        if dialog.exec() == dialog.Accepted:
            date = dialog.date()
            incoming = dialog.incoming()
            expense = dialog.expense()
            savings = dialog.savings()
            debt = dialog.debt()
            try:
                for item in incoming:
                    self.__model.add_entry({WalletModelColumns.INDEX_DATE: date,
                                            WalletModelColumns.INDEX_INCOMING: item['value'],
                                            WalletModelColumns.INDEX_DESCRIPTION: item['description']})
                for item in expense:
                    self.__model.add_entry({WalletModelColumns.INDEX_DATE: date,
                                            WalletModelColumns.INDEX_EXPENSE: item['value'],
                                            WalletModelColumns.INDEX_DESCRIPTION: item['description']})
                for item in savings:
                    self.__model.add_entry({WalletModelColumns.INDEX_DATE: date,
                                            WalletModelColumns.INDEX_SAVINGS: item['value'],
                                            WalletModelColumns.INDEX_DESCRIPTION: item['description']})
                for item in debt:
                    self.__model.add_entry({WalletModelColumns.INDEX_DATE: date,
                                            WalletModelColumns.INDEX_DEBT: item['value'],
                                            WalletModelColumns.INDEX_DESCRIPTION: item['description']})
            except WalletModelException as e:
                QMessageBox.critical(self,
                                     self.tr('Add sources dialog'),
                                     self.tr('Failed to add sources: {}').format(e))
            self.ui.view.resizeColumnsToContents()

    # Слот удаления записи из таблицы
    @Slot()
    def _on_delete_item(self):
        selected_indexes = self.ui.view.selectedIndexes()
        if not selected_indexes:
            return
        item = {index.column(): index.data() for index in selected_indexes}
        try:
            self.__model.remove_entry(item)
        except WalletModelException as e:
            QMessageBox.critical(self,
                                 self.tr('Remove sources dialog'),
                                 self.tr('Failed to remove sources: {}').format(e))

    # Слот изменения остатка на начало месяца
    @Slot()
    def _on_change_balance(self):
        dialog = ChangeMonthBalanceDialog()
        dialog.set_month_balance(float(self.ui.label_balance_value.text()))
        if dialog.exec() == QDialog.Accepted:
            balance = dialog.balance()
            self.__model.change_balance_at_start_of_month(balance)

    # Слот отображения информации о программе
    @Slot()
    def _on_about(self):
        QMessageBox.about(self,
                          self.tr('About application'),
                          self.tr('MyWallet developed in June 2015\n'
                                  'author: Dmitry Voronin\n'
                                  'email: carriingfate92@yandex.ru\n'
                                  'version: {}').format(MY_WALLET_VERSION_STR))

    # Слот отображения статистики
    @Slot()
    def _on_statistic_show(self):
        # TODO: Реализовать
        pass
        # dialog = StatisticDialog(self.__model)
        # dialog.exec()

    # Слот погашения долга
    @Slot()
    def _on_pay_debt_off(self):
        current_debt = self.__model.get_metadata().debt
        dialog = PayOffDebtDialog(current_debt)
        if dialog.exec() == QDialog.Accepted:
            item = dialog.data()
            if abs(item['value']) > current_debt:
                QMessageBox.warning(self,
                                    self.tr('Pay debt off'),
                                    self.tr('You can not repay the debt by this amount'))
                return
            self.__model.add_entry({WalletModelColumns.INDEX_DATE: QDate.currentDate(),
                                    WalletModelColumns.INDEX_DEBT: item['value'],
                                    WalletModelColumns.INDEX_DESCRIPTION: item['description']})

    # Слот преобразования накоплений в доходы
    @Slot()
    def _on_savings_to_incoming(self):
        current_savings = self.__model.get_metadata().savings
        dialog = SavingsToIncomingDialog(current_savings)
        if dialog.exec() == QDialog.Accepted:
            item = dialog.data()
            if item['value'] > current_savings:
                QMessageBox.warning(self,
                                    self.tr('Savings to incoming'),
                                    self.tr('You can not convert savings to incoming by this amount'))
                return
            self.__model.add_entry({WalletModelColumns.INDEX_DATE: QDate.currentDate(),
                                    WalletModelColumns.INDEX_SAVINGS: item['value'],
                                    WalletModelColumns.INDEX_DESCRIPTION: item['description']})

    # Слот изменения периода отчета
    @Slot()
    def _on_date_range_changed(self):
        print('changed', self.sender().objectName())
        start = self.ui.start_date_edit.date()
        end = self.ui.end_date_edit.date()
        date_range = WalletDateRange(start, end)
        self.__model.collect_items(date_range)
        self.ui.view.resizeColumnsToContents()
        self.ui.view.scrollToBottom()
