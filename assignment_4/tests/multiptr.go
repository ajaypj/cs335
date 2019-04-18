package main;

import "fmt";

func main() {
  var a int = 10;
  var p *int;
  var pp **int;

  p = &a;
  pp = &p;
  **pp = 2;
  print(a);
  return;
};
