#ifndef CUSTOMER_H
#define CUSTOMER_H

#include <string>

class Operator;
class Bill;

class Customer {
public:
    Customer(int id, const std::string& name, int age);

    // прив’язки
    void setOperator(Operator* op);
    void setBill(Bill* bill);

    // дії
    void talk(int minutes);
    void message(int quantity, const Customer& other);
    void connect(double megabytes);

    // простий доступ (для друку)
    int id() const;
    const std::string& name() const;
    int age() const;
    const Operator* op() const;
    const Bill* bill() const;

private:
    int id_;
    std::string name_;
    int age_;
    Operator* op_; // може бути nullptr
    Bill* bill_;   // може бути nullptr
};

#endif // CUSTOMER_H
