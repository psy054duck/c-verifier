int main() {
    int k, y, x, c;
    k = __VERIFIER_nondet_int();

    y = 0;
    x = 0;
    c = 0;

    while (c < k) {
        // __VERIFIER_assert(6*x - 2*y*y*y - 3*y*y - y == 0);

        c = c + 1;
        y = y + 1;
        x = y * y + x;
    }
    __VERIFIER_assert(6*x - 2*y*y*y - 3*y*y - y == 0);
    return 0;
}
