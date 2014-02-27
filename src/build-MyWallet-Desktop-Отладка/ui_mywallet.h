/********************************************************************************
** Form generated from reading UI file 'mywallet.ui'
**
** Created by: Qt User Interface Compiler version 5.2.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MYWALLET_H
#define UI_MYWALLET_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MyWallet
{
public:
    QAction *_action_add;
    QAction *_action_remove;
    QAction *_action_edit;
    QAction *_action_open;
    QAction *_action_exit;
    QAction *_action_settings;
    QWidget *_central_widget;
    QGridLayout *gridLayout;
    QTableWidget *_table;
    QFormLayout *_label_layout;
    QLabel *_label_output_month;
    QLabel *_label_output;
    QLabel *_label_input;
    QLabel *_label_total;
    QLabel *_label_output_month_value;
    QLabel *_label_output_value;
    QLabel *_label_input_value;
    QLabel *_label_total_value;
    QMenuBar *menuBar;
    QMenu *_menu_file;
    QMenu *_menu_table;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MyWallet)
    {
        if (MyWallet->objectName().isEmpty())
            MyWallet->setObjectName(QStringLiteral("MyWallet"));
        MyWallet->resize(704, 338);
        _action_add = new QAction(MyWallet);
        _action_add->setObjectName(QStringLiteral("_action_add"));
        QIcon icon;
        icon.addFile(QStringLiteral(":/edit_add.png"), QSize(), QIcon::Normal, QIcon::Off);
        _action_add->setIcon(icon);
        _action_remove = new QAction(MyWallet);
        _action_remove->setObjectName(QStringLiteral("_action_remove"));
        QIcon icon1;
        icon1.addFile(QStringLiteral(":/edit_remove.png"), QSize(), QIcon::Normal, QIcon::Off);
        _action_remove->setIcon(icon1);
        _action_edit = new QAction(MyWallet);
        _action_edit->setObjectName(QStringLiteral("_action_edit"));
        QIcon icon2;
        icon2.addFile(QStringLiteral(":/edit.png"), QSize(), QIcon::Normal, QIcon::On);
        _action_edit->setIcon(icon2);
        _action_open = new QAction(MyWallet);
        _action_open->setObjectName(QStringLiteral("_action_open"));
        QIcon icon3;
        icon3.addFile(QStringLiteral(":/folder_blue.png"), QSize(), QIcon::Normal, QIcon::Off);
        _action_open->setIcon(icon3);
        _action_exit = new QAction(MyWallet);
        _action_exit->setObjectName(QStringLiteral("_action_exit"));
        QIcon icon4;
        icon4.addFile(QStringLiteral(":/exit.png"), QSize(), QIcon::Normal, QIcon::Off);
        _action_exit->setIcon(icon4);
        _action_settings = new QAction(MyWallet);
        _action_settings->setObjectName(QStringLiteral("_action_settings"));
        QIcon icon5;
        icon5.addFile(QStringLiteral(":/kservices.png"), QSize(), QIcon::Normal, QIcon::Off);
        _action_settings->setIcon(icon5);
        _central_widget = new QWidget(MyWallet);
        _central_widget->setObjectName(QStringLiteral("_central_widget"));
        gridLayout = new QGridLayout(_central_widget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        _table = new QTableWidget(_central_widget);
        if (_table->columnCount() < 5)
            _table->setColumnCount(5);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        _table->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        _table->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        _table->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        _table->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        _table->setHorizontalHeaderItem(4, __qtablewidgetitem4);
        _table->setObjectName(QStringLiteral("_table"));
        _table->setEditTriggers(QAbstractItemView::NoEditTriggers);
        _table->setSelectionMode(QAbstractItemView::ExtendedSelection);
        _table->setSelectionBehavior(QAbstractItemView::SelectItems);
        _table->setShowGrid(true);
        _table->setGridStyle(Qt::DotLine);
        _table->setSortingEnabled(true);
        _table->horizontalHeader()->setCascadingSectionResizes(true);
        _table->horizontalHeader()->setDefaultSectionSize(130);
        _table->horizontalHeader()->setMinimumSectionSize(15);
        _table->horizontalHeader()->setProperty("showSortIndicator", QVariant(false));
        _table->horizontalHeader()->setStretchLastSection(true);
        _table->verticalHeader()->setVisible(false);
        _table->verticalHeader()->setCascadingSectionResizes(false);
        _table->verticalHeader()->setHighlightSections(false);
        _table->verticalHeader()->setMinimumSectionSize(15);
        _table->verticalHeader()->setProperty("showSortIndicator", QVariant(false));
        _table->verticalHeader()->setStretchLastSection(false);

        gridLayout->addWidget(_table, 0, 0, 1, 1);

        _label_layout = new QFormLayout();
        _label_layout->setSpacing(6);
        _label_layout->setObjectName(QStringLiteral("_label_layout"));
        _label_output_month = new QLabel(_central_widget);
        _label_output_month->setObjectName(QStringLiteral("_label_output_month"));

        _label_layout->setWidget(0, QFormLayout::LabelRole, _label_output_month);

        _label_output = new QLabel(_central_widget);
        _label_output->setObjectName(QStringLiteral("_label_output"));

        _label_layout->setWidget(1, QFormLayout::LabelRole, _label_output);

        _label_input = new QLabel(_central_widget);
        _label_input->setObjectName(QStringLiteral("_label_input"));

        _label_layout->setWidget(2, QFormLayout::LabelRole, _label_input);

        _label_total = new QLabel(_central_widget);
        _label_total->setObjectName(QStringLiteral("_label_total"));

        _label_layout->setWidget(3, QFormLayout::LabelRole, _label_total);

        _label_output_month_value = new QLabel(_central_widget);
        _label_output_month_value->setObjectName(QStringLiteral("_label_output_month_value"));
        _label_output_month_value->setAlignment(Qt::AlignCenter);

        _label_layout->setWidget(0, QFormLayout::FieldRole, _label_output_month_value);

        _label_output_value = new QLabel(_central_widget);
        _label_output_value->setObjectName(QStringLiteral("_label_output_value"));
        _label_output_value->setAlignment(Qt::AlignCenter);

        _label_layout->setWidget(1, QFormLayout::FieldRole, _label_output_value);

        _label_input_value = new QLabel(_central_widget);
        _label_input_value->setObjectName(QStringLiteral("_label_input_value"));
        _label_input_value->setAlignment(Qt::AlignCenter);

        _label_layout->setWidget(2, QFormLayout::FieldRole, _label_input_value);

        _label_total_value = new QLabel(_central_widget);
        _label_total_value->setObjectName(QStringLiteral("_label_total_value"));
        _label_total_value->setAlignment(Qt::AlignCenter);

        _label_layout->setWidget(3, QFormLayout::FieldRole, _label_total_value);


        gridLayout->addLayout(_label_layout, 1, 0, 1, 1);

        MyWallet->setCentralWidget(_central_widget);
        menuBar = new QMenuBar(MyWallet);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 704, 19));
        _menu_file = new QMenu(menuBar);
        _menu_file->setObjectName(QStringLiteral("_menu_file"));
        _menu_table = new QMenu(menuBar);
        _menu_table->setObjectName(QStringLiteral("_menu_table"));
        MyWallet->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MyWallet);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MyWallet->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MyWallet);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MyWallet->setStatusBar(statusBar);

        menuBar->addAction(_menu_file->menuAction());
        menuBar->addAction(_menu_table->menuAction());
        _menu_file->addAction(_action_open);
        _menu_file->addAction(_action_settings);
        _menu_file->addSeparator();
        _menu_file->addAction(_action_exit);
        _menu_table->addAction(_action_add);
        _menu_table->addAction(_action_remove);
        _menu_table->addAction(_action_edit);
        mainToolBar->addAction(_action_add);
        mainToolBar->addAction(_action_remove);
        mainToolBar->addAction(_action_edit);
        mainToolBar->addAction(_action_settings);

        retranslateUi(MyWallet);

        QMetaObject::connectSlotsByName(MyWallet);
    } // setupUi

    void retranslateUi(QMainWindow *MyWallet)
    {
        MyWallet->setWindowTitle(QApplication::translate("MyWallet", "MyWallet", 0));
        _action_add->setText(QApplication::translate("MyWallet", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \321\201\321\202\321\200\320\276\320\272\321\203", 0));
        _action_remove->setText(QApplication::translate("MyWallet", "\320\243\320\264\320\260\320\273\320\270\321\202\321\214 \321\201\321\202\321\200\320\276\320\272\321\203", 0));
        _action_edit->setText(QApplication::translate("MyWallet", "\320\240\320\265\320\264\320\260\320\272\321\202\320\270\321\200\320\276\320\262\320\260\321\202\321\214 \321\201\321\202\321\200\320\276\320\272\321\203", 0));
        _action_open->setText(QApplication::translate("MyWallet", "\320\236\321\202\320\272\321\200\321\213\321\202\321\214 \320\272\320\276\321\210\320\265\320\273\321\221\320\272", 0));
#ifndef QT_NO_TOOLTIP
        _action_open->setToolTip(QApplication::translate("MyWallet", "\320\236\321\202\320\272\321\200\321\213\321\202\321\214", 0));
#endif // QT_NO_TOOLTIP
        _action_exit->setText(QApplication::translate("MyWallet", "\320\222\321\213\321\205\320\276\320\264", 0));
        _action_settings->setText(QApplication::translate("MyWallet", "\320\235\320\260\321\201\321\202\321\200\320\276\320\271\320\272\320\270", 0));
        QTableWidgetItem *___qtablewidgetitem = _table->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QApplication::translate("MyWallet", "\320\224\320\260\321\202\320\260", 0));
        QTableWidgetItem *___qtablewidgetitem1 = _table->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QApplication::translate("MyWallet", "\320\240\320\260\321\201\321\205\320\276\320\264\321\213", 0));
        QTableWidgetItem *___qtablewidgetitem2 = _table->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QApplication::translate("MyWallet", "\320\241\321\202\320\260\321\202\321\214\321\217 \321\200\320\260\321\201\321\205\320\276\320\264\320\276\320\262", 0));
        QTableWidgetItem *___qtablewidgetitem3 = _table->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QApplication::translate("MyWallet", "\320\224\320\276\321\205\320\276\320\264\321\213", 0));
        QTableWidgetItem *___qtablewidgetitem4 = _table->horizontalHeaderItem(4);
        ___qtablewidgetitem4->setText(QApplication::translate("MyWallet", "\320\241\321\202\320\260\321\202\321\214\321\217 \320\264\320\276\321\205\320\276\320\264\320\276\320\262", 0));
        _label_output_month->setText(QApplication::translate("MyWallet", "\320\236\321\201\321\202\320\260\321\202\320\276\320\272 \320\275\320\260 \320\275\320\260\321\207\320\260\320\273\320\276 \320\274\320\265\321\201\321\217\321\206\320\260: ", 0));
        _label_output->setText(QApplication::translate("MyWallet", "\320\240\320\260\321\201\321\205\320\276\320\264\321\213:", 0));
        _label_input->setText(QApplication::translate("MyWallet", "\320\224\320\276\321\205\320\276\320\264:", 0));
        _label_total->setText(QApplication::translate("MyWallet", "\320\230\321\202\320\276\320\263\320\276:", 0));
        _label_output_month_value->setText(QApplication::translate("MyWallet", "0", 0));
        _label_output_value->setText(QString());
        _label_input_value->setText(QString());
        _label_total_value->setText(QString());
        _menu_file->setTitle(QApplication::translate("MyWallet", "\320\244\320\260\320\271\320\273", 0));
        _menu_table->setTitle(QApplication::translate("MyWallet", "\320\242\320\260\320\261\320\273\320\270\321\206\320\260", 0));
    } // retranslateUi

};

namespace Ui {
    class MyWallet: public Ui_MyWallet {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MYWALLET_H
