int main() { 
  int i, n=__VERIFIER_nondet_uint(), sn=0;
  for(i=1; i<=n; i++) {
    if (i<10)
    sn = sn + 2;
  }
  __VERIFIER_assert(sn==n*2 || sn == 0);
}
