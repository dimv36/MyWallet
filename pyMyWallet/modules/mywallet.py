__author__ = 'dimv36'
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QMessageBox
from PyQt5.QtCore import QSettings, QObject, pyqtSlot, pyqtSignal, QCoreApplication, QDir, QSize, QPoint, QFileInfo
from platform import system

from modules.mvc.walletmodel import WalletModel
from modules.settingsdialog import SettingsDialog
from modules.newwalletdialog import NewWalletDialog
from modules.addsourcesdialog import AddSourcesDialog
from ui.ui_mywallet import Ui_MyWallet


class MyWallet(QMainWindow, Ui_MyWallet):
    class Communicate(QObject):
        signal_wallet_changed = pyqtSignal()

    MAIN_SETTINGS = 'mywallet'
    tr = QCoreApplication.translate

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
        self._signals.signal_wallet_changed.connect(self.on_update)

    def set_current_path(self, path):
        if not path.endswith('/'):
            path += '/'
        self.__current_path = path

    def read_settings(self):
        settings = QSettings()
        if system() == 'Windows':
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
        print('write_settings')
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

    def closeEvent(self, event):
        print('closeEvent')
        self.write_settings()
        super().closeEvent(event)

    # Слот закрытия приложения
    @pyqtSlot()
    def on_exit(self):
        print('on_exit')
        self.write_settings()
        exit(0)

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
                # TODO: WriteXml() call
                self.set_current_path(directory)
                self.__wallet_name = wallet_name
                wallet_path = self.__current_path + self.__wallet_name
                try:
                    self.read_wallet_and_update_view(wallet_path)
                    pass
                except OSError:
                    QMessageBox.warning(self,
                                        self.tr('MyWallet', 'MyWallet'),
                                        self.tr('MyWallet', 'File %s does not exist') % wallet_path
                                        )
                    self.set_current_path(old_directory)
                    self.__wallet_name = old_wallet
                    self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)
                    pass

    # Слот окрытия кошелька
    @pyqtSlot()
    def on_open_wallet(self):
        file_name = QFileDialog.getOpenFileName(self, self.tr('MyWallet', 'Choose file'),
                                                QDir.current().path(),
                                                self.tr('MyWallet', 'XML-files (*.xml)'))[0]
        # TODO: WriteXml() call
        directory = QFileInfo(file_name).dir().path()
        wallet_name = QFileInfo(file_name).fileName()
        if wallet_name and not file_name == self.__current_path + self.__wallet_name:
            self.set_current_path(directory)
            self.__wallet_name = wallet_name
            self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот обновления заголовка приложения
    @pyqtSlot()
    def on_update(self):
        self.setWindowTitle(self.__current_path + self.__wallet_name + ' [MyWallet]')

    # Слот создания нового бумажника
    @pyqtSlot()
    def on_new_wallet(self):
        dialog = NewWalletDialog(self.__current_path)
        if dialog.exec() == QDialog.Accepted:
            wallet_name = dialog.wallet_name()
            directory = dialog.directory()
            # TODO: WriteXml() call
            self._model.create_new_wallet(directory + wallet_name)
            self.set_current_path(directory)
            self.__wallet_name = wallet_name
            self.read_wallet_and_update_view(self.__current_path + self.__wallet_name)

    # Слот дробавления источников данных
    @pyqtSlot()
    def on_add_item(self):
        print('Add item')
        dialog = AddSourcesDialog()
        if dialog.exec() == dialog.Accepted:
            pass
