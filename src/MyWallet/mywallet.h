#ifndef MYWALLET_H
#define MYWALLET_H

#include <QMainWindow>
#include "adddialog.h"

namespace Ui {
class MyWallet;
}

class MyWallet : public QMainWindow
{
    Q_OBJECT

public:
    explicit MyWallet(QWidget *parent = 0);
    ~MyWallet();

private slots:
    void on__action_add_triggered();

private:
    Ui::MyWallet* _ui;
};

#endif // MYWALLET_H
