#############################################################
To run the parser, do:

	$cd src
	$python parser.py --in=../tests/right/4.go --out=ir.txt > table.txt
	$make clean

The output symbol tables are written in "table.txt" and the 3-address code is written in "ir.txt".
