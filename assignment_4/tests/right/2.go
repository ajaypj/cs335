package main;

import "fmt";

type S struct {
  x, y int;
  z *S;
};

func sum(s S) int {
	return s.x + s.y;
};

func main() {
  var example *S;

  var S int;
  S = 0;

  (*example).x = -2;
  (*example).y = 1;

  if S == 0 {
    var S bool;
  };

	S = sum(*example);
};
