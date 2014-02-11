#-------------------------------------------------
#
# Project created by QtCreator 2014-02-02T13:32:05
#
#-------------------------------------------------

QT       += core gui xmlpatterns

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MyWallet
TEMPLATE = app


SOURCES += main.cpp\
        mywallet.cpp \
    adddialog.cpp

HEADERS  += mywallet.h \
    adddialog.h

FORMS    += mywallet.ui \
    adddialog.ui

RESOURCES += \
    files/resouce.qrc

OTHER_FILES +=
