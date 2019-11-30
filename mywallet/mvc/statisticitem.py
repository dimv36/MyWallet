__author__ = 'dimv36'
from enum import Enum


class StatisticItemType(Enum):
    ROOT = 0
    YEAR = 1
    MONTH = 2


class StatisticItemData:
    def __init__(self, item_type, name, translated_name=None):
        self.type = item_type
        self.name = name
        self.translated_name = translated_name

    def __repr__(self):
        return 'StatisticItemData: Type: %s\n' \
               'Name: %s\n' \
               'Translated name: %s\n' % (self.type, self.name, self.translated_name)

    def __str__(self):
        return self.__repr__()


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

    def child_count(self):
        return len(self.__child_items)

    def name(self):
        return self.__statistic_item_data.name

    def translated_name(self):
        if not self.__statistic_item_data.translated_name:
            return self.__statistic_item_data.name
        return None

    def type(self):
        return self.__statistic_item_data.type

    def insert_child(self, item):
        self.__child_items.append(item)

    def row(self):
        if self.__parent:
            return self.__parent.childs().index(self)
        return 0

    def parent(self):
        return self.__parent

    def childs(self):
        return self.__child_items

    def remove_child(self, position):
        if position < 0 or position > len(self.__child_items):
            raise StatisticItemException('Unexpected position: %d' % position)
        del self.__child_items[position]
