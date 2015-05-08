#!/usr/bin/python3
__author__ = 'dimv36'

import sys
from PyQt5.QtWidgets import QApplication
from modules.mywallet import MyWallet


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = MyWallet()
    w.show()

    sys.exit(app.exec())
