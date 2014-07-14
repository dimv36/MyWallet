#-------------------------------------------------
#
# Project created by QtCreator 2014-02-02T13:32:05
#
#-------------------------------------------------

QT       += core gui xmlpatterns xml

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MyWallet
TEMPLATE = app


SOURCES += main.cpp\
        mywallet.cpp \
    adddialog.cpp \
    settingsdialog.cpp \
    restmonthdialog.cpp \
    editingtabledelegate.cpp \
    tablewidget.cpp

HEADERS  += mywallet.h \
    adddialog.h \
    settingsdialog.h \
    restmonthdialog.h \
    editingtabledelegate.h \
    tablewidget.h

FORMS    += mywallet.ui \
    adddialog.ui \
    settingsdialog.ui \
    restmonthdialog.ui \
    tablewidget.ui

RESOURCES += \
    files/resouce.qrc

OTHER_FILES +=
