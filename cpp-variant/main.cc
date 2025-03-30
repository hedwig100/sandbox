#include <variant>
#include <iostream>
#include <string>

class X {
  public:
    X(int x) : x_(x) {}
    int x_;
};

class Y {
  public:
    Y(std::string y) : y_(y) {}
    std::string y_;
};

using Z = std::variant<X *, Y *>;

int main() {
    Z z1 = new X(42);
    Z z2 = new Y("Hello");
    
    if (std::holds_alternative<X *>(z1)) {
        std::cout << "z1 holds an X with value: " << std::get<X *>(z1)->x_ << std::endl;
    } else if (std::holds_alternative<Y *>(z1)) {
        std::cout << "z1 holds a Y with value: " << std::get<Y *>(z1)->y_ << std::endl;
    }

    if (std::holds_alternative<X *>(z2)) {
        std::cout << "z2 holds an X with value: " << std::get<X *>(z2)->x_ << std::endl;
    } else if (std::holds_alternative<Y *>(z2)) {
        std::cout << "z2 holds a Y with value: " << std::get<Y *>(z2)->y_ << std::endl;
    }
}