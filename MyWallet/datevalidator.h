#ifndef DATEVALIDATOR_H
#define DATEVALIDATOR_H

#include <QValidator>

class DateValidator : public QValidator
{
    Q_OBJECT
public:
    explicit DateValidator(QObject *parent = 0);
    QValidator::State validate(QString &text, int &) const;

signals:

public slots:

};

#endif // DATEVALIDATOR_H
