// WARNING: The files in this directory have not been extensively tested
//   and may be incorrect. --JTB

void main(int L) {
    int x;
    int y;
    if ((x - y) * (x - y) != 1) return 0;
    for(int t = 0; t < L; t++) {
        if (x > y) {
            y = y + 2; 
        } else { 
            x = x + 2; 
        }
    }
    __VERIFIER_assert((x - y) * (x - y) == 1);
}
