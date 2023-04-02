int main() {
    unsigned a, b;
    unsigned x, y, u, v;
    a = __VERIFIER_nondet_uint();
    b = __VERIFIER_nondet_uint();
    // assume_abort_if_not(a >= 1); //inf loop if remove
    // assume_abort_if_not(b >= 1);

    // assume_abort_if_not(a <= 65535);
    // assume_abort_if_not(b <= 65535);

    if (a < 1 || b < 1 || a > 65535 || b > 65535) return 0;

    x = a;
    y = b;
    u = b;
    v = a + 1;

    while (x != y) {

        if (x > y) {
            x = x - y;
            v = v + u;
        } else {
            y = y - x;
            u = u + v;
        }
    }

    __VERIFIER_assert(x*u + y*v == 2*a*b);
    // x == gcd(a,b)
    //(u + v)/2==lcm(a,b)

    return 0;
}