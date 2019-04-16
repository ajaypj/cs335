package main;
import "fmt";

func ret_arr(a [3]int) int{
	return a[2];
};

func main(){
	var a [3]int;
	a[0] = 10;
	a[1] = 20;
	a[2] = 30;
	b := ret_arr(a);
	print(b);
	return;
};
