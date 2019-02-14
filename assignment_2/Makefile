all:
	python lexer.py --in testajay/test1.go --out out.go
	python parser.py --in out.go > dot.txt
	dot -Tps dot.txt > ast.ps
clean:
	rm *.ps
	rm out.go
