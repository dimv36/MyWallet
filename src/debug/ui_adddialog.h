/********************************************************************************
** Form generated from reading UI file 'adddialog.ui'
**
** Created by: Qt User Interface Compiler version 5.2.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ADDDIALOG_H
#define UI_ADDDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDateEdit>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QTextEdit>

QT_BEGIN_NAMESPACE

class Ui_AddDialog
{
public:
    QFormLayout *formLayout;
    QLabel *_label_date;
    QDateEdit *_date;
    QGroupBox *_rest_box;
    QFormLayout *_rest_layout;
    QLabel *_label_rest;
    QLineEdit *_rest_value;
    QLabel *_label_description_rest;
    QPlainTextEdit *_rest_descripton;
    QGroupBox *_income_box;
    QFormLayout *_income_layout;
    QLabel *_label_income;
    QLineEdit *_income_value;
    QLabel *_label_description_income;
    QTextEdit *_income_description;
    QDialogButtonBox *_button_box;

    void setupUi(QDialog *AddDialog)
    {
        if (AddDialog->objectName().isEmpty())
            AddDialog->setObjectName(QStringLiteral("AddDialog"));
        AddDialog->setWindowModality(Qt::ApplicationModal);
        AddDialog->resize(549, 657);
        QSizePolicy sizePolicy(QSizePolicy::MinimumExpanding, QSizePolicy::MinimumExpanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(AddDialog->sizePolicy().hasHeightForWidth());
        AddDialog->setSizePolicy(sizePolicy);
        AddDialog->setMinimumSize(QSize(0, 0));
        AddDialog->setModal(true);
        formLayout = new QFormLayout(AddDialog);
        formLayout->setObjectName(QStringLiteral("formLayout"));
        _label_date = new QLabel(AddDialog);
        _label_date->setObjectName(QStringLiteral("_label_date"));

        formLayout->setWidget(0, QFormLayout::LabelRole, _label_date);

        _date = new QDateEdit(AddDialog);
        _date->setObjectName(QStringLiteral("_date"));

        formLayout->setWidget(0, QFormLayout::FieldRole, _date);

        _rest_box = new QGroupBox(AddDialog);
        _rest_box->setObjectName(QStringLiteral("_rest_box"));
        _rest_box->setCheckable(true);
        _rest_box->setChecked(false);
        _rest_layout = new QFormLayout(_rest_box);
        _rest_layout->setObjectName(QStringLiteral("_rest_layout"));
        _label_rest = new QLabel(_rest_box);
        _label_rest->setObjectName(QStringLiteral("_label_rest"));

        _rest_layout->setWidget(0, QFormLayout::LabelRole, _label_rest);

        _rest_value = new QLineEdit(_rest_box);
        _rest_value->setObjectName(QStringLiteral("_rest_value"));

        _rest_layout->setWidget(0, QFormLayout::FieldRole, _rest_value);

        _label_description_rest = new QLabel(_rest_box);
        _label_description_rest->setObjectName(QStringLiteral("_label_description_rest"));

        _rest_layout->setWidget(1, QFormLayout::LabelRole, _label_description_rest);

        _rest_descripton = new QPlainTextEdit(_rest_box);
        _rest_descripton->setObjectName(QStringLiteral("_rest_descripton"));

        _rest_layout->setWidget(2, QFormLayout::SpanningRole, _rest_descripton);


        formLayout->setWidget(2, QFormLayout::SpanningRole, _rest_box);

        _income_box = new QGroupBox(AddDialog);
        _income_box->setObjectName(QStringLiteral("_income_box"));
        _income_box->setEnabled(true);
        _income_box->setCheckable(true);
        _income_box->setChecked(false);
        _income_layout = new QFormLayout(_income_box);
        _income_layout->setObjectName(QStringLiteral("_income_layout"));
        _label_income = new QLabel(_income_box);
        _label_income->setObjectName(QStringLiteral("_label_income"));

        _income_layout->setWidget(0, QFormLayout::LabelRole, _label_income);

        _income_value = new QLineEdit(_income_box);
        _income_value->setObjectName(QStringLiteral("_income_value"));

        _income_layout->setWidget(0, QFormLayout::FieldRole, _income_value);

        _label_description_income = new QLabel(_income_box);
        _label_description_income->setObjectName(QStringLiteral("_label_description_income"));

        _income_layout->setWidget(1, QFormLayout::LabelRole, _label_description_income);

        _income_description = new QTextEdit(_income_box);
        _income_description->setObjectName(QStringLiteral("_income_description"));

        _income_layout->setWidget(2, QFormLayout::SpanningRole, _income_description);


        formLayout->setWidget(3, QFormLayout::SpanningRole, _income_box);

        _button_box = new QDialogButtonBox(AddDialog);
        _button_box->setObjectName(QStringLiteral("_button_box"));
        _button_box->setOrientation(Qt::Horizontal);
        _button_box->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);
        _button_box->setCenterButtons(false);

        formLayout->setWidget(4, QFormLayout::FieldRole, _button_box);


        retranslateUi(AddDialog);
        QObject::connect(_button_box, SIGNAL(accepted()), AddDialog, SLOT(accept()));
        QObject::connect(_button_box, SIGNAL(rejected()), AddDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(AddDialog);
    } // setupUi

    void retranslateUi(QDialog *AddDialog)
    {
        AddDialog->setWindowTitle(QApplication::translate("AddDialog", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \320\270\321\201\321\202\320\276\321\207\320\275\320\270\320\272\320\270", 0));
        _label_date->setText(QApplication::translate("AddDialog", "\320\224\320\260\321\202\320\260:", 0));
        _date->setDisplayFormat(QApplication::translate("AddDialog", "d MMMM yyyy", 0));
        _rest_box->setTitle(QApplication::translate("AddDialog", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \321\200\320\260\321\201\321\205\320\276\320\264\321\213:", 0));
        _label_rest->setText(QApplication::translate("AddDialog", "\320\241\321\203\320\274\320\274\320\260: ", 0));
        _label_description_rest->setText(QApplication::translate("AddDialog", "\320\230\321\201\321\202\320\276\321\207\320\275\320\270\320\272 \321\200\320\260\321\201\321\205\320\276\320\264\320\276\320\262:", 0));
        _income_box->setTitle(QApplication::translate("AddDialog", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \320\264\320\276\321\205\320\276\320\264\321\213:", 0));
        _label_income->setText(QApplication::translate("AddDialog", "\320\241\321\203\320\274\320\274\320\260: ", 0));
        _label_description_income->setText(QApplication::translate("AddDialog", "\320\230\321\201\321\202\320\276\321\207\320\275\320\270\320\272 \320\264\320\276\321\205\320\276\320\264\320\276\320\262:", 0));
    } // retranslateUi

};

namespace Ui {
    class AddDialog: public Ui_AddDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ADDDIALOG_H
