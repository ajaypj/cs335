package main;

import "fmt";

func partition(a [4]int, lo, hi int) int {
	p := a[hi];
	for j := lo; j < hi; j++ {
		if a[j] < p {
			tmp := a[j];
			a[j] = a[lo];
			a[lo] = tmp;
			lo++;
		};
	};
	tmp := a[lo];
	a[lo] = a[hi];
	a[hi] = tmp;
	return lo;
}

func quickSort(a [4]int, lo, hi int) {
	if lo > hi {
		return;
	}
	p := partition(a, lo, hi);
	quickSort(a, lo, p-1);
	quickSort(a, p+1, hi);
}

func main() {
	var list [4]int;
	list[0] = 10;
	list[1] = 9;
	list[2] = 8;
	list[3] = 7;
	quickSort(list, 0, 4);
	return;
}
