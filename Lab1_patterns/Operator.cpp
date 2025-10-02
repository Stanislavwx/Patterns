#include "Operator.h"

// Конструктор: створюємо оператора з його параметрами тарифу
Operator::Operator(int id, double t, double m, double n, int disc)
    : id_(id),                // ID оператора
      talkCharge_(t),         // ціна за хвилину розмови
      messageCost_(m),        // ціна за одне SMS
      networkCharge_(n),      // ціна за 1 MB інтернету
      discountRate_(disc) {}  // відсоток знижки (наприклад, 20 = 20%)

// Повертає ID оператора
int Operator::id() const { return id_; }

// Рахує вартість дзвінка
double Operator::talkingCost(int minutes, int age) const {
    double cost = minutes * talkCharge_;   // базова вартість: хвилини × тариф
    if (age < 18 || age > 65)              // якщо вік <18 або >65
        cost *= (1.0 - discountRate_ / 100.0); // робимо знижку (наприклад, 20%)
    return cost;                           // повертаємо остаточну ціну
}

// Рахує вартість SMS
double Operator::messageCost(int qty, bool sameOperator) const {
    double cost = qty * messageCost_;      // базова ціна: кількість × тариф
    if (sameOperator)                      // якщо обидва клієнти в одного оператора
        cost *= (1.0 - discountRate_ / 100.0); // даємо знижку
    return cost;
}

// Рахує вартість інтернету
double Operator::networkCost(double mb) const {
    return mb * networkCharge_; // мегабайти × тариф за 1 MB (знижки нема)
}
