package main;

import "fmt";

type S struct {
  x, y int;
  z *S;
};

// func sum(s S, a [3]int) int {
// 	return s.x + s.y;
// };

func main() {
  // var example S;
  var S [3]int;

  i := 2;
  S[i] = 0;
  // j := S[2];

  // example.x = 2;
  // example.y = 1;

  // S[0] = sum(example, S);
  return;
};
