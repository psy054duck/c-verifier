
extern void abort(void);
extern void __assert_fail(const char *, const char *, unsigned int, const char *) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__));
void reach_error() { __assert_fail("0", "iftelse.c", 4, "reach_error"); }
extern void abort(void);
void assume_abort_if_not(int cond) {
  if(!cond) {abort();}
}
void __VERIFIER_assert(int cond) {
  if (!(cond)) {
    ERROR: {reach_error();abort();}
  }
  return;
}
unsigned int __VERIFIER_nondet_uint();
int main() {
  int SIZE = 20000001;
  unsigned int _n = __VERIFIER_nondet_uint();
  unsigned int i = 0;
  unsigned int j = 0;
  unsigned int k = 0;
  if (!(_n <= SIZE)) return 0;
  while( i < _n ) {
    i = i + 3;
    if(i%2 == 1)
	    j = j+3;
    else
	    k = k+3;
    if(_n>0)
	   __VERIFIER_assert( (i<=j*2) );
  }
  return 0;
}

