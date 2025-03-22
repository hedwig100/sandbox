%{
    #include <stdio.h>
    #include <math.h>
    #include "calc.h"
    int yylex(void);
    void yyerror(char const*);
%}

%define api.value.type union
%token <double> NUM
%token <symrec*> VAR FUN
%nterm <double> exp

%precedence '='
%left '-' '+'
%left '*' '/'
%precedence NEG
%right '^'
%define parse.trace

%%

input
    : %empty
    | input line
    ;

line
    : '\n'
    | exp '\n'  { printf ("\t%.10g\n", $1); }
    | error '\n' { yyerrok; }
    ;

exp
    : NUM
    | VAR                { $$ = $1->value.var;          }
    | VAR '=' exp        { $$ = $3; $1->value.var = $3; }
    | FUN '(' exp ')'    { $$ = $1->value.fun($3);      }
    | exp '+' exp        { $$ = $1 + $3;      }
    | exp '-' exp        { $$ = $1 - $3;      }
    | exp '*' exp        { $$ = $1 * $3;      }
    | exp '/' exp        { $$ = $1 / $3;      }
    | '-' exp  %prec NEG { $$ = -$2;          }
    | exp '^' exp        { $$ = pow ($1, $3); }
    | '(' exp ')'        { $$ = $2;           }
    ;

%%

#include <stdlib.h>
#include <string.h>

symrec *putsym(char const *name, int sym_type) {
    symrec *ptr = (symrec *) malloc(sizeof(symrec));
    ptr->name = strdup(name);
    ptr->type = sym_type;
    ptr->next = sym_table;
    sym_table = ptr;
    return ptr;
}

symrec *getsym(char const *name) {
    for (symrec *ptr = sym_table; ptr; ptr = ptr->next)
        if (strcmp(ptr->name, name) == 0)
            return ptr;
    return NULL;
}

static void init_table(void) {
    for (int i = 0; funs[i].name; i++) {
        symrec *ptr = putsym(funs[i].name, FUN);
        ptr->value.fun = funs[i].fun;
    }
}

#include <stdlib.h>
#include <ctype.h>
#include <stddef.h>
#include <string.h>

int yylex (void) {
  int c = getchar ();

  /* Ignore white space, get first nonwhite character. */
  while (c == ' ' || c == '\t')
    c = getchar ();

  if (c == EOF)
    return YYEOF;

    /* Char starts a number => parse the number. */
  if (c == '.' || isdigit (c))
    {
      ungetc (c, stdin);
      if (scanf ("%lf", &yylval.NUM) != 1)
        abort ();
      return NUM;
    }

  if (isalpha (c))
    {
      static ptrdiff_t bufsize = 0;
      static char *symbuf = 0;
      ptrdiff_t i = 0;
      do {
          /* If buffer is full, make it bigger. */
          if (bufsize <= i)
            {
              bufsize = 2 * bufsize + 40;
              symbuf = realloc (symbuf, (size_t) bufsize);
            }
          /* Add this character to the buffer. */
          symbuf[i++] = (char) c;
          /* Get another character. */
          c = getchar ();
        } while (isalnum (c));

      ungetc (c, stdin);
      symbuf[i] = '\0';
      symrec *s = getsym (symbuf);
      if (!s)
        s = putsym (symbuf, VAR);
      yylval.VAR = s; /* or yylval.FUN = s. */
      return s->type;
    }

  /* Any other character is a token by itself. */
  return c;
}

/* Called by yyparse on error. */
void yyerror (char const *s)
{
  fprintf (stderr, "%s\n", s);
}

int main (int argc, char const* argv[])
{
  /* Enable parse traces on option -p. */
  if (argc == 2 && strcmp(argv[1], "-p") == 0)
    yydebug = 1;
  init_table();
  return yyparse ();
}
