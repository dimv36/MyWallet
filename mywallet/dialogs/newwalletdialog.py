__author__ = 'dimv36'
from PySide2.QtCore import QCoreApplication, QDir, Slot
from PySide2.QtWidgets import QDialog, QFileDialog
from mywallet.ui.ui_newwalletdialog import Ui_NewWalletDialog


class NewWalletDialog(QDialog, Ui_NewWalletDialog):

    def __init__(self, directory):
        super().__init__()
        self.setupUi(self)
        # Делаем кнопку Ok неактивной
        self._button_box.button(self._button_box.Ok).setEnabled(False)
        # Подключаем сигналы к слотам
        self.__init_signal_slots()

        self._edit_directory.setText(directory)

    def __init_signal_slots(self):
        self._button_directory.clicked.connect(self.__on_directory_triggered)
        self._edit_wallet.textChanged.connect(self.__on_wallet_name_changed)

    @Slot()
    def __on_directory_triggered(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     QCoreApplication.translate('NewWalletDialog', 'Choose directory'),
                                                     QDir.current().path())
        if directory:
            self._edit_directory.setText(directory)

    @Slot(str)
    def __on_wallet_name_changed(self, text):
        self._button_box.button(self._button_box.Ok).setEnabled(text is not None)

    def wallet_name(self):
        return self._edit_wallet.text()

    def directory(self):
        directory = self._edit_directory.text()
        if not directory.endswith('/'):
            directory += '/'
        return directory
