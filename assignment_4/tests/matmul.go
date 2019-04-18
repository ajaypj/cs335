package main;

import "fmt";

func main() {
	var mat, A, B [2][2]int;
  // mat[1][1] = 10;
  // res := mat[1][1];
  // print(res);
  for a := 0; a < 2; a++ {
    for k := 0; k < 2; k++ {
      input := 0;
      scan(input);
      A[a][k] = input;
    };
  };
  for b := 0; b < 2; b++ {
    for k := 0; k < 2; k++ {
      input := 0;
      scan(input);
      B[b][k] = input;
    };
  };

  sum := 0;
  for c := 0; c < 2; c++ {
    for d := 0; d < 2; d++ {
      for k := 0; k < 2; k++ {
        sum = sum + A[c][k] * B[k][d];
      };
      mat[c][d] = sum;
      sum = 0;
    };
  };
  for i := 0; i < 2; i++ {
    for j := 0; j < 2; j++ {
      res := mat[i][j];
      print(res);
    };
  };
	return;
};
