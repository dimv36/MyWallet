#include "datevalidator.h"

DateValidator::DateValidator(QObject *parent) :
    QValidator(parent) {

}


QValidator::State DateValidator::validate(QString &text, int &) const {
    QRegExp expression = QRegExp("[0-1][0-9]")
}
