
%{

#include "parser.h"
#include <stdio.h>

%}

/****************
** Options
*****************/

%option noyywrap

/****************
** Declarations
****************/
DIGIT [0-9]
ID [_a-zA-Z][_a-zA-Z0-9]*

/****************
** Rules
*****************/

[ \t\n]+

[+,;] { return yytext[0]; }

{DIGIT}+ {
    yylval->ival = strtoll(yytext, nullptr, 0);
    return TOKEN_INTEGER_VAL;
}

{ID} {
    yylval->identifier = strdup(yytext);
    return TOKEN_IDENTIFIER;
}

/* SQL keywords */
SELECT TOKEN_SELECT
FROM TOKEN_FROM



