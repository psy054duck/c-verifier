
void main() {
    int a = 1;
    int b = 3;
    int c = 5;
    int N = __VERIFIER_nondet_int();
    for(int t = 0; t < N; t++) {
        if (a == 1) {
            b += a;
            c += 1;
            a = -1;
        } else if (a == -1) {
            b += a;
            c -= 1;
            a = 1;
        } else {
            a = a; b = b; c = c;
        }
    }
    __VERIFIER_assert(c - b == 2);
}
