// Iterative version of Fibonacci
package main;
import "fmt";

func fiboI(n int) int {
	var result int;
	first := 0;
	second := 1;
	for i:=1; i<=n; i=i+1 {
		if i==n {
	   		result = first;
	  	};
	  	temp := first;
	  	first = second;
	  	second = temp + second;
	};
	return result;
};

func main() {
	b := fiboI(10);
	print(b);
	return;
};
