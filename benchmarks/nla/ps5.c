int main() {
    int k, y, x, c;
    k = __VERIFIER_nondet_int();

    y = 0;
    x = 0;
    c = 0;

    while (c < k) {
        // __VERIFIER_assert(6*y*y*y*y*y + 15*y*y*y*y + 10*y*y*y - 30*x - y == 0);

        c = c + 1;
        y = y + 1;
        x = y * y * y * y + x;
    }

    __VERIFIER_assert(6*y*y*y*y*y + 15*y*y*y*y + 10*y*y*y - 30*x - y == 0);
    __VERIFIER_assert(k*y == y*y);
    return 0;
}
