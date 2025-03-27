#include "parser.h"
#include "lexer.h"

int main() {
  int result = yyparse();
    if (result == 0) {
        std::cout << "Parsing successful" << std::endl;
    } else {
        std::cout << "Parsing failed" << std::endl;
    }
  return 0;
}