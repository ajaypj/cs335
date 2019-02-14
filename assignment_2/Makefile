all:
	python lexer.py --in tests/func.go --out out.go
	python parser.py --in out.go > dot.txt
	dot -Tpng dot.txt > new.png
clean:
	rm new.png
	rm out.go
