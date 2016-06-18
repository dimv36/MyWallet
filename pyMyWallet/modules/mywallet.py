__author__ = 'dimv36'
import sys
from platform import system

from PyQt5.QtWidgets import (
    QMainWindow, QDialog, QMessageBox, QFileDialog
)
from PyQt5.QtCore import (
    QSettings, pyqtSlot, QDir, QSize, QPoint, QFileInfo, QDate
)

from modules import *
from modules.mvc.walletmodel import WalletModel, WalletData, WalletModelException
from modules.enums import WalletItemModelType
from modules.dialogs import *
from modules.ui.ui_mywallet import Ui_MyWallet
from modules.version import MY_WALLET_VERSION_STR


class MyWallet(QMainWindow, Ui_MyWallet):
    MAIN_SETTINGS = 'mywallet'

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__current_path = None
        self.__wallet_name = None
        self.__model = WalletModel()

        # Подключаем необходимые сигналы ко слотам
        self.init_signal_slots()
        # Читаем настройки из конфигурационного файла
        self.read_settings()
        # Открываем бумажник
        self.__open_wallet()

    def init_signal_slots(self):
        self._action_exit.pyqtConfigure(triggered=self.on_exit)
        self._action_settings.pyqtConfigure(triggered=self.on_settings)
        self._action_open_wallet.pyqtConfigure(triggered=self.on_open_wallet)
        self._action_new_wallet.pyqtConfigure(triggered=self.on_new_wallet)
        self._action_add_item.pyqtConfigure(triggered=self.on_add_item)
        self._action_delete_item.pyqtConfigure(triggered=self.on_delete_item)
        self._action_change_balance.pyqtConfigure(triggered=self.on_change_balance)
        self._action_about.pyqtConfigure(triggered=self.on_about)
        self._action_show_statistic.pyqtConfigure(triggered=self.on_statistic_show)
        self._action_pay_debt_off.pyqtConfigure(triggered=self.on_pay_debt_off)
        self._action_savings_to_incoming.pyqtConfigure(triggered=self.on_savings_to_incoming)
        self.__model.signal_wallet_metadata_changed.connect(self.on_update)

    def set_current_path(self, path):
        if not path.endswith('/'):
            path += '/'
        self.__current_path = path

    def __open_wallet(self):
        try:
            if self.__wallet_name and self.__current_path:
                self.__model.set_wallet_path(self.__current_path, self.__wallet_name)
            self._view.setModel(self.__model)
            self._view.resizeColumnsToContents()
            self._view.scrollToBottom()
        except WalletModelException as e:
            QMessageBox.critical(self,
                                 tr('MyWallet', 'Could not open wallet'),
                                 str(e))
            self.__current_path = None
            self.__wallet_name = None
            self.write_settings()

    def read_settings(self):
        settings = QSettings('MyWallet')
        if system() == 'Windows':
            self.set_current_path(QDir.home().path() + '/MyWallet/')
            settings = QSettings('MyWallet', self.__current_path + 'mywallet.conf', QSettings.IniFormat)
        settings.beginGroup(self.MAIN_SETTINGS)
        self.resize(settings.value('size', type=QSize))
        self.move(settings.value('position', type=QPoint))
        if settings.value('path') and settings.value('wallet_name'):
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
        if system() == 'Windows':
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
    @pyqtSlot()
    def on_exit(self):
        self.write_settings()
        sys.exit(0)

    # Слот настроек
    @pyqtSlot()
    def on_settings(self):
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
                                        tr('MyWallet', 'MyWallet'),
                                        tr('MyWallet', 'File %s does not exist' % wallet_path)
                                        )
                    self.set_current_path(old_directory)
                    self.__wallet_name = old_wallet
                    self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот окрытия кошелька
    @pyqtSlot()
    def on_open_wallet(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                tr('MyWallet', 'Choose file'),
                                                self.__current_path,
                                                tr('MyWallet', 'DB-files (*.db)'))[0]
        if not file_name:
            return
        directory = QFileInfo(file_name).dir().path()
        wallet_name = QFileInfo(file_name).fileName()
        self.set_current_path(QFileInfo(file_name).dir().path())
        self.__wallet_name = QFileInfo(file_name).fileName()
        self.__model.set_wallet_path(directory, wallet_name)

    # Слот обновления данных доходов/расходов/займов/долгов/остатка на начало месяца приложения
    @pyqtSlot(WalletData)
    def on_update(self, data):
        # Обновляем заголовок окна
        self.setWindowTitle(self.__current_path + self.__wallet_name + ' [MyWallet]')
        self._label_incoming_value.setText(STR_FLOAT_FORMAT % data.incoming)
        self._label_expense_value.setText(STR_FLOAT_FORMAT % data.expense)
        self._label_saving_value.setText(STR_FLOAT_FORMAT % data.savings)
        self._label_debt_value.setText(STR_FLOAT_FORMAT % data.debt)
        self._label_balance_value.setText(STR_FLOAT_FORMAT % data.balance_at_start)
        if data.balance_at_end >= 0:
            self._label_total_value.setStyleSheet('QLabel { color : green }')
        else:
            self._label_total_value.setStyleSheet('QLabel { color : red }')
        self._label_total_value.setText(STR_FLOAT_FORMAT % data.balance_at_end)
        self._view.resizeColumnsToContents()
        self._view.scrollToBottom()

    # Слот создания нового бумажника
    @pyqtSlot()
    def on_new_wallet(self):
        # TODO: Было бы круто использовать стандартные методы
        dialog = NewWalletDialog(self.__current_path)
        if dialog.exec() == QDialog.Accepted:
            directory = dialog.directory()
            wallet_name = dialog.wallet_name()
            if not wallet_name:
                return
            file_name = '%s/%s' % (directory, wallet_name)
            if QFileInfo.exists(file_name):
                result = QMessageBox.question(self,
                                              tr('MyWallet', 'Create new wallet'),
                                              tr('MyWallet', 'Wallet \'%s\' already exists. Rewrite?' % wallet_name))
                if result == QMessageBox.No:
                    return
            if not wallet_name.endswith('.db'):
                file_name = '%s.db' % file_name
            try:
                WalletModel.create_new_wallet(file_name)
            except WalletModelException as e:
                QMessageBox.critical(self, tr('MyWallet', 'Create new wallet'), str(e))
            else:
                QMessageBox.information(self,
                                        tr('MyWallet', 'Create new wallet'),
                                        tr('MyWallet', 'Wallet \'%s\' was created' % wallet_name))

    # Слот добавления источников данных
    @pyqtSlot()
    def on_add_item(self):
        dialog = AddSourcesDialog()
        if dialog.exec() == dialog.Accepted:
            date = dialog.date()
            incoming = dialog.incoming()
            expense = dialog.expense()
            savings = dialog.savings()
            debt = dialog.debt()
            try:
                for item in incoming:
                    self.__model.add_entry({WalletItemModelType.INDEX_DATE.value: date,
                                            WalletItemModelType.INDEX_INCOMING.value: item['value'],
                                            WalletItemModelType.INDEX_DESCRIPTION.value: item['description']})
                for item in expense:
                    self.__model.add_entry({WalletItemModelType.INDEX_DATE.value: date,
                                            WalletItemModelType.INDEX_EXPENSE.value: item['value'],
                                            WalletItemModelType.INDEX_DESCRIPTION.value: item['description']})
                for item in savings:
                    self.__model.add_entry({WalletItemModelType.INDEX_DATE.value: date,
                                            WalletItemModelType.INDEX_SAVINGS.value: item['value'],
                                            WalletItemModelType.INDEX_DESCRIPTION.value: item['description']})
                for item in debt:
                    self.__model.add_entry({WalletItemModelType.INDEX_DATE.value: date,
                                            WalletItemModelType.INDEX_DEBT.value: item['value'],
                                            WalletItemModelType.INDEX_DESCRIPTION.value: item['description']})
            except WalletModelException as e:
                QMessageBox.critical(self,
                                     tr('MyWallet', 'Add sources dialog'),
                                     tr('MyWallet', 'Failed to add sources: %s' % e))
            self._view.resizeColumnsToContents()

    # Слот удаления записи из таблицы
    @pyqtSlot()
    def on_delete_item(self):
        selected_indexes = self._view.selectedIndexes()
        if not selected_indexes:
            return
        item = {index.column(): index.data() for index in selected_indexes}
        try:
            self.__model.remove_entry(item)
        except WalletModelException as e:
            QMessageBox.critical(self,
                                 tr('MyWallet', 'Remove sources dialog'),
                                 tr('MyWallet', 'Failed to remove sources: %s' % e))

    # Слот изменения остатка на начало месяца
    @pyqtSlot()
    def on_change_balance(self):
        dialog = ChangeMonthBalanceDialog()
        dialog.set_month_balance(float(self._label_balance_value.text()))
        if dialog.exec() == QDialog.Accepted:
            balance = dialog.balance()
            self.__model.change_balance_at_start_of_month(balance)

    # Слот отображения информации о программе
    @pyqtSlot()
    def on_about(self):
        QMessageBox.about(self,
                          tr('MyWallet', 'About application'),
                          tr('MyWallet', 'MyWallet developed in June 2015\n'
                                         'author: Dmitry Voronin\n'
                                         'email: carriingfate92@yandex.ru\n'
                                         'version: %s') % MY_WALLET_VERSION_STR)

    # Слот отображения статистики
    @pyqtSlot()
    def on_statistic_show(self):
        # TODO: Реализовать
        pass
        # dialog = StatisticDialog(self.__model)
        # dialog.exec()

    # Слот погашения долга
    @pyqtSlot()
    def on_pay_debt_off(self):
        current_debt = self.__model.get_metadata().debt
        dialog = PayOffDebtDialog(current_debt)
        if dialog.exec() == QDialog.Accepted:
            item = dialog.data()
            if abs(item['value']) > current_debt:
                QMessageBox.warning(self,
                                    tr('MyWallet', 'Pay debt off'),
                                    tr('MyWallet', 'You can not repay the debt by this amount'))
                return
            self.__model.add_entry({WalletItemModelType.INDEX_DATE.value: QDate.currentDate(),
                                    WalletItemModelType.INDEX_DEBT.value: item['value'],
                                    WalletItemModelType.INDEX_DESCRIPTION.value: item['description']})

    # Слот преобразования накоплений в доходы
    @pyqtSlot()
    def on_savings_to_incoming(self):
        current_savings = self.__model.get_metadata().savings
        dialog = SavingsToIncomingDialog(current_savings)
        if dialog.exec() == QDialog.Accepted:
            item = dialog.data()
            if item['value'] > current_savings:
                QMessageBox.warning(self,
                                    tr('MyWallet', 'Savings to incoming'),
                                    tr('MyWallet', 'You can not convert savings to incoming by this amount'))
                return
            self.__model.add_entry({WalletItemModelType.INDEX_DATE.value: QDate.currentDate(),
                                    WalletItemModelType.INDEX_SAVINGS.value: item['value'],
                                    WalletItemModelType.INDEX_DESCRIPTION.value: item['description']})
