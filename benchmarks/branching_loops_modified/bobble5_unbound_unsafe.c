// WARNING: The files in this directory have not been extensively tested
//   and may be incorrect. --JTB

void main() {
    int a;
    int b;
    int c;
    int _N = __VERIFIER_nondet_int();
    if (!(c - b == 2)) return 0;
    for(int t = 0; t < N; t++) {
        if (a > 0) {
            b += a;
            c += 1;
        } else {
            if (a < 0) {
                b += a;
                c -= 1;
            } else {
                c = c;
            }
        }
        a = -a;
    }
    __VERIFIER_assert(c - b == 2);
}
