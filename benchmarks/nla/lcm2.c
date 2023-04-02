int main() {
    unsigned a, b;
    unsigned x, y, u, v;
    a = __VERIFIER_nondet_uint();
    b = __VERIFIER_nondet_uint();

    if (a < 1 || b < 1 || a > 65535 || b > 65535) return 0;

    x = a;
    y = b;
    u = b;
    v = a;

    while (x != y) {
        // __VERIFIER_assert(x*u + y*v == 2*a*b);

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
