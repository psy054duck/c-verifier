int main()
{
  int a;
  int b;
  int p;
  int q;
  int r;
  int s;
  int x;
  int y;
  x = __VERIFIER_nondet_int();
  y = __VERIFIER_nondet_int();
  if ((x < 1) || (y < 1))
    return 0;
  a = x;
  b = y;
  p = 1;
  q = 0;
  r = 0;
  s = 1;
  while (a != b)
  {
    if (a > b)
    {
      a = a - b;
      p = p - q;
      r = r - s;
    }
    else
    {
      b = b - a;
      q = q - p;
      s = s - r;
    }
  }

  __VERIFIER_assert((a - b) == 0);
  __VERIFIER_assert((((p * x) + (r * y)) - b) == 0);
  __VERIFIER_assert((((q * r) - (p * s)) + 1) == 0);
  __VERIFIER_assert((((q * x) + (s * y)) - b) == 0);
  return 0;
}

