int main() {
    int X, Y;
    int v, x, y;
    X = __VERIFIER_nondet_int();
    Y = __VERIFIER_nondet_int();
    v = 2 * Y - X;
    y = 0;
    x = 0;

    while (x <= X) {
	// __VERIFIER_assert(2*Y*x - 2*X*y - X + 2*Y - v == 0);
        // out[x] = y

        if (v < 0) {
            v = v + 2 * Y;
        } else {
            v = v + 2 * (Y - X);
            y++;
        }
        x++;
    }
    __VERIFIER_assert(2*Y*x - 2*x*y - X + 2*Y - v + 2*y == 0);

    return 0;
}
