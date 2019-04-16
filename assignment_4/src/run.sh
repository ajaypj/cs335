python parser.py --in=../tests/right/$1 --out=ir.txt > table.txt
python3 gen.py > code.s
gcc code.s -m32 -no-pie -o code.out
./code.out
# make clean
