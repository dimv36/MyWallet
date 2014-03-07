#ifndef MYWALLET_H
#define MYWALLET_H

#include <QMainWindow>
#include <QDir>
#include <QFileDialog>
#include <QMessageBox>
#include <QTableWidgetItem>
#include <QSettings>
#include <QDomDocument>
#include <QXmlStreamReader>
#include "adddialog.h"
#include "settingsdialog.h"
#include "restmonthdialog.h"

namespace Ui {
class MyWallet;
}

class MyWallet : public QMainWindow
{
    Q_OBJECT

private:
    Ui::MyWallet* _ui;
    QString _current_path;
    QString _wallet_name;
    QSettings _settings;

public:
    explicit MyWallet(QWidget *parent = 0);
    ~MyWallet();

signals:
    void SignalUpdate();
    void SignalWalletWasOpen();

private slots:
    void on__action_add_triggered();
    void on__action_exit_triggered();
    void on__action_remove_triggered();
    void SlotUpdateTotalFields();
    void on__action_open_triggered();
    void on__action_settings_triggered();
    void SlotUpdateWindowHeader();

    void on__action_edit_triggered();

private:
    void CreateTableRow(QDate &date, int total, QString &description, bool isRest = true);
    void AddNewRowInTable();
    void CreateNewItem(int row, int column, QString text);
    void ReadXML(/*const QString file_name*/);
    QTableWidgetItem* GetNextItem(QTableWidgetItem* item) const;
    QTableWidgetItem* GetPreviousItem(QTableWidgetItem *item) const;
    void WriteXML() const;
    void WriteSettings();
    void ReadSettings();
    void ChangeMonthRest();
};

#endif // MYWALLET_H
