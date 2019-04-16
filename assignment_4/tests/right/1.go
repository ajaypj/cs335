package main;

import "fmt";

func add(a int, b int) int {
	return a+b;
};

func main() {
	var sum int;
	sum = 0;
	var i int;
	for i = 0; i < 10; i+=1 {
		sum = add(sum, i);
	};
	print(sum);
	return;
};
