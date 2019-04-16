package main;

import "fmt";

type S struct {
  x, y int;
  z *S;
};

func sum(s S, a [3]int) int {
	return s.x + s.y + a[2] + a[1];
};

func main() {
  var example S;
  var S [3]int;

  i := 2;
  S[i] = 10;
  S[1] = 10;

  example.x = 5;
  example.y = 5;

  S[0] = sum(example, S);
  res := S[0];
  print(res);
  return;
};
