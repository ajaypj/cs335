package main;

import "fmt";

func main() {
  var a int = 10;
  var p *int;
  var pp **int;
  var ppp ***int;

  p = &a;
  pp = &p;
  ppp = &pp;
  ***ppp = 2;
  print(a);
  return;
};
