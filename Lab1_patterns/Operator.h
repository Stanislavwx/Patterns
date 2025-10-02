#ifndef OPERATOR_H
#define OPERATOR_H

class Operator {
public:
    Operator(int id, double talkCharge, double messageCost, double networkCharge, int discountRate);

    int    id() const;

    double talkingCost(int minutes, int customerAge) const; // знижка: <18 або >65
    double messageCost(int quantity, bool sameOperator) const; // знижка: той самий оператор
    double networkCost(double megabytes) const; // без знижки

private:
    int    id_;
    double talkCharge_;
    double messageCost_;
    double networkCharge_;
    int    discountRate_; // %
};

#endif // OPERATOR_H
