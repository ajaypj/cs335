package main;

import "fmt";

func main() {
  var x,y int;
  // x = 0*0 + (1*1 + (2*2 + (3*3 + (4*4 + (5*5 + (6*6 + 7*7))))));
  y = 4 - (x*5);
  x = y;
	// fmt.Println(x);
  return;
};
