package main;
import "fmt";

type person struct {
    a int;
    b int;
};

func get(s person) int {
	return s.a;
};

func main() {
	var b int;
	var a int;
  var k person;
	k.a = 200;
  a = get(k);
  print(a);
  return;
};
