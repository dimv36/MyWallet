#include "mywallet.h"
#include "ui_mywallet.h"

MyWallet::MyWallet(QWidget *parent) :
    QMainWindow(parent),
    _ui(new Ui::MyWallet) {
    _ui -> setupUi(this);
}

MyWallet::~MyWallet() {
    delete _ui;
}


void MyWallet::on__action_add_triggered() {
    AddDialog *dialog = new AddDialog(this);
    dialog -> show();
}
