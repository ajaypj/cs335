python lexer.py --in $1 --out out.go
python parser.py --in out.go > dot.txt
dot -Tps dot.txt > $2
