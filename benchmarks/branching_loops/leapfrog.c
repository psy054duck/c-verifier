// WARNING: The files in this directory have not been extensively tested
//   and may be incorrect. --JTB

void main(int N) {
    int x = 2;
    int y = 1;
    for(int t = 0; t < N; t++) {
        if (x > y) {
            y = y + 2; 
        } else { 
            x = x + 2; 
        }
    }
    __VERIFIER_assert((x - y) * (x - y) == 1);
}
