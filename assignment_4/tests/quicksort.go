package main;

import "fmt";

func partition(a *int, l, h int) int {
	p := *(a+4*h);
	for j:=l; j<h; j++ {
		if *(a+4*j) <= p {
			temp := *(a+4*j);
			*(a+4*j) = *(a+4*l);
			*(a+4*l) = temp;
			l++;
		};
	};
	temp := *(a+4*l);
	*(a+4*l) = *(a+4*h);
	*(a+4*h) = temp;
	return l;
};

func quickSort(a *int, l, h int) {
	if l > h {
		return;
	};
	p := partition(a, l, h);
	quickSort(a, l, p-1);
	quickSort(a, p+1, h);
	return;
};

func main() {
	var list [4]int;
	list[0] = 10;
	list[1] = 9;
	list[2] = 8;
	list[3] = 7;
	var a *int;
	a = &list;
	quickSort(a, 0, 3);
	for k:=0; k<4; k++ {
    res := list[k];
    print(res);
  };
	return;
};
