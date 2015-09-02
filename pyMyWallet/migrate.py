#!/usr/bin/env python3
__author__ = 'dimv36'
from sys import argv
from lxml import etree
from sqlite3 import connect
from os.path import exists, isfile, basename, dirname


if __name__ == '__main__':
    if not len(argv) == 2:
        print('Need XML file to migrate')
        exit(1)
    xml_path = str(argv[1])
    db_path = dirname(xml_path) + '/' + basename(xml_path).split('.')[0] + '.db'
    if not exists(xml_path):
        print('XML path %s does not exists' % xml_path)
        exit(1)
    elif not isfile(xml_path):
        print('%s is not file')
        exit(1)
    connection = connect(db_path)
    if not connection:
        print('Could not connect to database %s' % db_path)
        exit(1)
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS wallet_data;')
    cursor.execute('DROP TABLE IF EXISTS wallet_month_data;')
    cursor.execute('CREATE TABLE IF NOT EXISTS wallet_data(ID INTEGER PRIMARY KEY,'
                   'day INTEGER,'
                   'month INTEGER,'
                   'year INTEGER,'
                   'incoming REAL,'
                   'expense REAL,'
                   'saving REAL,'
                   'loan REAL,'
                   'debt REAL,'
                   'description TEXT);')
    cursor.execute('CREATE TABLE IF NOT EXISTS wallet_month_data(ID INTEGER PRIMARY KEY,'
                   'month INTEGER,'
                   'year INTEGER,'
                   'balance_at_start REAL,'
                   'balance_at_end REAL);')
    tree = etree.parse(xml_path)
    if tree:
        root = tree.getroot()
        years = root.findall('year')
        for year in years:
            months = year.findall('month')
            for month in months:
                balance_at_start = float(month.attrib['rest'])
                incomings_sum = float()
                expenses_sum = float()
                savings_sum = float()
                loans_sum = float()
                debt_sum = float()
                days = month.findall('day')
                month_value = int(month.attrib['value'])
                year_value = int(year.attrib['value'])
                for day in days:
                    incomings = day.findall('incoming')
                    day_value = int(day.attrib['value'])
                    for incoming in incomings:
                        value = float(incoming.attrib['value'])
                        cursor.execute('INSERT INTO wallet_data VALUES(NULL, %d, %d, %d, '
                                       '%d, NULL, NULL, NULL, NULL, \'%s\')' %
                                       (day_value,
                                        month_value,
                                        year_value,
                                        value,
                                        incoming.attrib['description']))
                        incomings_sum += value
                    expenses = day.findall('expense')
                    for expense in expenses:
                        value = float(expense.attrib['value'])
                        cursor.execute('INSERT INTO wallet_data VALUES(NULL, %d, %d, %d, '
                                       'NULL, %d, NULL, NULL, NULL, \'%s\')' %
                                       (day_value,
                                        month_value,
                                        year_value,
                                        value,
                                        expense.attrib['description']))
                        expenses_sum += value
                    savings = day.findall('saving')
                    for saving in savings:
                        value = float(saving.attrib['value'])
                        cursor.execute('INSERT INTO wallet_data VALUES(NULL, %d, %d, %d, '
                                       'NULL, NULL, %d, NULL, NULL, \'%s\')' %
                                       (day_value,
                                        month_value,
                                        year_value,
                                        value,
                                        saving.attrib['description']))
                        savings_sum += value
                    loans = day.findall('loan')
                    for loan in loans:
                        value = float(loan.attrib['value'])
                        cursor.execute('INSERT INTO wallet_data VALUES(NULL, %d, %d, %d, '
                                       'NULL, NULL, NULL, %d, NULL, \'%s\')' %
                                       (day_value,
                                        month_value,
                                        year_value,
                                        value,
                                        loan.attrib['description']))
                        loans_sum += value
                    debts = day.findall('debt')
                    for debt in debts:
                        value = float(debt.attrib['value'])
                        cursor.execute('INSERT INTO wallet_data VALUES(NULL, %d, %d, %d, '
                                       'NULL, NULL, NULL, NULL, %d, \'%s\')' %
                                       (day_value,
                                        month_value,
                                        year_value,
                                        value,
                                        debt.attrib['description']))
                        debt_sum += value
                balance_at_end = balance_at_start + incomings_sum - expenses_sum + savings_sum + debt_sum
                cursor.execute('INSERT INTO wallet_month_data VALUES(NULL, %d, %d, %d, %d)' % (month_value,
                                                                                               year_value,
                                                                                               balance_at_start,
                                                                                               balance_at_end))
        connection.commit()
