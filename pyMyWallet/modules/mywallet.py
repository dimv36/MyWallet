import sys
from platform import system

from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QDialog, QMessageBox
)
from PyQt5.QtCore import (
    QSettings, QObject, pyqtSlot, pyqtSignal, QCoreApplication,
    QDir, QSize, QPoint, QFileInfo, QModelIndex, QDate
)

from modules.mvc.walletmodel import WalletModel
from modules.enums import WalletItemType, WalletItemModelType
from modules.dialogs import *
from modules.ui.ui_mywallet import Ui_MyWallet
from modules.version import MY_WALLET_VERSION_STR


class MyWallet(QMainWindow, Ui_MyWallet):
    class Communicate(QObject):
        signal_wallet_changed = pyqtSignal()

    MAIN_SETTINGS = 'mywallet'

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._signals = self.Communicate()

        self.__current_path = None
        self.__wallet_name = None

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
        self._signals.signal_wallet_changed.connect(self.on_update)

    def set_current_path(self, path):
        if not path.endswith('/'):
            path += '/'
        self.__current_path = path

    def __open_wallet(self):
        # Устанавливаем модель
        self._model = WalletModel(self.__current_path + self.__wallet_name)
        self._model.beginResetModel()
        self._view.setModel(self._model)
        self._view.resizeColumnsToContents()
        self._model.endResetModel()

        # Отправляем сигнал обновления заголовка окна
        self._signals.signal_wallet_changed.emit()

    def read_settings(self):
        settings = QSettings()
        if system() == 'Windows':
            self.set_current_path(QDir.home().path() + '/MyWallet/')
            settings = QSettings(self.__current_path + 'mywallet.conf', QSettings.IniFormat)
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
            self.__wallet_name = 'wallet.db'
        settings.endGroup()

    def write_settings(self):
        settings = QSettings()
        if system() == 'Windows':
            settings = QSettings(self.__current_path + 'mywallet.conf', QSettings.IniFormat)
        settings.beginGroup(self.MAIN_SETTINGS)
        settings.setValue('size', self.size())
        settings.setValue('position', self.pos())
        settings.setValue('path', self.__current_path)
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
                                        QCoreApplication.translate('MyWallet', 'MyWallet'),
                                        QCoreApplication.translate('MyWallet', 'File %s does not exist') % wallet_path
                                        )
                    self.set_current_path(old_directory)
                    self.__wallet_name = old_wallet
                    self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот окрытия кошелька
    @pyqtSlot()
    def on_open_wallet(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                QCoreApplication.translate('MyWallet', 'Choose file'),
                                                QDir.current().path(),
                                                QCoreApplication.translate('MyWallet', 'DB-files (*.db)'))[0]
        directory = QFileInfo(file_name).dir().path()
        wallet_name = QFileInfo(file_name).fileName()
        if wallet_name and not file_name == self.__current_path + self.__wallet_name:
            self.set_current_path(directory)
            self.__wallet_name = wallet_name
            self.__open_wallet()

    # Слот обновления данных доходов/расходов/займов/долгов/остатка на начало месяца приложения
    @pyqtSlot()
    def on_update(self):
        wallet_data = self._model.get_wallet_info()
        # Обновляем заголовок окна
        self.setWindowTitle(self.__current_path + self.__wallet_name + ' [MyWallet]')
        total = wallet_data.balance_at_start + wallet_data.incoming + \
            wallet_data.savings - wallet_data.expense
        total = round(total, 2)
        self._label_incoming_value.setText(str(round(wallet_data.incoming, 2)))
        self._label_expense_value.setText(str(round(wallet_data.expense, 2)))
        self._label_saving_value.setText(str(round(wallet_data.savings, 2)))
        self._label_loan_value.setText(str(round(wallet_data.loan, 2)))
        self._label_debt_value.setText(str(round(wallet_data.debt, 2)))
        self._label_balance_value.setText(str(round(wallet_data.balance_at_start, 2)))
        if total >= 0:
            self._label_total_value.setStyleSheet('QLabel { color : green }')
        else:
            self._label_total_value.setStyleSheet('QLabel { color : red }')
        self._label_total_value.setText(str(total))

    # Слот создания нового бумажника
    @pyqtSlot()
    def on_new_wallet(self):
        dialog = NewWalletDialog(self.__current_path)
        if dialog.exec() == QDialog.Accepted:
            wallet_name = dialog.wallet_name()
            directory = dialog.directory()
            self._model.create_new_wallet(directory + wallet_name)
            self.set_current_path(directory)
            self.__wallet_name = wallet_name
            self._signals.signal_wallet_changed.emit()

    # Слот добавления источников данных
    @pyqtSlot()
    def on_add_item(self):
        dialog = AddSourcesDialog()
        if dialog.exec() == dialog.Accepted:
            date = dialog.date()
            incoming = dialog.incoming()
            expense = dialog.expense()
            savings = dialog.savings()
            loan = dialog.loan()
            debt = dialog.debt()
            for item in incoming:
                self._model.add_entry(date, item, WalletItemType.INCOMING)
            for item in expense:
                self._model.add_entry(date, item, WalletItemType.EXPENSE)
            for item in savings:
                self._model.add_entry(date, item, WalletItemType.SAVING)
            for item in loan:
                self._model.add_entry(date, item, WalletItemType.LOAN)
            for item in debt:
                self._model.add_entry(date, item, WalletItemType.DEBT)
            self._view.resizeColumnsToContents()
            self._signals.signal_wallet_changed.emit()
            # Прокручиваем скроллер
            self._view.scrollToBottom()

    # Слот удаления записи из таблицы
    @pyqtSlot()
    def on_delete_item(self):
        selected_indexes = self._view.selectedIndexes()
        if not selected_indexes:
            return
        # Определяем тип объекта
        item_type = None
        day = int()
        month = int()
        year = int()
        item = []
        for index in selected_indexes:
            index = QModelIndex(index)
            if index.column() == WalletItemModelType.INDEX_DAY.value:
                day = self._model.data(index)
            elif index.column() == WalletItemModelType.INDEX_MONTH.value:
                month = self._model.data(index)
            elif index.column() == WalletItemModelType.INDEX_YEAR.value:
                year = self._model.data(index)
            elif index.column() == WalletItemModelType.INDEX_INCOMING.value:
                if index.data():
                    item_type = WalletItemType.INCOMING
                    item.append(index.data())
            elif index.column() == WalletItemModelType.INDEX_EXPENSE.value:
                if index.data():
                    item_type = WalletItemType.EXPENSE
                    item.append(index.data())
            elif index.column() == WalletItemModelType.INDEX_SAVINGS.value:
                if index.data():
                    item_type = WalletItemType.SAVING
                    item.append(index.data())
            elif index.column() == WalletItemModelType.INDEX_LOAN.value:
                if index.data():
                    item_type = WalletItemType.LOAN
                    item.append(index.data())
            elif index.column() == WalletItemModelType.INDEX_DEBT.value:
                if index.data():
                    item_type = WalletItemType.DEBT
                    item.append(index.data())
            elif index.column() == WalletItemModelType.INDEX_DESCRIPTION.value:
                item.append(index.data())
        self._model.remove_entry(QDate(year, month, day), item, item_type)
        self._signals.signal_wallet_changed.emit()

    # Слот изменения остатка на начало месяца
    @pyqtSlot()
    def on_change_balance(self):
        dialog = ChangeMonthBalanceDialog()
        dialog.set_month_balance(float(self._label_balance_value.text()))
        if dialog.exec() == QDialog.Accepted:
            balance = dialog.balance()
            self._model.change_current_month_balance(balance)
            self._signals.signal_wallet_changed.emit()

    # Слот отображения информации о программе
    @pyqtSlot()
    def on_about(self):
        QMessageBox.about(self,
                          QCoreApplication.translate('MyWallet', 'About application'),
                          QCoreApplication.translate('MyWallet', 'MyWallet developed in June 2015\n'
                                                                 'author: Dmitry Voronin\n'
                                                                 'email: carriingfate92@yandex.ru\n'
                                                                 'version: %s') % MY_WALLET_VERSION_STR)

    # Слот отображения статистики
    @pyqtSlot()
    def on_statistic_show(self):
        dialog = StatisticDialog(self._model.root())
        dialog.exec()

    # Слот погашения долга
    @pyqtSlot()
    def on_pay_debt_off(self):
        dialog = PayOffDebtDialog()
        if dialog.exec() == QDialog.Accepted:
            data = dialog.data()
            self._model.beginResetModel()
            self._model.append_entry(QDate.currentDate().toString('dd.MM.yyyy'),
                                     str(-1 * data[0]),
                                     data[1],
                                     WalletItemType.DEBT)
            self._signals.signal_wallet_changed.emit()
            self._model.endResetModel()
