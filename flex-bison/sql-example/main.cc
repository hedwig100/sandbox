#include "parser.h"
#include "lexer.h"
#include <iostream>
#include "sql.h"
#include <string>

sql::ParseResult Parse(const std::string &sql_stmt) {
  yyscan_t scanner;
  YY_BUFFER_STATE state;
  yylex_init(&scanner);

  const char* sql_stmt_cchr = sql_stmt.c_str();
  state = yy_scan_string(sql_stmt_cchr, scanner);
  sql::ParseResult result;
  yyparse(&result, scanner);

  yy_delete_buffer(state, scanner);
  yylex_destroy(scanner);

  return result;
}

int main() {
  sql::ParseResult result = Parse("SELECT a FROM table;");
  return 0;
}