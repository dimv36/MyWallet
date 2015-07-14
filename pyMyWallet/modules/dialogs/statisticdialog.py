__author__ = 'dimv36'
from lxml import etree
from enum import Enum

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import QCoreApplication, pyqtSlot, Qt
from PyQt5.QtGui import QColor, QPen
from qcustomplot.qcustomplot import QCPBars, QCPBarsGroup, QCP

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
    def __init__(self):
        self.balance_at_start = float()
        self.incoming = float()
        self.expense = float()
        self.loan = float()
        self.debt = float()
        self.balance_at_end = float()

    def __str__(self):
        return 'balance at start: %d ' \
               'incoming: %d ' \
               'expense: %d ' \
               'loan: %d ' \
               'debt: %d ' \
               'balance at end: %d' % (self.balance_at_start, self.incoming,
                                       self.expense, self.loan,
                                       self.debt, self.balance_at_end)

    def make_balance_at_end(self):
        self.balance_at_end = self.balance_at_start + self.incoming - self.expense + self.loan - self.debt


class StatisticDialog(QDialog, Ui_StatisticDialog):
    BALANCE_AT_START = QCoreApplication.translate('StatisticDialog', 'balance \nat start of month')
    INCOMING = QCoreApplication.translate('StatisticDialog', 'incoming')
    EXPENSE = QCoreApplication.translate('StatisticDialog', 'expense')
    LOAN = QCoreApplication.translate('StatisticDialog', 'loan')
    DEBT = QCoreApplication.translate('StatisticDialog', 'debt')
    BALANCE_AT_END = QCoreApplication.translate('StatisticDialog', 'balance \nat end of month')

    class Bars:
        def __init__(self, customplot):
            self.__graphic = customplot
            self.balance_at_start = QCPBars(customplot.xAxis, customplot.yAxis)
            self.incoming = QCPBars(customplot.xAxis, customplot.yAxis)
            self.expense = QCPBars(customplot.xAxis, customplot.yAxis)
            self.loan = QCPBars(customplot.xAxis, customplot.yAxis)
            self.debt = QCPBars(customplot.xAxis, customplot.yAxis)
            self.balance_at_end = QCPBars(customplot.xAxis, customplot.yAxis)
            self.__make_legend()

        def __make_legend(self):
            pen = QPen()
            pen.setWidth(1.2)
            # add bars to qcustomplot widget
            self.__graphic.addPlottable(self.balance_at_start)
            self.__graphic.addPlottable(self.incoming)
            self.__graphic.addPlottable(self.expense)
            self.__graphic.addPlottable(self.loan)
            self.__graphic.addPlottable(self.debt)
            self.__graphic.addPlottable(self.balance_at_end)
            # Make names
            self.balance_at_start.setName(StatisticDialog.BALANCE_AT_START)
            self.incoming.setName(StatisticDialog.INCOMING)
            self.expense.setName(StatisticDialog.EXPENSE)
            self.loan.setName(StatisticDialog.LOAN)
            self.debt.setName(StatisticDialog.DEBT)
            self.balance_at_end.setName(StatisticDialog.BALANCE_AT_END)
            # Colors
            # balance at start
            pen.setColor(QColor(255, 100, 0))
            self.balance_at_start.setPen(pen)
            self.balance_at_start.setBrush(QColor(255, 100, 0, 50))
            self.balance_at_start.setWidth(0.3)
            # incoming
            pen.setColor(QColor(255, 0, 0))
            self.incoming.setPen(pen)
            self.incoming.setBrush(QColor(255, 0, 0, 50))
            self.incoming.setWidth(0.3)
            # expense
            pen.setColor(QColor(10, 90, 190))
            self.expense.setPen(pen)
            self.expense.setBrush(QColor(10, 90, 190, 50))
            self.expense.setWidth(0.3)
            # loan
            pen.setColor(QColor(150, 220, 70))
            self.loan.setPen(pen)
            self.loan.setBrush(QColor(150, 220, 70, 50))
            self.loan.setWidth(0.3)
            # debt
            pen.setColor(QColor(180, 50, 250))
            self.loan.setPen(pen)
            self.debt.setBrush(QColor(180, 50, 250, 50))
            self.debt.setWidth(0.3)
            # balance at end
            pen.setColor(QColor(250, 250, 50))
            self.balance_at_end.setPen(pen)
            self.balance_at_end.setBrush(QColor(250, 250, 50, 50))
            self.balance_at_end.setWidth(0.3)

    def __init__(self, wallet_root):
        super().__init__()
        self.setupUi(self)
        self.__wallet_root = wallet_root
        self.__graphics = []
        self.__bar_group = QCPBarsGroup(self._graphic)
        self.__bar_groups = []
        self.__init_plottable()
        self.__create_statistic_items()
        self.__init_signal_slots()

    def __init_plottable(self):
        # Axis settings
        self._graphic.xAxis.setAutoTicks(False)
        self._graphic.xAxis.setAutoTickLabels(False)
        self._graphic.xAxis.grid().setVisible(True)
        self._graphic.xAxis.setAutoTickStep(False)
        self._graphic.xAxis.setTickStep(1)
        self._graphic.xAxis.setSubTickCount(0)
        grid_pen = QPen()
        grid_pen.setStyle(Qt.SolidLine)
        grid_pen.setColor(QColor(0, 0, 0, 25))
        self._graphic.yAxis.grid().setSubGridPen(grid_pen)
        self._graphic.xAxis.setTickLabelRotation(60)
        # legend
        self._graphic.legend.setVisible(True)
        self._graphic.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignRight | Qt.AlignTop)
        self._graphic.legend.setBrush(QColor(255, 255, 255, 200))
        legend_pen = QPen()
        legend_pen.setColor(QColor(130, 130, 130, 200))
        self._graphic.legend.setBorderPen(legend_pen)
        self._graphic.setInteractions(QCP.iRangeDrag or QCP.iRangeZoom)
        self._graphic.xAxis.setAutoTicks(False)

    def __init_signal_slots(self):
        self._periods.itemClicked.connect(self.__on_item_clicked)

    @pyqtSlot(QTreeWidgetItem)
    def __on_item_clicked(self, item):
        if item.type() == _StatisticItemType.ROOT.value:
            pass
        elif item.type() == _StatisticItemType.ITEM_YEAR.value:
            self.__make_year_statistic(item)
        elif item.type() == _StatisticItemType.ITEM_MONTH.value:
            self.__make_month_statistic(item)

    def __create_statistic_items(self):
        root_item = QTreeWidgetItem(self._periods, _StatisticItemType.ROOT.value)
        root_item.setText(0, 'mywallet')
        if self.__wallet_root is None:
            return
        years = self.__wallet_root.findall('year')
        for year in years:
            year_item = QTreeWidgetItem(root_item, _StatisticItemType.ITEM_YEAR.value)
            year_item.setText(0, year.attrib['value'])
            months = year.findall('month')
            for month in months:
                month_item = QTreeWidgetItem(year_item, _StatisticItemType.ITEM_MONTH.value)
                long_month_name = _MonthName(int(month.attrib['value'])).name
                month_item.setText(0, QCoreApplication.translate('StatisticDialog', long_month_name))
        self._periods.expandAll()

    def __get_item_sum(self, items):
        result = float()
        if items:
            for item in items:
                result += float(item.attrib['value'])
        return result

    def __get_month_statistic(self, month, year):
        month_statistic_data = _MonthStatisticData()
        tree = etree.ElementTree(self.__wallet_root)
        month_item = tree.xpath('///year[@value=%s]/month[@value=%s]' % (str(year), str(month)))[0]
        try:
            month_statistic_data.balance_at_start = float(month_item.attrib['rest'])
        except KeyError:
            month_statistic_data.balance_at_start = float()
        incoming_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/incoming' % (str(year), str(month)))
        expense_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/expense' % (str(year), str(month)))
        load_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/loan' % (str(year), str(month)))
        debt_items = tree.xpath('///year[@value=%s]/month[@value=%s]/*/debt' % (str(year), str(month)))
        month_statistic_data.incoming = self.__get_item_sum(incoming_items)
        month_statistic_data.expense = self.__get_item_sum(expense_items)
        month_statistic_data.loan = self.__get_item_sum(load_items)
        month_statistic_data.debt = self.__get_item_sum(debt_items)
        month_statistic_data.make_balance_at_end()
        return month_statistic_data

    def __make_month_statistic(self, item):
        if self.__graphics:
            self._graphic.clearPlottables()
            self.__graphics.clear()
        year = int(item.parent().text(0))
        month = _MonthName.from_string(item.text(0)).value
        month_data = self.__get_month_statistic(month, year)
        self._graphic.xAxis.setTickVectorLabels([])
        self._graphic.yAxis.setRange(-250, max(month_data.balance_at_start, month_data.incoming,
                                            month_data.expense, month_data.loan,
                                            month_data.debt, month_data.balance_at_end) + 5000)
        self._graphic.xAxis.setRange(0, 7)
        bars = self.Bars(self._graphic)
        self.__graphics.append(bars)
        self.__bar_group.append(bars.balance_at_start)
        self.__bar_group.append(bars.incoming)
        self.__bar_group.append(bars.expense)
        self.__bar_group.append(bars.loan)
        self.__bar_group.append(bars.debt)
        self.__bar_group.append(bars.balance_at_end)
        bars.balance_at_start.setData([3], [month_data.balance_at_start])
        bars.incoming.setData([3], [month_data.incoming])
        bars.expense.setData([3], [month_data.expense])
        bars.loan.setData([3], [month_data.loan])
        bars.debt.setData([3], [month_data.debt])
        bars.balance_at_end.setData([3], [month_data.balance_at_end])
        self._graphic.replot()

    def __make_year_statistic(self, year_item):
        if self.__graphics:
            self._graphic.clearPlottables()
            self.__graphics.clear()
            self.__bar_groups.clear()
        year = int(year_item.text(0))
        self._graphic.xAxis.setRange(0, year_item.childCount() + 5)
        balance_at_start_data = []
        incoming_data = []
        expense_data = []
        loan_data = []
        debt_data = []
        balance_at_end_data = []
        datax = []
        labels = []
        for i in range(0, year_item.childCount()):
            if not datax:
                datax.append(3)
            else:
                datax.append(datax[-1] + 6)
        self._graphic.xAxis.setRange(min(datax), max(datax) + 1)
        self._graphic.yAxis.setRange(0, 150000)
        for i in range(0, year_item.childCount()):
            month_item = year_item.child(i)
            labels.append(month_item.text(0))
            month = _MonthName.from_string(month_item.text(0)).value
            month_data = self.__get_month_statistic(month, year)
            balance_at_start_data.append(month_data.balance_at_start)
            incoming_data.append(month_data.incoming)
            expense_data.append(month_data.expense)
            loan_data.append(month_data.loan)
            debt_data.append(month_data.debt)
            balance_at_end_data.append(month_data.balance_at_end)
        bars = self.Bars(self._graphic)
        self.__graphics.append(bars)
        bars.balance_at_start.setData(datax, balance_at_start_data)
        bars.incoming.setData(datax, incoming_data)
        bars.expense.setData(datax, expense_data)
        bars.loan.setData(datax, loan_data)
        bars.debt.setData(datax, debt_data)
        bars.balance_at_end.setData(datax, balance_at_end_data)
        self.__bar_group.append(bars.balance_at_start)
        self.__bar_group.append(bars.incoming)
        self.__bar_group.append(bars.expense)
        self.__bar_group.append(bars.loan)
        self.__bar_group.append(bars.debt)
        self.__bar_group.append(bars.balance_at_end)
        self._graphic.xAxis.setTickVectorLabels(labels)
        self._graphic.xAxis.setAutoTicks(False)
        self._graphic.replot()
