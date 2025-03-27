/* Reverse Polish Notation calculator */

/* Prologue */
%{
    #include <stdio.h>
    #include <math.h>
    int yylex(void);
    void yyerror(char const *);
%}

/* Bison declarations */
%define api.value.type {double}
%token NUMBER

/* Grammer rules */
%%

input
    : %empty
    | input line
    ;

line
    : '\n'
    | exp '\n' { printf("%.10g\n", $1); }
    ;

exp
    : NUMBER
    | exp exp '+' { $$ = $1 + $2; }
    | exp exp '-' { $$ = $1 - $2; }
    | exp exp '*' { $$ = $1 * $2; }
    | exp exp '/' { $$ = $1 / $2; }
    | exp exp '^' { $$ = pow($1, $2); }
    | exp 'n' { $$ = -$1; }
    ;

/* Epilogue */
%%

#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

int yylex(void) {
    int c = getchar();
    while (c == ' ' || c == '\t')
        c = getchar();
    
    if (c == '.' || isdigit(c)) {
        ungetc(c, stdin);
        if (scanf("%lf", &yylval) != 1)
            abort();
        return NUMBER;
    } else if (c == EOF)
        return YYEOF;
    else
        return c;
}

void yyerror(char const *s) {
    fprintf(stderr, "%s\n", s);
}

int main(void) {
    return yyparse();
}

