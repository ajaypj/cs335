package main;

import "fmt";

// var input [10]int = [10]int{1,3,2,4,8,6,7,2,3,0};

func main() {
  var input [5]int;
  input[0]=5;
  input[1]=4;
  input[2]=3;
  input[3]=2;
  input[4]=1;
  n := 5;
  for i:=0;i<n;i++{
    for j:=0;j<n-1;j++{
      if input[j]>input[j+1]{
        temp:=input[j];
        input[j]=input[j+1];
        input[j+1]=temp;
      };
    };
  };
  for k:=0;k<n;k++{
    res := input[k];
    print(res);
  };
  return;
};
