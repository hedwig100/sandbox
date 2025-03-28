
%top {

#include "sql.h"
#include "parser.h"
#include <stdio.h>

}

/****************
** Options
*****************/

%option noyywrap
%option reentrant
%option bison-bridge

/****************
** Declarations
****************/
DIGIT [0-9]
ID [_a-zA-Z][_a-zA-Z0-9]*

/****************
** Rules
*****************/
%%

[ \t\n]+

SELECT {return TOKEN_SELECT;}
FROM {return TOKEN_FROM;}

[+,;] { return yytext[0]; }

{DIGIT}+ {
    yylval->ival = strtoll(yytext, nullptr, 0);
    return TOKEN_INTEGER_VAL;
}

{ID} {
    yylval->identifier = strdup(yytext);
    return TOKEN_IDENTIFIER;
}

%%

void yyerror(sql::ParseResult* result, yyscan_t scanner, char const *msg) {
    fprintf(stderr, "%s\n", msg);
}


