__author__ = 'dimv36'
from lxml import etree
from enum import Enum

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import QCoreApplication, pyqtSlot, Qt
from PyQt5.QtGui import QColor, QPen
from qcustomplot.qcustomplot import QCPBars, QCP

from modules.ui.ui_statisticdialog import Ui_StatisticDialog


class _StatisticItemType(Enum):
    ROOT = QTreeWidgetItem.UserType
    ITEM_YEAR = QTreeWidgetItem.UserType + 1
    ITEM_MONTH = QTreeWidgetItem.UserType + 2


class _MonthName(Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12

    @classmethod
    def from_string(cls, name):
        for value in cls._member_map_.values():
            if value.name == name:
                return value


class StatisticDialog(QDialog, Ui_StatisticDialog):
    def __init__(self, wallet_root):
        super().__init__()
        self.setupUi(self)
        self.__incoming = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__expense = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__loan = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__debt = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__init_plottable()
        self.__create_statistic_items(wallet_root)
        self.__init_signal_slots()

    def __init_plottable(self):
        pen = QPen()
        pen.setWidth(1.2)
        # incoming settings
        self._graphic.addPlottable(self.__incoming)
        self.__incoming.setName(QCoreApplication.translate('StatisticDialog', 'incoming'))
        pen.setColor(QColor(255, 131, 0))
        self.__incoming.setPen(pen)
        self.__incoming.setBrush(QColor(255, 131, 0, 50))
        # expense settings
        self._graphic.addPlottable(self.__expense)
        self.__expense.setName(QCoreApplication.translate('StatisticDialog', 'expense'))
        pen.setColor(QColor(1, 92, 192))
        self.__expense.setPen(pen)
        self.__expense.setBrush(QColor(1, 92, 191, 50))
        # loan settings
        self._graphic.addPlottable(self.__loan)
        self.__loan.setName(QCoreApplication.translate('StatisticDialog', 'loan'))
        pen.setColor(QColor(150, 222, 0))
        self.__loan.setPen(pen)
        self.__loan.setBrush(QColor(150, 222, 0, 70))
        # debt settings
        self._graphic.addPlottable(self.__debt)
        self.__debt.setName(QCoreApplication.translate('StatisticDialog', 'debt'))
        # legend
        self._graphic.legend.setVisible(True)
        self._graphic.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignTop | Qt.AlignHCenter)
        self._graphic.legend.setBrush(QColor(255, 255, 255, 200))
        legend_pen = QPen()
        legend_pen.setColor(QColor(130, 130, 130, 200))
        self._graphic.legend.setBorderPen(legend_pen)
        self._graphic.setInteractions(QCP.iRangeDrag or QCP.iRangeZoom)

    def __init_signal_slots(self):
        self._periods.itemClicked.connect(self.__on_item_clicked)

    @pyqtSlot(QTreeWidgetItem)
    def __on_item_clicked(self, item):
        print('item clicked: item %s' % (str(item)))
        if item.type() == _StatisticItemType.ROOT.value:
            print('ROOT')
        elif item.type() == _StatisticItemType.ITEM_YEAR.value:
            print('YEAR')
        elif item.type() == _StatisticItemType.ITEM_MONTH.value:
            print('MONTH')
            self.__make_month_statistic(item)

    def __create_statistic_items(self, wallet_root):
        root_item = QTreeWidgetItem(self._periods, _StatisticItemType.ROOT.value)
        root_item.setText(0, 'mywallet')
        years = wallet_root.findall('year')
        for year in years:
            year_item = QTreeWidgetItem(root_item, _StatisticItemType.ITEM_YEAR.value)
            year_item.setText(0, year.attrib['value'])
            months = year.findall('month')
            for month in months:
                month_item = QTreeWidgetItem(year_item, _StatisticItemType.ITEM_MONTH.value)
                long_month_name = _MonthName(int(month.attrib['value'])).name
                month_item.setText(0, QCoreApplication.translate('StatisticDialog', long_month_name))
        self._periods.expandAll()

    def __make_month_statistic(self, item):
        year = int(item.parent().text(0))
        month = _MonthName.from_string(item.text(0)).value
        print(month, year)