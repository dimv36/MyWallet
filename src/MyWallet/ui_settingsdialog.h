/********************************************************************************
** Form generated from reading UI file 'settingsdialog.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SETTINGSDIALOG_H
#define UI_SETTINGSDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>

QT_BEGIN_NAMESPACE

class Ui_SettingsDialog
{
public:
    QGridLayout *_main_layout;
    QGroupBox *_wallet_box;
    QGridLayout *_wallet_box_layout;
    QLineEdit *_directory;
    QLabel *_wallet_name_label;
    QLabel *_directory_label;
    QPushButton *_directory_button;
    QLineEdit *_wallet_name;
    QDialogButtonBox *_button_box;

    void setupUi(QDialog *SettingsDialog)
    {
        if (SettingsDialog->objectName().isEmpty())
            SettingsDialog->setObjectName(QStringLiteral("SettingsDialog"));
        SettingsDialog->setWindowModality(Qt::ApplicationModal);
        SettingsDialog->resize(488, 141);
        _main_layout = new QGridLayout(SettingsDialog);
        _main_layout->setObjectName(QStringLiteral("_main_layout"));
        _wallet_box = new QGroupBox(SettingsDialog);
        _wallet_box->setObjectName(QStringLiteral("_wallet_box"));
        _wallet_box->setCheckable(true);
        _wallet_box->setChecked(false);
        _wallet_box_layout = new QGridLayout(_wallet_box);
        _wallet_box_layout->setObjectName(QStringLiteral("_wallet_box_layout"));
        _directory = new QLineEdit(_wallet_box);
        _directory->setObjectName(QStringLiteral("_directory"));

        _wallet_box_layout->addWidget(_directory, 0, 1, 1, 2);

        _wallet_name_label = new QLabel(_wallet_box);
        _wallet_name_label->setObjectName(QStringLiteral("_wallet_name_label"));

        _wallet_box_layout->addWidget(_wallet_name_label, 1, 0, 1, 1);

        _directory_label = new QLabel(_wallet_box);
        _directory_label->setObjectName(QStringLiteral("_directory_label"));

        _wallet_box_layout->addWidget(_directory_label, 0, 0, 1, 1);

        _directory_button = new QPushButton(_wallet_box);
        _directory_button->setObjectName(QStringLiteral("_directory_button"));

        _wallet_box_layout->addWidget(_directory_button, 0, 3, 1, 1);

        _wallet_name = new QLineEdit(_wallet_box);
        _wallet_name->setObjectName(QStringLiteral("_wallet_name"));

        _wallet_box_layout->addWidget(_wallet_name, 1, 1, 1, 3);


        _main_layout->addWidget(_wallet_box, 0, 0, 1, 1);

        _button_box = new QDialogButtonBox(SettingsDialog);
        _button_box->setObjectName(QStringLiteral("_button_box"));
        _button_box->setOrientation(Qt::Horizontal);
        _button_box->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);

        _main_layout->addWidget(_button_box, 2, 0, 1, 1);


        retranslateUi(SettingsDialog);
        QObject::connect(_button_box, SIGNAL(accepted()), SettingsDialog, SLOT(accept()));
        QObject::connect(_button_box, SIGNAL(rejected()), SettingsDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(SettingsDialog);
    } // setupUi

    void retranslateUi(QDialog *SettingsDialog)
    {
        SettingsDialog->setWindowTitle(QApplication::translate("SettingsDialog", "\320\235\320\260\321\201\321\202\321\200\320\276\320\271\320\272\320\270", 0));
        _wallet_box->setTitle(QApplication::translate("SettingsDialog", "\320\237\320\260\321\200\320\260\320\274\320\265\321\202\321\200\321\213 \320\272\320\276\321\210\320\265\320\273\321\214\320\272\320\260", 0));
        _wallet_name_label->setText(QApplication::translate("SettingsDialog", "\320\232\320\276\321\210\320\265\320\273\320\265\320\272", 0));
        _directory_label->setText(QApplication::translate("SettingsDialog", "\320\224\320\270\321\200\320\265\320\272\321\202\320\276\321\200\320\270\321\217", 0));
        _directory_button->setText(QApplication::translate("SettingsDialog", "\320\230\320\267\320\274\320\265\320\275\320\270\321\202\321\214...", 0));
    } // retranslateUi

};

namespace Ui {
    class SettingsDialog: public Ui_SettingsDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SETTINGSDIALOG_H
