// WARNING: The files in this directory have not been extensively tested
//   and may be incorrect. --JTB

void main() {
    int a = 1;
    int b = 3;
    int c = 5;
    int N = __VERIFIER_nondet_int();
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
