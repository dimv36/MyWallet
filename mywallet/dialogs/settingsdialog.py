__author__ = 'dimv36'
from PySide2.QtWidgets import QDialog, QFileDialog
from PySide2.QtCore import QDir
from mywallet.ui.ui_settingsdialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    DEFAULT_WALLET_NAME = 'wallet.db'

    def __init__(self, directory, wallet_name=DEFAULT_WALLET_NAME):
        super().__init__()
        self.setupUi(self)
        self._directory.setText(directory)
        self._wallet_name.setText(wallet_name)

        # Подключаем необходимые сигналы к слотам
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self._directory_button.clicked.connect(self.__on_directory_clicked)

    def directory(self):
        directory = self._directory.text()
        if not directory.endswith('/'):
            directory += '/'
        return directory

    def wallet_name(self):
        return self._wallet_name.text()

    def __on_directory_clicked(self):
        new_directory = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Open directory'),
                                                         QDir.current().path())
        if new_directory:
            self._directory.setText(new_directory)
