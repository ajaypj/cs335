package main;

import "fmt";

func ackermann(m, n int) int {
	if m == 0 {
		return n + 1;
	}	else if m > 0 {
		if n==0 {
			return ackermann(m-1, 1);
		};
	};
	return ackermann(m-1, ackermann(m, n-1));
};

func main() {
	a:= ackermann(1, 2);
	print(a);
	return;
};
