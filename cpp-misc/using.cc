#include <tuple>
#include <variant>
#include <iostream>

using Value = int;
using Mul = std::tuple<Expr, Expr>;
using Add = std::tuple<Mul, Mul>;
using Expr = std::variant<Value, Add, Mul>;

/**
 * 結論としては再帰的な型をusingを使って定義することは出来なさそう
 * 型推論に失敗していそう。このコードはコンパイルできない。
 * なのでやるならstd::variantを持つ構造体とかを使うのがいい。
 */

int main() {
    // Create an expression tree for the expression (1 + 2) + (3 + 4)
    Value value = 1;
    Expr expr = value;
}