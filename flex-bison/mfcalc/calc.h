#ifndef _CALC_H_
#define _CALC_H_

#include <math.h>

typedef double (func_t) (double);

struct symrec {
    char *name;
    int type;
    union {
        double var;
        func_t *fun;
    } value;
    struct symrec *next;
};

typedef struct symrec symrec;

symrec *sym_table;

symrec *putsym(char const *name, int sym_type);
symrec *getsym(char const *name);

struct init {
    char const *name;
    func_t *fun;
};

struct init const funs[] = {
    {"sin", sin},
    {"cos", cos},
    {"exp", exp},
    {"log", log},
    {"sqrt", sqrt},
    {0, 0}
};

static void init_table(void);


#endif