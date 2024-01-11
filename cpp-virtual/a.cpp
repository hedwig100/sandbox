#include <stdio.h>

class C {
 int f() {return 0;}
 virtual int g() {return 0;}
};
class D: C {
 int f() {return 1;}
virtual int g() {return 1;}
};
int main() {
 C* pc = new C();
 C* pd = new D();
 printf(“%d %d %d %d¥n”,
 pc->f(), pc->g(),
 pd->f(), pd->g());
}
