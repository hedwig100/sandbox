#include <tuple>
#include <variant>
#include <iostream>

/**
 * 結論としては再帰的な型をusingを使って定義することは出来なさそう
 * 型推論に失敗していそう。このコードはコンパイルできない。
 * なのでやるならstd::variantを持つ構造体とかを使うのがいい。
 */

// using Value = int;
// using Mul = std::tuple<Expr, Expr>;
// using Add = std::tuple<Mul, Mul>;
// using Expr = std::variant<Value, Add, Mul>;

// int main() {
//     // Create an expression tree for the expression (1 + 2) + (3 + 4)
//     Value value = 1;
//     Expr expr = value;
// }

/**
 * 結論としては再帰的な型をusingを使って定義することは出来なそう。
 * ポインタ型にしても、再帰的に利用したい型をusingで定義していて宣言ができないのでできない。
 * なのでやるならstd::variantを持つ構造体とかを使うのがいい。
 */

// using Value2 = int;
// using Mul2 = std::tuple<Expr2*, Expr2*>;
// using Add2 = std::tuple<Mul2*, Mul2*>;
// using Expr2 = std::variant<Value2*, Add2*, Mul2*>;

// int ptr_using() {
//     // Create an expression tree for the expression (1 + 2) + (3 + 4)
//     Value2 value = 1;
//     Expr2 expr = &value;
//     return 0;
// }

/**
 * 以下のコードはコンパイルできる。
 * 再帰的な型を定義するときはポインタを使う必要あり(型のサイズが計算できなくなるので)
 */


using Value = int;

struct Expr;

struct Mul {
    Mul() = default;
    Mul(Expr *left, Expr *right) : values(left, right) {}
    std::tuple<Expr*, Expr*> values;
};

struct Add {
    Add() = default;
    Add(Mul *left, Mul *right) : values(left, right) {}
    std::tuple<Mul*, Mul*> values;
};

struct Expr {
    Expr() = default;
    Expr(Value *value) : value(value) {}
    Expr(Mul *mul) : value(mul) {}
    Expr(Add *add) : value(add) {}
    std::variant<Value*, Add*, Mul*> value;
};

int ptr_struct() {
    // Create an expression tree for the expression (1 + 2) + (3 + 4)
    Value value = 1;
    Expr expr = {&value};

    // You can also create Add and Mul expressions
    Mul mul = {&expr, &expr};
    Add add = {&mul, &mul};

    std::cout << "Expression tree created successfully." << std::endl;
    return 0;
}

int main() {
    // ptr_using();
    ptr_struct();
    return 0;
}