__author__ = 'dimv36'
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QSettings, pyqtSlot, QCoreApplication, QDir, QSize, QPoint, QFileInfo
from platform import system

from modules.mvc.walletmodel import WalletModel
from modules.settingsdialog import SettingsDialog
from ui.ui_mywallet import Ui_MyWallet


class MyWallet(QMainWindow, Ui_MyWallet):
    MAIN_SETTINGS = 'mywallet'
    tr = QCoreApplication.translate

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__current_path = None
        self.__wallet_name = None

        # Подключаем необходимые сигналы ко слотам
        self.init_signal_slots()
        # Читаем настройки из конфигурационного файла
        self.read_settings()

        # Устанавливаем модель
        self._view.setModel(WalletModel())
        self._view.resizeColumnsToContents()

    def __del__(self):
        print('__del__')
        self.write_settings()

    def init_signal_slots(self):
        self._action_exit.pyqtConfigure(triggered=self.on_exit)
        self._action_settings.pyqtConfigure(triggered=self.on_settings)
        self._action_open_wallet.pyqtConfigure(triggered=self.on_open_wallet)

    def read_settings(self):
        settings = QSettings()
        if system() == 'Windows':
            settings = QSettings(self.__current_path + '/mywallet.conf', QSettings.IniFormat)
        settings.beginGroup(self.MAIN_SETTINGS)
        self.resize(settings.value('size', type=QSize))
        self.move(settings.value('position', type=QPoint))
        if settings.value('path') and settings.value('wallet_name'):
            self.__current_path = settings.value('path')
            self.__wallet_name = settings.value('wallet_name')
        settings.endGroup()

    def write_settings(self):
        settings = QSettings()
        if system() == 'Windows':
            settings = QSettings(self.__current_path + '/mywallet.conf', QSettings.IniFormat)
        settings.beginGroup(self.MAIN_SETTINGS)
        settings.setValue('size', self.size())
        settings.setValue('position', self.pos())
        settings.setValue('path', self.__current_path)
        settings.setValue('wallet_name', self.__wallet_name)
        settings.endGroup()

    def close(self):
        print('close')
        self.write_settings()
        super().close()

    # Слот закрытия приложения
    @pyqtSlot()
    def on_exit(self):
        print('on_exit')
        self.close()

    # Слот настроек
    @pyqtSlot()
    def on_settings(self):
        dialog = SettingsDialog(self.__current_path, self.__wallet_name)
        dialog.exec()

    # Слот окрытия кошелька
    @pyqtSlot()
    def on_open_wallet(self):
        file_name = QFileDialog.getOpenFileName(self, self.tr('MyWallet', 'Choose file'),
                                                QDir.current().path(),
                                                self.tr('MyWallet', 'XML-files (*.xml)'))[0]
        # WriteXml() call
        self.__current_path = QFileInfo(file_name).dir().path()
        self.__wallet_name = QFileInfo(file_name).fileName()
        print(self.__current_path, self.__wallet_name)
        # ReadXml() call
