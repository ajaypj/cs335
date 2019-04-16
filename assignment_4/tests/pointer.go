package main;

import "fmt";

func main() {
	var i int;
  i = 1;

  var p *int;
  p = &i;

  res := *p;
	print(res);
	return;
};
