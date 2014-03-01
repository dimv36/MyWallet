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
    adddialog.cpp \
    settingsdialog.cpp \
    restmonthdialog.cpp

HEADERS  += mywallet.h \
    adddialog.h \
    settingsdialog.h \
    restmonthdialog.h

FORMS    += mywallet.ui \
    adddialog.ui \
    settingsdialog.ui \
    restmonthdialog.ui

RESOURCES += \
    files/resouce.qrc

OTHER_FILES +=
