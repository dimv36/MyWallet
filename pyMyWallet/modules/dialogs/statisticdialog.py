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


class _MonthStatisticData:
    balance = float()
    incoming = float()
    expense = float()
    loan = float()
    debt = float()

class StatisticDialog(QDialog, Ui_StatisticDialog):
    BALANCE = QCoreApplication.translate('StatisticDialog', 'balance')
    INCOMING = QCoreApplication.translate('StatisticDialog', 'incoming')
    EXPENSE = QCoreApplication.translate('StatisticDialog', 'expense')
    LOAN = QCoreApplication.translate('StatisticDialog', 'loan')
    DEBT = QCoreApplication.translate('StatisticDialog', 'debt')

    def __init__(self, wallet_root):
        super().__init__()
        self.setupUi(self)
        self.__wallet_root = wallet_root
        self.__balance = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__incoming = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__expense = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__loan = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__debt = QCPBars(self._graphic.xAxis, self._graphic.yAxis)
        self.__init_plottable()
        self.__create_statistic_items()
        self.__init_signal_slots()

    def __init_plottable(self):
        pen = QPen()
        pen.setWidth(1.2)
        # balance settings
        self._graphic.addPlottable(self.__balance)
        self.__balance.setName(self.BALANCE)
        pen.setColor(QColor(255, 100, 0))
        self.__balance.setPen(pen)
        self.__balance.setBrush(QColor(255, 100, 0, 50))
        # incoming settings
        self._graphic.addPlottable(self.__incoming)
        self.__incoming.setName(self.INCOMING)
        pen.setColor(QColor(255, 131, 0))
        self.__incoming.setPen(pen)
        self.__incoming.setBrush(QColor(255, 131, 0, 50))
        # expense settings
        self._graphic.addPlottable(self.__expense)
        self.__expense.setName(self.EXPENSE)
        pen.setColor(QColor(1, 92, 192))
        self.__expense.setPen(pen)
        self.__expense.setBrush(QColor(1, 92, 191, 50))
        # loan settings
        self._graphic.addPlottable(self.__loan)
        self.__loan.setName(self.LOAN)
        pen.setColor(QColor(150, 222, 0))
        self.__loan.setPen(pen)
        self.__loan.setBrush(QColor(150, 222, 0, 70))
        # debt settings
        self._graphic.addPlottable(self.__debt)
        self.__debt.setName(self.DEBT)
        pen.setColor(QColor(100, 180, 0))
        self.__debt.setPen(pen)
        self.__debt.setBrush(QColor(100, 180, 0, 70))
        # legend
        self._graphic.legend.setVisible(True)
        self._graphic.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignTop | Qt.AlignHCenter)
        self._graphic.legend.setBrush(QColor(255, 255, 255, 200))
        legend_pen = QPen()
        legend_pen.setColor(QColor(130, 130, 130, 200))
        self._graphic.legend.setBorderPen(legend_pen)
        self._graphic.setInteractions(QCP.iRangeDrag or QCP.iRangeZoom)
        # Axis settings
        self._graphic.xAxis.setAutoTicks(False)
        self._graphic.xAxis.setAutoTickLabels(False)
        self._graphic.xAxis.grid().setVisible(True)
        self._graphic.xAxis.setSubTickCount(0)
        grid_pen = QPen()
        grid_pen.setStyle(Qt.SolidLine)
        grid_pen.setColor(QColor(0, 0, 0, 25))
        self._graphic.yAxis.grid().setSubGridPen(grid_pen)
        self._graphic.xAxis.setTickLabelRotation(60)

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

    def __create_statistic_items(self):
        root_item = QTreeWidgetItem(self._periods, _StatisticItemType.ROOT.value)
        root_item.setText(0, 'mywallet')
        try:
            years = self.__wallet_root.findall('year')
            for year in years:
                year_item = QTreeWidgetItem(root_item, _StatisticItemType.ITEM_YEAR.value)
                year_item.setText(0, year.attrib['value'])
                months = year.findall('month')
                for month in months:
                    month_item = QTreeWidgetItem(year_item, _StatisticItemType.ITEM_MONTH.value)
                    long_month_name = _MonthName(int(month.attrib['value'])).name
                    month_item.setText(0, QCoreApplication.translate('StatisticDialog', long_month_name))
        except AttributeError:
            pass
        self._periods.expandAll()

    def __get_item_sum(self, items):
        result = float()
        if items:
            for item in items:
                result += float(item.attrib['value'])
        return result

    def __get_month_statistic(self, month, year):
        month_statistic_data = _MonthStatisticData
        tree = etree.ElementTree(self.__wallet_root)
        month_item = tree.xpath('///year[@value=%s]/month[@value=%s]' % (str(year), str(month)))[0]
        try:
            month_statistic_data.balance = float(month_item.attrib['rest'])
        except KeyError:
            month_statistic_data.balance = float()
        incoming_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/incoming' % (str(year), str(month)))
        expense_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/expense' % (str(year), str(month)))
        load_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/loan' % (str(year), str(month)))
        debt_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/debt' % (str(year), str(month)))
        month_statistic_data.incoming = self.__get_item_sum(incoming_items)
        month_statistic_data.expense = self.__get_item_sum(expense_items)
        month_statistic_data.loan = self.__get_item_sum(load_items)
        month_statistic_data.debt = self.__get_item_sum(debt_items)
        return month_statistic_data

    def __make_month_statistic(self, item):
        year = int(item.parent().text(0))
        month = _MonthName.from_string(item.text(0)).value
        month_data = self.__get_month_statistic(month, year)
        labels = [self.BALANCE,
                  self.INCOMING,
                  self.EXPENSE,
                  self.LOAN,
                  self.DEBT]
        ticks = [i + 1 for i in range(0, len(labels))]
        self._graphic.xAxis.setTickVector(ticks)
        self._graphic.xAxis.setTickVectorLabels(labels)
        self._graphic.yAxis.setRange(0, max(month_data.balance, month_data.incoming,
                                            month_data.expense, month_data.loan,
                                            month_data.debt) + 5000)
        self._graphic.xAxis.setRange(0, len(labels) + 1)
        self.__balance.setData([1], [month_data.balance])
        self.__incoming.setData([2], [month_data.incoming])
        self.__expense.setData([3], [month_data.expense])
        self.__loan.setData([4], [month_data.loan])
        self.__debt.setData([5], [month_data.debt])
        self._graphic.replot()
