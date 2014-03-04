/********************************************************************************
** Form generated from reading UI file 'restmonthdialog.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_RESTMONTHDIALOG_H
#define UI_RESTMONTHDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLineEdit>

QT_BEGIN_NAMESPACE

class Ui_RestMonthDialog
{
public:
    QGridLayout *_main_layout;
    QLineEdit *_value;
    QDialogButtonBox *_button_box;

    void setupUi(QDialog *RestMonthDialog)
    {
        if (RestMonthDialog->objectName().isEmpty())
            RestMonthDialog->setObjectName(QStringLiteral("RestMonthDialog"));
        RestMonthDialog->resize(368, 70);
        _main_layout = new QGridLayout(RestMonthDialog);
        _main_layout->setObjectName(QStringLiteral("_main_layout"));
        _value = new QLineEdit(RestMonthDialog);
        _value->setObjectName(QStringLiteral("_value"));

        _main_layout->addWidget(_value, 0, 0, 1, 1);

        _button_box = new QDialogButtonBox(RestMonthDialog);
        _button_box->setObjectName(QStringLiteral("_button_box"));
        _button_box->setOrientation(Qt::Horizontal);
        _button_box->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);

        _main_layout->addWidget(_button_box, 1, 0, 1, 1);


        retranslateUi(RestMonthDialog);
        QObject::connect(_button_box, SIGNAL(accepted()), RestMonthDialog, SLOT(accept()));
        QObject::connect(_button_box, SIGNAL(rejected()), RestMonthDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(RestMonthDialog);
    } // setupUi

    void retranslateUi(QDialog *RestMonthDialog)
    {
        RestMonthDialog->setWindowTitle(QApplication::translate("RestMonthDialog", "\320\222\320\262\320\265\321\201\321\202\320\270 \320\276\321\201\321\202\320\260\321\202\320\276\320\272 \320\275\320\260 \320\275\320\260\321\207\320\260\320\273\320\276 \320\274\320\265\321\201\321\217\321\206\320\260", 0));
    } // retranslateUi

};

namespace Ui {
    class RestMonthDialog: public Ui_RestMonthDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_RESTMONTHDIALOG_H
