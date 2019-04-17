package main;

import "fmt";

func get(p *int, i int) {
	*(p+4*i) = 7;
	return;
};

func main() {
	var i int;
  i = 1;
	var arr [2]int;
	arr[0] = 5;
	arr[1] = 6;

  p := &arr;
  get(p, i);
	res := *(p+4);
	print(res);
	return;
};
