#!/usr/bin/evn python3
__author__ = 'dimv36'

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator
from modules.mywallet import MyWallet


if __name__ == '__main__':

    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load('ts/pymywallet_RU')
    app.installTranslator(translator)

    w = MyWallet()
    w.show()

    sys.exit(app.exec())
