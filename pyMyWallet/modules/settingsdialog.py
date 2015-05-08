__author__ = 'dimv36'
from PyQt5.QtWidgets import QDialog

from ui.ui_settingsdialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    DEFAULT_WALLET_NAME = 'wallet.xml'

    def __init__(self, directory, wallet_name=DEFAULT_WALLET_NAME):
        super().__init__()
        self.setupUi(self)
        self.__directory = directory
        self.__wallet_name = wallet_name

    def directory(self):
        return self.__directory

    def wallet_name(self):
        return self.__wallet_name