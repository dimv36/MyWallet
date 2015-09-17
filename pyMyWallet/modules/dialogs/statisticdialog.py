__author__ = 'dimv36'
from enum import Enum

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt, QCoreApplication, QDate
from PyQt5.QtGui import QColor, QPen
from qcustomplot.qcustomplot import QCPBars, QCPBarsGroup, QCP, QCPScatterStyle

from modules.mvc.statistictreemodel import StatisticTreeItem, StatisticItemType, StatisticItemData, StatisticTreeModel
from modules.ui.ui_statisticdialog import Ui_StatisticDialog


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

    @staticmethod
    def translated_names(number):
        if number == _MonthName.January.value:
            return QCoreApplication.translate('_MonthName', 'January')
        elif number == _MonthName.February.value:
            return QCoreApplication.translate('_MonthName', 'February')
        elif number == _MonthName.March.value:
            return QCoreApplication.translate('_MonthName', 'March')
        elif number == _MonthName.April.value:
            return QCoreApplication.translate('_MonthName', 'April')
        elif number == _MonthName.May.value:
            return QCoreApplication.translate('_MonthName', 'May')
        elif number == _MonthName.June.value:
            return QCoreApplication.translate('_MonthName', 'June')
        elif number == _MonthName.July.value:
            return QCoreApplication.translate('_MonthName', 'July')
        elif number == _MonthName.August.value:
            return QCoreApplication.translate('_MonthName', 'August')
        elif number == _MonthName.September.value:
            return QCoreApplication.translate('_MonthName', 'September')
        elif number == _MonthName.October.value:
            return QCoreApplication.translate('_MonthName', 'October')
        elif number == _MonthName.November.value:
            return QCoreApplication.translate('_MonthName', 'November')
        elif number == _MonthName.December.value:
            return QCoreApplication.translate('_MonthName', 'December')


class StatisticDialog(QDialog, Ui_StatisticDialog):
    class Bars:
        def __init__(self, customplot, width=None):
            self.__graphic = customplot
            self.balance_at_start = QCPBars(customplot.xAxis, customplot.yAxis)
            self.incoming = QCPBars(customplot.xAxis, customplot.yAxis)
            self.expense = QCPBars(customplot.xAxis, customplot.yAxis)
            self.savings = QCPBars(customplot.xAxis, customplot.yAxis)
            self.loan = QCPBars(customplot.xAxis, customplot.yAxis)
            self.debt = QCPBars(customplot.xAxis, customplot.yAxis)
            self.balance_at_end = QCPBars(customplot.xAxis, customplot.yAxis)
            self.__width = width
            self.__make_legend()

        def __make_legend(self):
            pen = QPen()
            pen.setWidth(1.2)
            # add bars to qcustomplot widget
            self.__graphic.addPlottable(self.balance_at_start)
            self.__graphic.addPlottable(self.incoming)
            self.__graphic.addPlottable(self.expense)
            self.__graphic.addPlottable(self.savings)
            self.__graphic.addPlottable(self.loan)
            self.__graphic.addPlottable(self.debt)
            self.__graphic.addPlottable(self.balance_at_end)
            # Make names
            self.balance_at_start.setName(QCoreApplication.translate('Bars', 'Balance\nat start of month'))
            self.incoming.setName(QCoreApplication.translate('Bars', 'Incoming'))
            self.expense.setName(QCoreApplication.translate('Bars', 'Expense'))
            self.savings.setName(QCoreApplication.translate('Bars', 'Savings'))
            self.loan.setName(QCoreApplication.translate('Bars', 'Loan'))
            self.debt.setName(QCoreApplication.translate('Bars', 'Debt'))
            self.balance_at_end.setName(QCoreApplication.translate('Bars', 'Balance\nat end of month'))
            # Colors
            # balance at start
            pen.setColor(QColor(255, 100, 0))
            self.balance_at_start.setPen(pen)
            self.balance_at_start.setBrush(QColor(255, 100, 0, 50))
            # self.balance_at_start.setWidth(0.3)
            # incoming
            pen.setColor(QColor(255, 0, 0))
            self.incoming.setPen(pen)
            self.incoming.setBrush(QColor(255, 0, 0, 50))
            # self.incoming.setWidth(0.3)
            # expense
            pen.setColor(QColor(10, 90, 190))
            self.expense.setPen(pen)
            self.expense.setBrush(QColor(10, 90, 190, 50))
            # self.expense.setWidth(0.3)
            # savings
            pen.setColor(QColor(150, 50, 10))
            self.savings.setPen(pen)
            self.savings.setBrush(QColor(150, 90, 190, 50))
            # loan
            pen.setColor(QColor(150, 220, 70))
            self.loan.setPen(pen)
            self.loan.setBrush(QColor(150, 220, 70, 50))
            # self.loan.setWidth(0.3)
            # debt
            pen.setColor(QColor(180, 50, 250))
            self.loan.setPen(pen)
            self.debt.setBrush(QColor(180, 50, 250, 50))
            # self.debt.setWidth(0.3)
            # balance at end
            pen.setColor(QColor(250, 250, 50))
            self.balance_at_end.setPen(pen)
            self.balance_at_end.setBrush(QColor(250, 250, 50, 50))
            # self.balance_at_end.setWidth(0.3)
            if self.__width:
                self.balance_at_start.setWidth(self.__width)
                self.incoming.setWidth(self.__width)
                self.expense.setWidth(self.__width)
                self.savings.setWidth(self.__width)
                self.loan.setWidth(self.__width)
                self.debt.setWidth(self.__width)
                self.balance_at_end.setWidth(self.__width)

    def __init__(self, model):
        super().__init__()
        self.setupUi(self)
        self.__model = model
        self.__graphics = []
        self.__bar_group = QCPBarsGroup(self._graphic)
        self.__bar_groups = []
        self.__statistic_model = StatisticTreeModel()
        self._statistic_view.setModel(self.__statistic_model)
        self.__init_plottable()
        self.__create_statistic_items()
        self.__init_signal_slots()

    def __init_plottable(self):
        # Axis settings
        grid_pen = QPen()
        grid_pen.setStyle(Qt.SolidLine)
        grid_pen.setColor(QColor(0, 0, 0, 25))
        self._graphic.yAxis.grid().setSubGridPen(grid_pen)
        self._graphic.xAxis.setSubTickCount(0)
        self._graphic.yAxis.setLabel(QCoreApplication.translate('StatisticDialog', 'rubles'))
        # legend
        self._graphic.legend.setVisible(True)
        self._graphic.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignRight | Qt.AlignTop)
        self._graphic.legend.setBrush(QColor(255, 255, 255, 200))
        legend_pen = QPen()
        legend_pen.setColor(QColor(130, 130, 130, 200))
        self._graphic.legend.setBorderPen(legend_pen)
        flags = QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables
        self._graphic.setInteractions(QCP.Interactions(flags))

    def __init_signal_slots(self):
        self._statistic_view.clicked.connect(self.__on_item_clicked)

    @pyqtSlot(QTreeWidgetItem)
    def __on_item_clicked(self, index):
        if index.isValid():
            parent_index = index.parent()
            item = self.__statistic_model.item_by_indexes(index, parent_index)
            if item.type() == StatisticItemType.YEAR:
                self.__make_year_statistic(item)
            elif item.type() == StatisticItemType.MONTH:
                self.__make_month_statistic(item)

    def __create_statistic_items(self):
        items = self.__model.get_statistic_periods_items()
        for year in items.keys():
            year_item_data = StatisticItemData(StatisticItemType.YEAR, year)
            year_item = StatisticTreeItem(year_item_data, self.__statistic_model.root())
            self.__statistic_model.root().insert_child(year_item)
            for month in items[year]:
                month_item_data = StatisticItemData(StatisticItemType.MONTH,
                                                    _MonthName(int(month)).name,
                                                    _MonthName.translated_names(month))
                month_item = StatisticTreeItem(month_item_data, year_item)
                year_item.insert_child(month_item)
        self._statistic_view.expandAll()

    def __make_month_statistic(self, month_item):
        if self.__graphics or self._graphic.graphCount():
            self._graphic.clearPlottables()
            self.__graphics.clear()
            self._graphic.clearGraphs()
        year_item = month_item.parent()
        year = int(year_item.name())
        month = _MonthName.from_string(month_item.name()).value
        month_data = self.__model.get_wallet_info(QDate(year, month, 1))
        self._graphic.xAxis.setTicks(False)
        self._graphic.xAxis.setLabel(QCoreApplication.translate('StatisticDialog',
                                                                '%s %s') % (month_item.translated_name(),
                                                                            year_item.name()))
        self._graphic.yAxis.setRange(-100, max(month_data.balance_at_start, month_data.incoming,
                                            month_data.expense, month_data.loan,
                                            month_data.debt, month_data.balance_at_end) + 5000)
        self._graphic.xAxis.setRange(0.5, 7)
        bars = self.Bars(self._graphic)
        self.__graphics.append(bars)
        self.__bar_group.append(bars.balance_at_start)
        self.__bar_group.append(bars.incoming)
        self.__bar_group.append(bars.expense)
        self.__bar_group.append(bars.savings)
        self.__bar_group.append(bars.loan)
        self.__bar_group.append(bars.debt)
        self.__bar_group.append(bars.balance_at_end)
        bars.balance_at_start.setData([4], [month_data.balance_at_start])
        bars.incoming.setData([4], [month_data.incoming])
        bars.expense.setData([4], [month_data.expense])
        bars.savings.setData([4], [month_data.savings])
        bars.loan.setData([4], [month_data.loan])
        bars.debt.setData([4], [month_data.debt])
        bars.balance_at_end.setData([4], [month_data.balance_at_end])
        self._graphic.replot()

    def __make_year_statistic(self, year_item):
        if self.__graphics or self._graphic.graphCount():
            self._graphic.clearPlottables()
            self.__graphics.clear()
            self.__bar_groups.clear()
        year = int(year_item.name())
        balance_at_start_data = []
        incoming_data = []
        expense_data = []
        savings_data = []
        saving_aggregate = float()
        loan_data = []
        debt_data = []
        balance_at_end_data = []
        labels = ['']
        datax = [i + 1 for i in range(0, year_item.child_count())]
        self._graphic.xAxis.setLabel(QCoreApplication.translate('StatisticDialog',
                                                                'Statistic by %s  year') % str(year))
        for i in range(0, year_item.child_count()):
            month_item = year_item.child(i)
            labels.append('%s\n%s' % (month_item.translated_name(), str(year)))
            month = _MonthName.from_string(month_item.name()).value
            month_data = self.__model.get_wallet_info(QDate(year, month, 1))
            balance_at_start_data.append(month_data.balance_at_start)
            incoming_data.append(month_data.incoming)
            expense_data.append(month_data.expense)
            saving_aggregate += month_data.savings
            savings_data.append(saving_aggregate)
            loan_data.append(month_data.loan)
            debt_data.append(month_data.debt)
            balance_at_end_data.append(month_data.balance_at_end)
        self._graphic.xAxis.setAutoTickLabels(False)
        self._graphic.xAxis.setRange(min(datax) - 0.1, max(datax) + 0.1)
        self._graphic.xAxis.setAutoSubTicks(False)
        self._graphic.xAxis.setAutoTickStep(False)
        self._graphic.xAxis.setTicks(True)
        self._graphic.xAxis.setSubTickCount(4)
        self._graphic.xAxis.setTickStep(1)
        self._graphic.yAxis.setRange(-100, max(max(balance_at_start_data), max(incoming_data),
                                               max(expense_data), max(savings_data),
                                               max(loan_data), max(debt_data),
                                               max(balance_at_end_data)) + 5000)
        for i in range(0, 7):
            self._graphic.addGraph()
        self._graphic.xAxis.setTickVectorLabels(labels)
        self._graphic.xAxis.setNumberPrecision(0)
        self._graphic.graph(0).setData(datax, balance_at_start_data)
        self._graphic.graph(0).setName(QCoreApplication.translate('StatisticDialog', 'Balance\nat start of month'))
        self._graphic.graph(0).setPen(QPen(Qt.red))
        self._graphic.graph(0).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 8))
        self._graphic.graph(1).setData(datax, incoming_data)
        self._graphic.graph(1).setName(QCoreApplication.translate('StatisticDialog', 'Incoming'))
        self._graphic.graph(1).setPen(QPen(Qt.blue))
        self._graphic.graph(1).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCrossSquare, 8))
        self._graphic.graph(2).setData(datax, expense_data)
        self._graphic.graph(2).setName(QCoreApplication.translate('StatisticDialog', 'Expense'))
        self._graphic.graph(2).setPen(QPen(Qt.green))
        self._graphic.graph(2).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssStar, 8))
        self._graphic.graph(3).setData(datax, savings_data)
        self._graphic.graph(3).setName(QCoreApplication.translate('StatisticDialog', 'Savings'))
        self._graphic.graph(3).setPen(QPen(Qt.green))
        self._graphic.graph(3).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCross, 8))
        self._graphic.graph(4).setData(datax, loan_data)
        self._graphic.graph(4).setName(QCoreApplication.translate('StatisticDialog', 'Loan'))
        self._graphic.graph(4).setPen(QPen(Qt.yellow))
        self._graphic.graph(4).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssDisc, 8))
        self._graphic.graph(5).setData(datax, debt_data)
        self._graphic.graph(5).setName(QCoreApplication.translate('StatisticDialog', 'Debt'))
        self._graphic.graph(5).setPen(QPen(Qt.gray))
        self._graphic.graph(5).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssDiamond, 8))
        self._graphic.graph(6).setData(datax, balance_at_end_data)
        self._graphic.graph(6).setPen(QPen(Qt.darkRed))
        self._graphic.graph(6).setName(QCoreApplication.translate('StatisticDialog', 'Balance\nat end of month'))
        self._graphic.graph(6).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCrossCircle, 8))
        self._graphic.replot()
