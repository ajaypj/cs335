// _Switch statements_ express conditionals across many
// branches.

package main;

import "fmt";
import "time";

func main() {
  // Here's a basic `switch`.
  var i,c int;
  i = 2;
  switch (i) {
    case 1:
      c = 10;
    case 2:
      c = 20;
    case 3:
      c = 30;
  };

  print(c);
  return;
};
