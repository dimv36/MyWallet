#include "settingsdialog.h"
#include "ui_settingsdialog.h"

SettingsDialog::SettingsDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::SettingsDialog) {
    _ui -> setupUi(this);
    _ui -> _button_box -> button(_ui -> _button_box -> Cancel) -> setText("Отмена");
}


SettingsDialog::~SettingsDialog() {
    delete _ui;
}


void SettingsDialog::set_directory(const QString directory) {
    _ui -> _directory -> setText(directory);
}


void SettingsDialog::set_wallet_name(const QString wallet_name) {
    _ui -> _wallet_name -> setText(wallet_name);
}


QString SettingsDialog::get_directory() const {
    return _ui -> _directory -> text();
}


QString SettingsDialog::get_wallet_name() const {
    return _ui -> _wallet_name -> text();
}


bool SettingsDialog::IsWalletBoxIsActive() const {
    return _ui -> _wallet_box -> isChecked();
}


void SettingsDialog::on__directory_button_clicked() {
    QString directory = QFileDialog::getExistingDirectory(this,
                                                          tr("Открыть папку"),
                                                          QDir().current().path());
    _ui -> _directory -> setText(directory);
}
