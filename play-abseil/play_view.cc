#include <string>
#include <vector>
#include <iostream>


#include "absl/strings/str_split.h"
#include "absl/status/status.h"
#include "absl/status/statusor.h"


absl::StatusOr<int> CrazyOperation(int x) {
    if (x == 0) return absl::InvalidArgumentError("Don't allow zero as an input.");
    return x;
}



int main() {
    std::string original = "a,b,c,ddd,e,";
    std::vector<std::string> splits = absl::StrSplit(original,",");
    for (const auto &s:splits) {
        std::cout << s << '\n';
    }

    int x;
    std::cin >> x;
    absl::StatusOr<int> crazy = CrazyOperation(x);
    if (crazy.ok()) std::cout << *crazy << '\n';
}