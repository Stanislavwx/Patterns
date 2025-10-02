#ifndef BILL_H
#define BILL_H

class Bill {
public:
    Bill(double limit = 0.0);

    bool canAdd(double amount) const; // чи влізе в ліміт
    void add(double amount);          // додати борг
    void pay(double amount);          // оплатити (не менше 0)
    void setLimit(double newLimit);   // змінити ліміт

    double limit() const;
    double debt()  const;

private:
    double limit_;
    double debt_;
};

#endif // BILL_H
