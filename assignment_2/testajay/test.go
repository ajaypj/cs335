package main

import (
	"fmt"
	"time"
	"math/rand"
	"math/cmplx"
	"math"
	"runtime"
	"strings"
	"golang.org/x/tour/wc"
)

func add1(x int, y int) int {
	fmt.Println("add1 ")
	return x + y
}

func add2(x, y int) int {
	fmt.Println("add2 ")
	return x + y
}

func swap(x, y string) (string, string) {
	return y, x
}

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func needInt(x int) int { return x*10 + 1 }
func needFloat(x float64) float64 {
	return x * 0.1
}

var c, python, java bool

var i1, j1 int = 1, 2

var (
	ToBe   bool       = false
	MaxInt uint64     = 1<<64 - 1
	z      complex128 = cmplx.Sqrt(-5 + 12i)
)

const (
	// Create a huge number by shifting a 1 bit left 100 places.
	// In other words, the binary number that is 1 followed by 100 zeroes.
	Big = 1 << 100
	// Shift it right again 99 places, so we end up with 1<<1, or 2.
	Small = Big >> 99
)

func sqrt(x float64) string {
	if x < 0 {
		return sqrt(-x) + "i"
	}
	return fmt.Sprint(math.Sqrt(x))
}

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	}
	return lim
}

func pow2(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	} else {
		fmt.Printf("%g >= %g\n", v, lim)
	}
	// can't use v here, though
	return lim
}

type Vertex struct {
	X int
	Y int
}

var (
	v3 = Vertex{1, 2}  // has type Vertex
	v4 = Vertex{X: 1}  // Y:0 is implicit
	v5 = Vertex{}      // X:0 and Y:0
	p3  = &Vertex{1, 2} // has type *Vertex
)

func printSlice(s []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}

func printSlice1(s string, x []int) {
	fmt.Printf("%s len=%d cap=%d %v\n",
		s, len(x), cap(x), x)
}

var pow3 = []int{1, 2, 4, 8, 16, 32, 64, 128}

type Vertex2 struct {
	Lat, Long float64
}

var m map[string]Vertex2

var m1 = map[string]Vertex2{
	"Bell Labs": Vertex2{
		40.68433, -74.39967,
	},
	"Google": Vertex2{
		37.42202, -122.08408,
	},
}

var m2 = map[string]Vertex2{
	"Bell Labs": {40.68433, -74.39967},
	"Google":    {37.42202, -122.08408},
}

func WordCount(s string) map[string]int {
	return map[string]int{"x": 1}
}

func compute(fn func(float64, float64) float64) float64 {
	return fn(3, 4)
}

func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

type MyFloat float64

func (f MyFloat) Abs() float64 {
	if f < 0 {
		return float64(-f)
	}
	return float64(f)
}


func main() {
	fmt.Println("Welcome to the playground!")

	fmt.Println("The time is", time.Now())

	fmt.Println("My favorite number is", rand.Intn(10))

	fmt.Printf("Now you have %g problems.\n", math.Sqrt(7))

	fmt.Println(math.Pi)

	fmt.Println(add1(42, 13))

	fmt.Println(add2(42, 13))

	a, b := swap("hello", "world")
	fmt.Println(a, b)

	fmt.Println(split(17))

	var i int
	fmt.Println(i, c, python, java)

	var c1, python1, java1 = true, false, "no!"
	fmt.Println(i1, j1, c1, python1, java1)

	c2, python2, java2 := true, false, "no!"
	fmt.Println(c2, python2, java2)

	fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
	fmt.Printf("Type: %T Value: %v\n", MaxInt, MaxInt)
	fmt.Printf("Type: %T Value: %v\n", z, z)

	var s string
	fmt.Printf("%q\n",s)

	var x, y int = 3, 4
	var f float64 = math.Sqrt(float64(x*x + y*y))
	var z1 uint = uint(f)
	fmt.Println(x, y, z1)

	v := 42 // change me!
	fmt.Printf("v is of type %T\n", v)

	const World = "世界"
	fmt.Println("Hello", World)

	const Truth = true
	fmt.Println("Go rules?", Truth)

	fmt.Println(needInt(Small))
	fmt.Println(needFloat(Small))
	fmt.Println(needFloat(Big))

	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}
	fmt.Println(sum)

	sum = 1
	for ; sum < 1000; {
		sum += sum
	}
	fmt.Println(sum)

	sum = 1
	for sum < 1000 {
		sum += sum
	}
	fmt.Println(sum)

	// infinite loop
	// for {
	// }

	fmt.Println(sqrt(2), sqrt(-4))

	fmt.Println(
		pow(3, 2, 10),
		pow(3, 3, 20),
	)

	fmt.Println(
		pow2(3, 2, 10),
		pow2(3, 3, 20),
	)

	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.", os)
	}	

	fmt.Println("When's Saturday?")
	today := time.Now().Weekday()
	switch time.Saturday {
	case today + 0:
		fmt.Println("Today.")
	case today + 1:
		fmt.Println("Tomorrow.")
	case today + 2:
		fmt.Println("In two days.")
	default:
		fmt.Println("Too far away.")
	}

	t := 5
	switch {
	case t < 12:
		fmt.Println("Good morning!")
	case t < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}

	defer fmt.Println("defer is working")

	fmt.Println("hello")

	fmt.Println("counting")

	for i := 0; i < 10; i++ {
		defer fmt.Println("defer", i)
	}

	fmt.Println("done")

	i2, j2 := 42, 2701

	p := &i2         // point to i
	fmt.Println(*p) // read i through the pointer
	*p = 21         // set i through the pointer
	fmt.Println(i2)  // see the new value of i

	p1 := &j2         // point to j
	*p1 = *p1 / 37   // divide j through the pointer
	fmt.Println(j2) // see the new value of j

	fmt.Println(Vertex{1, 2})

	v1 := Vertex{1, 2}
	v1.X = 4
	fmt.Println(v1.X)

	v2 := Vertex{1, 2}
	p2 := &v2
	p2.X = 1e9
	fmt.Println(v2)

	fmt.Println(v3, p2, v4, v5)

	var a1 [2]string
	a1[0] = "Hello"
	a1[1] = "World"
	fmt.Println(a1[0], a1[1])
	fmt.Println(a1)

	primes := [6]int{2, 3, 5, 7, 11, 13}
	fmt.Println(primes)

	primes1 := [6]int{2, 3, 5, 7, 11, 13}

	var s6 []int = primes1[1:4]
	fmt.Println(s6)

	names := [4]string{
		"John",
		"Paul",
		"George",
		"Ringo",
	}
	fmt.Println(names)

	a2 := names[0:2]
	b2 := names[1:3]
	fmt.Println(a, b)

	b2[0] = "XXX"
	fmt.Println(a2, b2)
	fmt.Println(names)

	q := []int{2, 3, 5, 7, 11, 13}
	fmt.Println(q)

	r := []bool{true, false, true, true, false, true}
	fmt.Println(r)

	s1 := []struct {
		i int
		b bool
	}{
		{2, true},
		{3, false},
		{5, true},
		{7, true},
		{11, false},
		{13, true},
	}
	fmt.Println(s1)

	s2 := []int{2, 3, 5, 7, 11, 13}

	s7 := s2[1:4]
	fmt.Println(s7)

	s7 = s2[:2]
	fmt.Println(s7)

	s7 = s2[1:]
	fmt.Println(s7)

	s3 := []int{2, 3, 5, 7, 11, 13}
	printSlice(s3)

	// Slice the slice to give it zero length.
	s8 := s3[:0]
	printSlice(s8)

	// Extend its length.
	s8 = s3[:4]
	printSlice(s8)

	// Drop its first two values.
	s8 = s3[2:]
	printSlice(s8)

	var s4 []int
	fmt.Println(s4, len(s4), cap(s4))
	if s4 == nil {
		fmt.Println("nil!")
	}

	a3 := make([]int, 5)
	printSlice1("a", a3)

	b3 := make([]int, 0, 5)
	printSlice1("b", b3)

	c3 := b3[:2]
	printSlice1("c", c3)

	d3 := c3[2:5]
	printSlice1("d", d3)

	// Create a tic-tac-toe board.
	board := [][]string{
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
	}

	// The players take turns.
	board[0][0] = "X"
	board[2][2] = "O"
	board[1][2] = "X"
	board[1][0] = "O"
	board[0][2] = "X"

	for i := 0; i < len(board); i++ {
		fmt.Printf("%s\n", strings.Join(board[i], " "))
	}

	var s5 []int
	printSlice(s5)

	// append works on nil slices.
	s5 = append(s5, 0)
	printSlice(s5)

	// The slice grows as needed.
	s5 = append(s5, 1)
	printSlice(s5)

	// We can add more than one element at a time.
	s5 = append(s5, 2, 3, 4)
	printSlice(s5)

	for i, v := range pow3 {
		fmt.Printf("2**%d = %d\n", i, v)
	}

	pow4 := make([]int, 10)
	for i := range pow4 {
		pow4[i] = 1 << uint(i) // == 2**i
	}
	for _, value := range pow4 {
		fmt.Printf("%d\n", value)
	}

	m = make(map[string]Vertex2)
	m["Bell Labs"] = Vertex2{
		40.68433, -74.39967,
	}
	fmt.Println(m["Bell Labs"])

	fmt.Println(m1)

	fmt.Println(m2)

	m3 := make(map[string]int)

	m3["Answer"] = 42
	fmt.Println("The value:", m3["Answer"])

	m3["Answer"] = 48
	fmt.Println("The value:", m3["Answer"])

	delete(m3, "Answer")
	fmt.Println("The value:", m3["Answer"])

	v6, ok := m3["Answer"]
	fmt.Println("The value:", v6, "Present?", ok)

	wc.Test(WordCount)

	hypot := func(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
	}
	fmt.Println(hypot(5, 12))

	fmt.Println(compute(hypot))
	fmt.Println(compute(math.Pow))

	pos, neg := adder(), adder()
	for i := 0; i < 10; i++ {
		fmt.Println(
			pos(i),
			neg(-2*i),
		)
	}

	f := MyFloat(-math.Sqrt2)
	fmt.Println(f.Abs())
}
