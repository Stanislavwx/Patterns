#include "Bill.h"
#include <algorithm>

Bill::Bill(double limit) : limit_(limit), debt_(0.0) {}

// Перевіряє, чи можна додати ще amount до боргу, не перевищивши ліміт
bool Bill::canAdd(double amount) const {
    return debt_ + amount <= limit_;
}

// Додає нову витрату до боргу
void Bill::add(double amount) {
    debt_ += amount;
}

// Оплата: зменшує борг на amount, але не дає боргу стати від’ємним
void Bill::pay(double amount) {
    if (amount < 0) return;  // якщо число від’ємне — нічого не робимо
    debt_ = std::max(0.0, debt_ - amount);
}

// Міняє ліміт рахунку на новий
void Bill::setLimit(double newLimit) {
    limit_ = newLimit;
}

// Повертає значення ліміту 
double Bill::limit() const { return limit_; }

// Повертає поточний борг
double Bill::debt()  const { return debt_;  }
