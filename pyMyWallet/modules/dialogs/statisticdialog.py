__author__ = 'dimv36'
from lxml import etree
from enum import Enum

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import QCoreApplication

from modules.ui.ui_staticsticdialog import Ui_StatisticDialog


class _StatisticItemType(Enum):
    UNDEFINED = 0
    ITEM_YEAR = 1
    ITEM_MONTH = 2


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

    def __str__(self):
        return self.name


class _StatisticTableWidgetItem(QTreeWidgetItem):
    def __init__(self, item_type=_StatisticItemType.UNDEFINED):
        super().__init__()
        self.__type = item_type

    def item_type(self):
        return self.__type


class StatisticDialog(QDialog, Ui_StatisticDialog):
    def __init__(self, wallet_root):
        super().__init__()
        self.setupUi(self)
        self.__create_statistic_items(wallet_root)

    def __create_statistic_items(self, wallet_root):
        root_item = QTreeWidgetItem(self._periods)
        root_item.setText(0, 'mywallet')
        years = wallet_root.findall('year')
        for year in years:
            year_item = QTreeWidgetItem(root_item)
            year_item.setText(0, year.attrib['value'])
            months = year.findall('month')
            for month in months:
                month_item = QTreeWidgetItem(year_item)
                long_month_name = str(_MonthName(int(month.attrib['value'])))
                month_item.setText(0, QCoreApplication.translate('StatisticDialog', long_month_name))
        self._periods.expandAll()
