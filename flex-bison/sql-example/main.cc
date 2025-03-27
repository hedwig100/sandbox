#include "parser.h"
#include "lexer.h"
#include <iostream>

int main() {
  yyscan_t scanner;
  yylex_init(&scanner);

  int result = yyparse(scanner);
  if (result == 0) {
    std::cout << "Parsing successful" << std::endl;
  } else {
    std::cout << "Parsing failed" << std::endl;
  }
  
  yylex_destroy(scanner);
  return 0;
}