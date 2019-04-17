package main;

import "fmt";

func binarySearch(arr [5]int, l,r,x int) int {
	if r >= l {
		mid := l + (r-l)/2;
    if arr[mid] == x {
			return mid;
    };
		if arr[mid] > x {
			return binarySearch(arr, l, mid-1, x);
    };
		return binarySearch(arr, mid+1, r, x);
	};
	return -1;
};

func main() {
  var input [5]int;
  input[0] = 1;
  input[1] = 2;
  input[2] = 3;
  input[3] = 4;
  input[4] = 5;

  x := 40;
	res := binarySearch(input, 0, 4, x);
  print(res);
	return;
};
