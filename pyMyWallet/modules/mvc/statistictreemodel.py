__author__ = 'dimv36'
from PyQt5.QtCore import QAbstractItemModel, Qt, QCoreApplication
from PyQt5.QtCore import QModelIndex
from .statisticitem import *


class StatisticTreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__root = StatisticTreeItem(StatisticItemData(StatisticItemType.ROOT,
                                                          'Statistic periods',
                                                          QCoreApplication.translate('StatisticTreeModel',
                                                                                     'Statistic periods')))

    def columnCount(self, parent_index=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if not role == Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.translated_name()

    def flags(self, index):
        if not index.isValid():
            return 0
        return super().flags(index)

    def headerData(self, section=None, orientation=None, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__root.translated_name()
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

    def root(self):
        return self.__root

    def parent(self, index=None):
        if not index.isValid():
            return QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.__root:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent_index=None, *args, **kwargs):
        parent_item = None
        if not parent_index.isValid():
            parent_item = self.__root
        else:
            parent_item = parent_index.internalPointer()
        return parent_item.child_count()

    def item_by_indexes(self, item_index, parent_index):
        if parent_index.data() is None:
            return self.__root.child(item_index.row())
        else:
            return self.__root.child(parent_index.row()).child(item_index.row())
