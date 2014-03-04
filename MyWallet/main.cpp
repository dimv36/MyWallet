#include "mywallet.h"
#include <QApplication>

int main(int argc, char *argv[]) {
    QApplication application(argc, argv);
    MyWallet window;
    window.show();
    return application.exec();
}
