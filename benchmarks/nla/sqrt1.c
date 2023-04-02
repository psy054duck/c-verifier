int main() {
    int n, a, s, t;
    n = __VERIFIER_nondet_int();

    a = 0;
    s = 1;
    t = 1;

    while (s <= n) {
        // __VERIFIER_assert(t == 2*a + 1);
        // __VERIFIER_assert(s == (a + 1) * (a + 1));
	// __VERIFIER_assert(t*t - 4*s + 2*t + 1 == 0);
        // the above 2 should be equiv to 

        a = a + 1;
        t = t + 2;
        s = s + t;
    }
    
    __VERIFIER_assert(t == 2 * a + 1);
    __VERIFIER_assert(s == (a + 1) * (a + 1));
    __VERIFIER_assert(t*t - 4*s + 2*t + 1 == 0);

    return 0;
}

