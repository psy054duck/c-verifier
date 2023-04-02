int main() {
    int X, Y;
    long long x, y, v, xy, yx;
    X = __VERIFIER_nondet_int();
    Y = __VERIFIER_nondet_int();
    v = (2 * Y) - X;         // cast required to avoid int overflow
    y = 0;
    x = 0;

    while (x > X) {
        if (v < 0) {
            v = v + 2 * Y;
        } else {
            v = v + 2 * (Y - X);
            y++;
        }
        x++;
    }
    xy = x*y;
    yx = Y*x;
    __VERIFIER_assert(2*yx - 2*xy - X + 2*Y - v + 2*y == 0);

    return 0;
}