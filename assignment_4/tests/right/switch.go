// _Switch statements_ express conditionals across many
// branches.

package main;

import "fmt";
import "time";

func main() {
  // Here's a basic `switch`.
  var i int;
  i=2;
  var a,b,c int;
  a=10;
  b=6;

  switch (i) {
  case 1:
      c=a+b;
  case 2:
      c=a-b;
  case 3:
      c=a*b;
  };

  return;
};
