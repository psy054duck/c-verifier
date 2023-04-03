int main() {
    int a, b;
    int x, y, z;

    a = __VERIFIER_nondet_double();
    b = __VERIFIER_nondet_double();
    if (b < 1) return 0;

    x = a;
    y = b;
    z = 0;

    while (y != 0) {
        // __VERIFIER_assert(z + x * y == a * b);

        if (y % 2 == 1) {
            z = z + x;
            y = y - 1;
        }
        x = 2 * x;
        y = y / 2;
        a = a;
        b = b;
    }
    __VERIFIER_assert(z == a * b);
    
    return 0;
}
