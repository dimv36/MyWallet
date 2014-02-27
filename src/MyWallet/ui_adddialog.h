/********************************************************************************
** Form generated from reading UI file 'adddialog.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
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

QT_BEGIN_NAMESPACE

class Ui_AddDialog
{
public:
    QFormLayout *formLayout;
    QLabel *_label_date;
    QDateEdit *_date;
    QGroupBox *_output_box;
    QFormLayout *_rest_layout;
    QLabel *_label_output;
    QLineEdit *_output_value;
    QLabel *_label_description_output;
    QLineEdit *_output_description;
    QGroupBox *_input_box;
    QFormLayout *_income_layout;
    QLabel *_label_input;
    QLineEdit *_input_value;
    QLabel *_label_description_input;
    QLineEdit *_input_description;
    QDialogButtonBox *_button_box;

    void setupUi(QDialog *AddDialog)
    {
        if (AddDialog->objectName().isEmpty())
            AddDialog->setObjectName(QStringLiteral("AddDialog"));
        AddDialog->setWindowModality(Qt::ApplicationModal);
        AddDialog->resize(549, 319);
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

        _output_box = new QGroupBox(AddDialog);
        _output_box->setObjectName(QStringLiteral("_output_box"));
        _output_box->setCheckable(true);
        _output_box->setChecked(false);
        _rest_layout = new QFormLayout(_output_box);
        _rest_layout->setObjectName(QStringLiteral("_rest_layout"));
        _rest_layout->setFieldGrowthPolicy(QFormLayout::AllNonFixedFieldsGrow);
        _label_output = new QLabel(_output_box);
        _label_output->setObjectName(QStringLiteral("_label_output"));

        _rest_layout->setWidget(0, QFormLayout::LabelRole, _label_output);

        _output_value = new QLineEdit(_output_box);
        _output_value->setObjectName(QStringLiteral("_output_value"));

        _rest_layout->setWidget(0, QFormLayout::FieldRole, _output_value);

        _label_description_output = new QLabel(_output_box);
        _label_description_output->setObjectName(QStringLiteral("_label_description_output"));

        _rest_layout->setWidget(1, QFormLayout::LabelRole, _label_description_output);

        _output_description = new QLineEdit(_output_box);
        _output_description->setObjectName(QStringLiteral("_output_description"));

        _rest_layout->setWidget(2, QFormLayout::SpanningRole, _output_description);


        formLayout->setWidget(2, QFormLayout::SpanningRole, _output_box);

        _input_box = new QGroupBox(AddDialog);
        _input_box->setObjectName(QStringLiteral("_input_box"));
        _input_box->setEnabled(true);
        _input_box->setCheckable(true);
        _input_box->setChecked(false);
        _income_layout = new QFormLayout(_input_box);
        _income_layout->setObjectName(QStringLiteral("_income_layout"));
        _income_layout->setFieldGrowthPolicy(QFormLayout::AllNonFixedFieldsGrow);
        _label_input = new QLabel(_input_box);
        _label_input->setObjectName(QStringLiteral("_label_input"));

        _income_layout->setWidget(0, QFormLayout::LabelRole, _label_input);

        _input_value = new QLineEdit(_input_box);
        _input_value->setObjectName(QStringLiteral("_input_value"));

        _income_layout->setWidget(0, QFormLayout::FieldRole, _input_value);

        _label_description_input = new QLabel(_input_box);
        _label_description_input->setObjectName(QStringLiteral("_label_description_input"));

        _income_layout->setWidget(1, QFormLayout::LabelRole, _label_description_input);

        _input_description = new QLineEdit(_input_box);
        _input_description->setObjectName(QStringLiteral("_input_description"));

        _income_layout->setWidget(2, QFormLayout::SpanningRole, _input_description);


        formLayout->setWidget(3, QFormLayout::SpanningRole, _input_box);

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
        _output_box->setTitle(QApplication::translate("AddDialog", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \321\200\320\260\321\201\321\205\320\276\320\264\321\213:", 0));
        _label_output->setText(QApplication::translate("AddDialog", "\320\241\321\203\320\274\320\274\320\260: ", 0));
        _label_description_output->setText(QApplication::translate("AddDialog", "\320\230\321\201\321\202\320\276\321\207\320\275\320\270\320\272 \321\200\320\260\321\201\321\205\320\276\320\264\320\276\320\262:", 0));
        _input_box->setTitle(QApplication::translate("AddDialog", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \320\264\320\276\321\205\320\276\320\264\321\213:", 0));
        _label_input->setText(QApplication::translate("AddDialog", "\320\241\321\203\320\274\320\274\320\260: ", 0));
        _label_description_input->setText(QApplication::translate("AddDialog", "\320\230\321\201\321\202\320\276\321\207\320\275\320\270\320\272 \320\264\320\276\321\205\320\276\320\264\320\276\320\262:", 0));
    } // retranslateUi

};

namespace Ui {
    class AddDialog: public Ui_AddDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ADDDIALOG_H
