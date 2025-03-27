%code requires {

#include "sql.h"
#include <string>
#include <stdio.h>

extern int yylex(void);
void yyerror(char const *msg) {
    fprintf(stderr, "%s\n", msg);
}

}

/************
** Semantic values (https://www.gnu.org/software/bison/manual/html_node/Union-Decl.html)
*************/

%union {
    int ival;
    std::string identifier;

    sql::SelectStatement *select_statement;
}


// Destructor (https://www.gnu.org/software/bison/manual/html_node/Destructor-Decl.html)
%destructor {} <ival> <identifier>
%destructor { delete($$); } <*>


/************
** Semantic Value type and the corresponding token or nterm
*************/
%define api.token.prefix {TOKEN_}

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




