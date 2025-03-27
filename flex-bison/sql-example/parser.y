%code requires {

#include "sql.h"
#include <string>
#include <stdio.h>
#include <iostream>

}

%define api.pure full

/************
** Semantic values (https://www.gnu.org/software/bison/manual/html_node/Union-Decl.html)
*************/

%union {
    int ival;
    char *identifier;

    sql::SelectStatement *select_statement;
}


// Destructor (https://www.gnu.org/software/bison/manual/html_node/Destructor-Decl.html)
%destructor {} <ival>
%destructor { delete($$); } <*>


/************
** Semantic Value type and the corresponding token or nterm
*************/
%define api.token.prefix {TOKEN_}

/* Terminal types (https://www.gnu.org/software/bison/manual/html_node/Token-Decl.html) */
%token <ival> INTEGER_VAL
%token <identifier> IDENTIFIER

%token SELECT FROM

/* Non-terminal symbols (https://www.gnu.org/software/bison/manual/html_node/Type-Decl.html) */
%type <select_statement> select_statement

%{
extern int yylex(YYSTYPE *);
extern void yyerror(char const *);
%}

/**********
** Grammer Definitions
**********/
%%

input
    : select_statement
    ;

select_statement
    : SELECT column FROM table ';' { std::cerr << "SELECT!!\n"; }
    ;

column
    : INTEGER_VAL { std::cerr << "integer!!\n"; }
    | IDENTIFIER { std::cerr << "ident!!\n"; }
    ;

table
    : IDENTIFIER { std::cerr << "ident!!\n"; }
    ;

%%




