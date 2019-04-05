package main;

import "fmt";

func add(a int, b int) int {
	return a+b;
};

func main() {
	var sum int;
	sum = 0;
	var i int;
	for i = 0; i < 10; i++ {
		var v int;
		v = 0;
		if v != 2 {
			sum += add(sum, i);
		};
	};
	// fmt.Println(sum);
};
