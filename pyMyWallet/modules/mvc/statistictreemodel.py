__author__ = 'dimv36'
from PyQt5.QtCore import QAbstractItemModel, Qt
from .statisticitem import StatisticTreeItem


class StatisticTreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.__headers = ['Statistic Periods']
        self.__root = StatisticTreeItem(self.__headers[0])
        self.__setup_model_data(data, self.__root)

    def columnCount(self, parent_index=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if not role == Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0
        return super().flags(index)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__root.data(section)
        return None

    def index(self, row, column, parent_index=None, *args, **kwargs):
        if not self.hasIndex(row, column, parent_index):
            return None
        parent_item = None
        if not parent_index.isValid():
            parent_item = self.__root
        else:
            parent_item = parent_index.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return None

    def parent(self, index=None):
        if not index.isValid():
            return None
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.__root:
            return None
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent_index=None, *args, **kwargs):
        parent_item = None
        if parent_item.column() > 0:
            return 0
        if not parent_index.isValid():
            parent_item = self.__root
        else:
            parent_item = parent_index.internalPointer()
        return parent_item.child_count()

    @staticmethod
    def __setup_model_data(lines, parent):
        parents = []
        indentations = []
        parents.append(parent)
        indentations.append(0)
        number = 0

        while number < len(lines):
            position = 0
            line = lines[number]
            if position > indentations[-1]:
                if parents[-1].child(parents[-1].child_count() - 1):
                    indentations.append(position)
            else:
                while position < indentations[-1] and len(parents) > 0:
                    parents.pop()
                    indentations.pop()
            parents[-1].append_child(StatisticTreeItem(line, parents[-1]))
            number += 1
