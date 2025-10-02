#include <iostream>
#include <iomanip>     
#include "Bill.h"
#include "Operator.h"
#include "Customer.h"

int main() {
    // Створюємо 2 оператори з тарифами
    // id, ціна/хв, ціна/смс, ціна/MB, % знижки
    Operator op0(0, 1.20, 0.15, 0.03, 20);
    Operator op1(1, 0.95, 0.20, 0.07, 10);

    // Створюємо 3 рахунки (з різними лімітами витрат)
    Bill b0(40), b1(60), b2(80);


    Customer c0(0, "Ivan",   17); 
    Customer c1(1, "Oksana", 66);
    Customer c2(2, "Taras",  30); // без знижок

    // Прив'язуємо їм операторів і рахунки
    c0.setOperator(&op0); c0.setBill(&b0);
    c1.setOperator(&op0); c1.setBill(&b1);
    c2.setOperator(&op1); c2.setBill(&b2);

    c0.talk(30);          // Ivan дзвонить 30 хв (знижка за вік)
    c0.message(10, c1);   // Ivan шле 10 смс Oksana (вони на одному операторі → знижка)
    c2.connect(500);      // Taras качає 500 MB (без знижок)
    b0.pay(5.5);          // Ivan платить 5.5 грн → борг зменшується
    c1.setOperator(&op1); // Oksana переходить до іншого оператора
    c1.message(10, c0);   // тепер Oksana шле 10 смс Ivan → знижки нема
    b1.setLimit(60);      // міняємо ліміт рахунку Oksana на 60
    c1.connect(300);      // Oksana качає 300 MB

    // Функція для красивого виводу стану клієнта
    auto print = [](const Customer& c){
        std::cout.setf(std::ios::fixed);
        std::cout << std::setprecision(2)
                  << "Customer " << c.id() << " " << c.name()
                  << " op=" << (c.op() ? c.op()->id() : -1)          // оператор
                  << " limit=" << (c.bill() ? c.bill()->limit() : 0) // ліміт
                  << " debt="  << (c.bill() ? c.bill()->debt() : 0)  // борг
                  << "\n";
    };

 
    print(c0); print(c1); print(c2);

    return 0;
}
