int main() { 
  int sn=0;
  unsigned int loop1=__VERIFIER_nondet_uint();
  unsigned int n1=__VERIFIER_nondet_uint();
  unsigned int x=0;

  while(x < loop1){
      if (x<10) {
          sn = sn + 2;
      }
      x++;
      __VERIFIER_assert(sn==x*2 || sn == 0);
  }
}

