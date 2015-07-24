__author__ = 'dimv36'
from enum import Enum

class StatisticTreeItemType(Enum):
    TYPE = 0
    NAME = 1
    TRANSLATED_NAME = 2


class StatisticItemData:
    def __init__(self, item_type, name, translated_name):
        self.type = item_type
        self.name = name
        self.translated_name = translated_name


class StatisticItemException(Exception):
    pass


class StatisticTreeItem:
    def __init__(self, statistic_item_data, parent=None):
        self.__statistic_item_data = statistic_item_data
        self.__parent = parent
        self.__child_items = []

    def child(self, number):
        try:
            return self.__child_items[number]
        except KeyError:
            return None

    def column_count(self):
        print('StatisticTreeItem: count: %d' % len(self.__statistic_item_data))
        return len(self.__statistic_item_data)

    def child_count(self):
        return len(self.__child_items)

    def data(self, column):
        if column == StatisticTreeItemType.TYPE.value:
            return self.__statistic_item_data.type
        elif column == StatisticTreeItemType.NAME.value:
            return self.__statistic_item_data.name
        elif column == StatisticTreeItemType.TRANSLATED_NAME.value:
            return self.__statistic_item_data.translated_name
        else:
            raise StatisticItemException('Unexpected column number: %d' % column)

    def insert_children(self, position, item):
        if position < 0 or position > len(self.__child_items):
            raise StatisticItemException('Unexpected position: %d' % position)
        self.__child_items.append(item)

    def parent(self):
        return self.__parent

    def remove_children(self, position):
        if position < 0 or position > len(self.__child_items):
            raise StatisticItemException('Unexpected position: %d' % position)
        del self.__child_items[position]

    def child_number(self):
        return len(self.__child_items)

    def set_data(self, column, value):
        if column < StatisticTreeItemType.TYPE.value or column > StatisticTreeItemType.TRANSLATED_NAME.value:
            raise StatisticItemException('Unexpected column: %d' % column)
        if column == StatisticTreeItemType.TYPE.value:
            self.__statistic_item_data.type = value
        elif column == StatisticTreeItemType.NAME.value:
            self.__statistic_item_data.name = value
        elif column == StatisticTreeItemType.TRANSLATED_NAME.value:
            self.__statistic_item_data.translated_name = value
