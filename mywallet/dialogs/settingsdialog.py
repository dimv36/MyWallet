__author__ = 'dimv36'
from PySide2.QtWidgets import QDialog, QFileDialog
from PySide2.QtCore import QDir
from mywallet.ui.ui_settingsdialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    DEFAULT_WALLET_NAME = 'wallet.db'

    def __init__(self, directory, wallet_name=DEFAULT_WALLET_NAME):
        super().__init__()
        self.setupUi(self)
        self.directory_edit.setText(directory)
        self.wallet_edit.setText(wallet_name)

        # Подключаем необходимые сигналы к слотам
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self.directory_button.clicked.connect(self.__on_directory_clicked)

    def directory(self):
        directory = self.directory_edit.text()
        if not directory.endswith('/'):
            directory += '/'
        return directory

    def wallet_name(self):
        return self.wallet_edit.text()

    def __on_directory_clicked(self):
        new_directory = QFileDialog.getExistingDirectory(self,
                                                         self.tr('Open directory'),
                                                         QDir.current().path())
        if new_directory:
            self.directory_edit.setText(new_directory)
