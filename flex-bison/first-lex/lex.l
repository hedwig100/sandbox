%option header-file="lex.yy.h"
%option noyywrap

%{
int num_lines = 0, num_chars = 0;
%}

%%
\n ++num_lines; ++num_chars;

. ++num_chars;

%%

int main() {
    yylex();
    printf("Number of lines = %d, Number of chars = %d\n", num_lines, num_chars);
}