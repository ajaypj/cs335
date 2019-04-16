package main;
import "fmt";

func add(a,b,c,d,e,f,g,h,i int) int{
  return (a+b+c+d+e+f+g+h+i);
};

func main(){
  a := (1*1+(2*2+(3*3+(4*4+(5*5+(6*6+7*7+(8*8)))))));
  print(a);
  b:= add (1,2,3,4,5,6,7,8,9);
  print(b);
  return;
};
