/********************************************************************************
** Form generated from reading UI file 'editdialog.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_EDITDIALOG_H
#define UI_EDITDIALOG_H

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

class Ui_EditDialog
{
public:
    QGridLayout *_main_layout;
    QLineEdit *_editing_field;
    QDialogButtonBox *_button_box;

    void setupUi(QDialog *EditDialog)
    {
        if (EditDialog->objectName().isEmpty())
            EditDialog->setObjectName(QStringLiteral("EditDialog"));
        EditDialog->setWindowModality(Qt::ApplicationModal);
        EditDialog->resize(307, 70);
        EditDialog->setModal(true);
        _main_layout = new QGridLayout(EditDialog);
        _main_layout->setObjectName(QStringLiteral("_main_layout"));
        _editing_field = new QLineEdit(EditDialog);
        _editing_field->setObjectName(QStringLiteral("_editing_field"));

        _main_layout->addWidget(_editing_field, 0, 0, 1, 1);

        _button_box = new QDialogButtonBox(EditDialog);
        _button_box->setObjectName(QStringLiteral("_button_box"));
        _button_box->setOrientation(Qt::Horizontal);
        _button_box->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);

        _main_layout->addWidget(_button_box, 1, 0, 1, 1);


        retranslateUi(EditDialog);
        QObject::connect(_button_box, SIGNAL(accepted()), EditDialog, SLOT(accept()));
        QObject::connect(_button_box, SIGNAL(rejected()), EditDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(EditDialog);
    } // setupUi

    void retranslateUi(QDialog *EditDialog)
    {
        EditDialog->setWindowTitle(QApplication::translate("EditDialog", "\320\230\320\267\320\274\320\265\320\275\320\270\321\202\321\214 \320\267\320\275\320\260\321\207\320\265\320\275\320\270\320\265", 0));
    } // retranslateUi

};

namespace Ui {
    class EditDialog: public Ui_EditDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_EDITDIALOG_H
