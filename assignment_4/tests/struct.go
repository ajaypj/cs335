package main;
import "fmt";

type person struct {
  a int;
  b int;
};

func main() {
	var b int;
  	var a int;
    var k person;

    k.a = 2;
    a = k.a;

    print(a);
    return;
};
