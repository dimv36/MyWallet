__author__ = 'dimv36'
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QDir, QCoreApplication

from ui.ui_settingsdialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    DEFAULT_WALLET_NAME = 'wallet.xml'

    def __init__(self, directory, wallet_name=DEFAULT_WALLET_NAME):
        super().__init__()
        self.setupUi(self)
        self._directory.setText(directory)
        self._wallet_name.setText(wallet_name)

        # Подключаем необходимые сигналы к слотам
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self._directory_button.pyqtConfigure(clicked=self.__on_directory_clicked)

    def directory(self):
        directory = self._directory.text()
        if not directory.endswith('/'):
            directory += '/'
        return directory

    def wallet_name(self):
        return self._wallet_name.text()

    def __on_directory_clicked(self):
        new_directory = QFileDialog.getExistingDirectory(self,
                                                         QCoreApplication.translate('SettingsDialog', 'Open directory'),
                                                         QDir.current().path())
        if new_directory:
            self._directory.setText(new_directory)