__author__ = 'dimv36'
import sys
from platform import system

from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QDialog, QMessageBox
)
from PyQt5.QtCore import (
    QSettings, QObject, pyqtSlot, pyqtSignal, QCoreApplication,
    QDir, QSize, QPoint, QFileInfo, QModelIndex
)

from modules.mvc.walletmodel import WalletModel
from modules.enums import WalletItemType, WalletItemModelType
from modules.dialogs.settingsdialog import SettingsDialog
from modules.dialogs.newwalletdialog import NewWalletDialog
from modules.dialogs.addsourcesdialog import AddSourcesDialog
from modules.dialogs.changemonthbalance import ChangeMonthBalance
from modules.ui.ui_mywallet import Ui_MyWallet


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

        # Устанавливаем модель
        self._model = WalletModel(self.__current_path + self.__wallet_name)
        self.read_wallet_and_update_view()

        # Отправляем сигнал обновления заголовка окна
        self._signals.signal_wallet_changed.emit()

    def init_signal_slots(self):
        self._action_exit.pyqtConfigure(triggered=self.on_exit)
        self._action_settings.pyqtConfigure(triggered=self.on_settings)
        self._action_open_wallet.pyqtConfigure(triggered=self.on_open_wallet)
        self._action_new_wallet.pyqtConfigure(triggered=self.on_new_wallet)
        self._action_add_item.pyqtConfigure(triggered=self.on_add_item)
        self._action_delete_item.pyqtConfigure(triggered=self.on_delete_item)
        self._action_change_balance.pyqtConfigure(triggered=self.on_change_balance)
        self._action_about.pyqtConfigure(triggered=self.on_about)
        self._signals.signal_wallet_changed.connect(self.on_update)

    def set_current_path(self, path):
        if not path.endswith('/'):
            path += '/'
        self.__current_path = path

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
            self.__wallet_name = 'wallet.xml'
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

    def read_wallet_and_update_view(self, wallet_path=None):
        self._model.read_wallet(wallet_path)
        self._model.beginResetModel()
        self._view.setModel(self._model)
        self._model.endResetModel()
        self._view.resizeColumnsToContents()
        # Отправляем сигнал на обновление заголовка окна приложения
        self._signals.signal_wallet_changed.emit()
        self._view.scrollTo()

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
                                                QCoreApplication.translate('MyWallet', 'XML-files (*.xml)'))[0]
        directory = QFileInfo(file_name).dir().path()
        wallet_name = QFileInfo(file_name).fileName()
        if wallet_name and not file_name == self.__current_path + self.__wallet_name:
            self.set_current_path(directory)
            self.__wallet_name = wallet_name
            self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот обновления данных доходов/расходов/займов/долгов/остатка на начало месяца приложения
    @pyqtSlot()
    def on_update(self):
        self.setWindowTitle(self.__current_path + self.__wallet_name + ' [MyWallet]')
        wallet_data = self._model.wallet_data()
        total = wallet_data.balance + wallet_data.incoming - wallet_data.expense + wallet_data.loan - wallet_data.debt
        total = round(total, 2)
        self._label_incoming_value.setText(str(round(wallet_data.incoming, 2)))
        self._label_expense_value.setText(str(round(wallet_data.expense, 2)))
        self._label_loan_value.setText(str(round(wallet_data.loan, 2)))
        self._label_debt_value.setText(str(round(wallet_data.debt, 2)))
        self._label_balance_value.setText(str(round(wallet_data.balance)))
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
            self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот добавления источников данных
    @pyqtSlot()
    def on_add_item(self):
        dialog = AddSourcesDialog()
        if dialog.exec() == dialog.Accepted:
            date = dialog.date().toString('dd.MM.yyyy')
            incoming = dialog.incoming()
            expense = dialog.expense()
            loan = dialog.loan()
            debt = dialog.debt()
            self._model.beginResetModel()
            for item in incoming:
                self._model.append_entry(date, item[0], item[1], WalletItemType.INCOMING)
            for item in expense:
                self._model.append_entry(date, item[0], item[1], WalletItemType.EXPENSE)
            for item in loan:
                self._model.append_entry(date, item[0], item[1], WalletItemType.LOAN)
            for item in debt:
                self._model.append_entry(date, item[0], item[1], WalletItemType.DEBT)
            self._model.endResetModel()
            self._view.resizeColumnsToContents()
            self._signals.signal_wallet_changed.emit()
            # Прокручиваем скроллер
            self._view.scrollToBottom()

    # Слот удаления записи из таблицы
    @pyqtSlot()
    def on_delete_item(self):
        if not self._view.selectedIndexes():
            return
        # Определяем тип объекта
        item_type = None
        item_data = []
        for index in self._view.selectedIndexes():
            index = QModelIndex(index)
            if index.column() == WalletItemModelType.INDEX_DATE:
                item_data.append(index.data())
            elif not index.column() == WalletItemModelType.INDEX_DATE and index.data():
                if WalletItemModelType.INDEX_INCOMING.value <= index.column() \
                        <= WalletItemModelType.INDEX_INCOMING_DESCRIPTION.value:
                    item_type = WalletItemType.INCOMING
                elif WalletItemModelType.INDEX_EXPENSE.value <= index.column() \
                        <= WalletItemModelType.INDEX_EXPENSE_DESCRIPTION.value:
                    item_type = WalletItemType.EXPENSE
                elif WalletItemModelType.INDEX_LOAN.value <= index.column() \
                        <= WalletItemModelType.INDEX_LOAN_DESCRIPTION.value:
                    item_type = WalletItemType.LOAN
                elif WalletItemModelType.INDEX_DEBT.value <= index.column() \
                        <= WalletItemModelType.INDEX_DEBT_DESCRIPTION.value:
                    item_type = WalletItemType.DEBT
                item_data.append(index.data())
        self._model.beginResetModel()
        self._model.remove_entry(item_data[0], item_data[1], item_data[2], item_type)
        self._model.endResetModel()
        self._view.clearSelection()
        self._signals.signal_wallet_changed.emit()

    # Слот изменения остатка на начало месяца
    @pyqtSlot()
    def on_change_balance(self):
        dialog = ChangeMonthBalance()
        dialog.set_month_balance(float(self._label_balance_value.text()))
        if dialog.exec() == QDialog.Accepted:
            balance = dialog.balance()
            self._model.change_current_month_balance(balance)
            self._signals.signal_wallet_changed.emit()

    # Слот отображения информации о программе
    @pyqtSlot()
    def on_about(self):
        dialog = QMessageBox.about(self,
                                   QCoreApplication.translate('MyWallet', 'About application'),
                                   QCoreApplication.translate('MyWallet', 'MyWallet developed at June 2015\n'
                                                                          'author: Dmitry Voronin\n'
                                                                          'email: carriingfate92@yandex.ru\n'
                                                                          'version: 0.10'))
        dialog.exec()