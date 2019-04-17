package main;
import "fmt";
func even(n int) int;

func odd(n int) int{
	if n==0 {
		return 0;
	} else {
		return even(n-1);
	};
};

func even(n int) int{
	if n==0 {
		return 1;
	} else {
		return odd(n-1);
	};
};

func main(){
	n := 13;
	b := even(n);
	print(b);
	return;
};
