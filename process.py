import re
import argparse

parser = argparse.ArgumentParser(description="argument parser")
parser.add_argument("--cfg", help='Specify CFG', required=True)
parser.add_argument("--out", help='Specify output file', required=True)
args = vars(parser.parse_args())

data = '''
 3 + 4 * 10
   + -20 *2
 '''

def get_cfg(cfg_file):
	cfg=open(cfg_file)
	tokencolour = dict()
	line=cfg.readline()
	while line:
		token_col=line.split()
		# print(token_col)
		tokencolour[token_col[0]]=token_col[1]
		line=cfg.readline()
	return tokencolour

tokencolour= get_cfg(args["cfg"])

# tokencolour = {"NUMBER":"red", "OPERATOR":"blue", "IDENTIFIER":"green", "KEYWORD":"black", "SPECIAL":"yellow"}
ignored = ["SPACE", "NEWLINE"]

operators = ["ADD","SUB","MUL","QUO","REM",	"AND","OR","XOR","SHL"   ,"SHR"   ,"AND_NOT","ADD_ASSIGN","SUB_ASSIGN","MUL_ASSIGN","QUO_ASSIGN","REM_ASSIGN",	"AND_ASSIGN"    ,"OR_ASSIGN"     ,"XOR_ASSIGN"    ,"SHL_ASSIGN"    ,"SHR_ASSIGN"    ,"AND_NOT_ASSIGN" ,"LAND","LOR" ,"ARROW",	"INC" ,"DEC",	"EQL"  ,"LSS"  ,"GTR"  ,"ASSIGN",	"NOT",	"NEQ"    ,"LEQ"    ,"GEQ"    ,"DEFINE" ,"ELLIPSIS",
	"LPAREN","LBRACK","LBRACE","COMMA ","PERIOD",	"RPAREN","RBRACK","RBRACE","SEMICOLON","COLON"]

identifiers = ["IDENT","INT"  ,"FLOAT","IMAG" ,"CHAR" ,"STRING" ]

keywords = ["BREAK","CASE","CHAN","CONST","CONTINUE","DEFAULT","DEFER","ELSE","FALLTHROUGH","FOR","FUNC","GO","GOTO","IF","IMPORT","INTERFACE","MAP","PACKAGE","RANGE","RETURN","SELECT","STRUCT","SWITCH","TYPE","VAR"]

specials = ["ILLEGAL","EOF","COMMENT"]

f = open("output.txt")
datalist = list()
line=f.readline()

while(line):
	# print(line)
	datalist.append(line)
	line=f.readline()

pos = list()

for i in range(len(datalist)):
	start=datalist[i].find('(')
	end=datalist[i].find(')')
	positions = datalist[i][start+1:end].split(',')
	if "'" in positions[1]:
		positions[1] = positions[1].replace("'","")
		positions[1] = positions[1].replace('"',"")
	pos.append(positions)
	# print(positions)

for i in range(len(pos)):
	token_name = pos[i][0]
	if token_name=="NUMBER":
		pos[i].append(tokencolour["NUMBER"])
	else:
		if token_name in ignored:
			pos[i].append(token_name)
		elif token_name in operators:
			pos[i].append(tokencolour["OPERATOR"])
		elif token_name in identifiers:
			pos[i].append(tokencolour["IDENTIFIER"])
		elif token_name in keywords:
			pos[i].append(tokencolour["KEYWORD"])
		elif token_name in specials:
			pos[i].append(tokencolour["SPECIAL"])

text = '<font color="{}">{}</font>'
# print(text)

nf=open(args["out"],"w")
for i in pos:
	if i[-1]=="SPACE":
		nf.write("&nbsp;")
	elif i[-1]=="NEWLINE":
		nf.write("<br>")
	else:		
		string = text.format(i[-1], i[1])
		nf.write(string)