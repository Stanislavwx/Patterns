#include "Customer.h"
#include "Operator.h"
#include "Bill.h"

// Конструктор: створює клієнта з id, ім’ям і віком.
Customer::Customer(int id, const std::string& name, int age)
    : id_(id), name_(name), age_(age), op_(nullptr), bill_(nullptr) {}

// Призначаємо оператор клієнту
void Customer::setOperator(Operator* op) { op_ = op; }

// Призначаємо рахунок клієнту
void Customer::setBill(Bill* bill)       { bill_ = bill; }

// Метод "дзвінок"
void Customer::talk(int minutes) {
    if (!op_ || !bill_) return;                   // якщо нема оператора чи рахунку — вихід
    double cost = op_->talkingCost(minutes, age_); // оператор рахує ціну (враховуючи вік)
    if (bill_->canAdd(cost)) bill_->add(cost);     // якщо не перевищили ліміт → додаємо борг
}

// Метод "повідомлення": відправляє кількість смс іншому клієнту
void Customer::message(int quantity, const Customer& other) {
    if (!op_ || !bill_ || !other.op_) return;     // якщо нема даних — нічого не робимо
    bool sameOp = (op_ == other.op_);             // перевіряємо, чи в одного оператора
    double cost = op_->messageCost(quantity, sameOp); // оператор рахує ціну (може бути знижка)
    if (bill_->canAdd(cost)) bill_->add(cost);        // додаємо борг, якщо влізе
}

//мегабайти
void Customer::connect(double megabytes) {
    if (!op_ || !bill_) return;                   
    double cost = op_->networkCost(megabytes);    
    if (bill_->canAdd(cost)) bill_->add(cost);    //додаємо борг
}

int Customer::id() const { return id_; }
const std::string& Customer::name() const { return name_; }
int Customer::age() const { return age_; }
const Operator* Customer::op() const { return op_; }
const Bill* Customer::bill() const { return bill_; }
