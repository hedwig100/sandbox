%{

#include "sql.h"
#include <string>

%}

%define api.token.prefix {TOKEN_}

/************
** Semantic values (https://www.gnu.org/software/bison/manual/html_node/Union-Decl.html)
*************/

%union {
    int ival;
    std::string identifier;

    sql::SelectStatement *select_statement;
}


/************
** Token types and 
*************/

/* Terminal types (https://www.gnu.org/software/bison/manual/html_node/Token-Decl.html) */
%token <ival> INTEGER_VAL
%token <identifier> IDENTIFIER

%token SELECT FROM

/* Non-terminal symbols (https://www.gnu.org/software/bison/manual/html_node/Type-Decl.html)
%type <select_statement> select_statement


/**********
** Grammer Definitions
**********/
%%

input
    : select_statement
    ;

select_statement
    : SELECT column FROM table ';'
    ;

column
    : IDENTIFIER
    ;

table
    : IDENTIFIER
    ;

%%




