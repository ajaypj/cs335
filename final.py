import re
import argparse

import ply.lex as lex

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

#################################   Keywords

reserved = {
    'break' : 'KEY',
    'default' : 'KEY',
    'func' : 'KEY',
    'interface' : 'KEY',
    'select' : 'KEY',
    'case' : 'KEY',
    'defer' : 'KEY',
    'go' : 'KEY',
    'map' : 'KEY',
    'struct' : 'KEY',
    'chan' : 'KEY',
    'else' : 'KEY',
    'goto' : 'KEY',
    'package' : 'KEY',
    'switch' : 'KEY',
    'const' : 'KEY',
    'fallthrough' : 'KEY',
    'if' : 'KEY',
    'range' : 'KEY',
    'type' : 'KEY',
    'continue' : 'KEY',
    'for' : 'KEY',
    'import' : 'KEY',
    'return' : 'KEY',
    'var' : 'KEY',
}

tokens = ['NUM','STR','OP','ID','KEY','COM','FUNC']# + list(reserved.values())

################################### Operators and delimiters
OP1 = r'\+|-|\*|/|%'
OP2 = r'\&|\||\^|<<|>>|\&\^'
OP3 = r'\+=|-=|\*=|/=|%='
OP4 = r'\&=|\|=|\^=|<<=|>>=|\&\^='
OP5 = r'\&\&|\|\||<-|\+\+|--'
OP6 = r'==|<|>|=|!'
OP7 = r'!=|<=|>=|:=|\.\.\.'
OP8 = r'\(|\[|\{|,|\.'
OP9 = r'\)|\]|\}|;|:'

t_OP = OP1+'|'+OP2+'|'+OP3+'|'+OP4+'|'+OP5+'|'+OP6+'|'+OP7+'|'+OP8+'|'+OP9



##################################### Numbers


decimal_lit = r'[1-9][\d]*'
octal_lit = r'0[0-7]+'
hexal_lit = r'0[xX][\dA-F]+'
int_lit = '('+decimal_lit+')|('+octal_lit+')|('+hexal_lit+')'

decimals = r'[0-9]+'
exponent = r'[eE][+-]?[0-9]+'
float_lit = '('+decimals+'\.'+decimals+exponent+')|('+decimals+exponent+')|('+decimals+'\.'+decimals+')'
imag_lit = '(('+decimals+')|('+float_lit+'))'+'i'

t_NUM = '('+float_lit+')|('+imag_lit+')|('+int_lit+')'



###################################### Strings


char = r'\'[^\']\''
string = r'\"[^\"]*\"'

t_STR = '('+string+')|('+char+')'



###################################### Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_\d]*'
    t.type = reserved.get(t.value,'ID')
    return t


###################################### Special/Comment


def t_COM(t):
    r'(/\*(.|\n)*\*/)|(//.*\n)'
    return t

####################################### Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

####################################### A string containing ignored characters
####################################### (spaces and tabs)


t_ignore  = ' \t'

####################################### Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

####################################### Build the lexer
lexer = lex.lex()

#######################################    HTML PART    ###########################
#######################################                 ########################

data = '''
3 + 0x4234</if() * 10i if dsgsfns""djs//
+ -2.0e6 *2 "hf/*a"ff"fgafg"*/
'''

lexer.input(data)

f = open(args["out"], "w")
f.write("<html><body>")
pos = 0

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

    l = len(str(tok.value))
    for i in xrange(pos, tok.lexpos):
        if data[i] == ' ':
            f.write("&nbsp;")
        elif data[i] == '\n':
            f.write("<br>")
    pos = tok.lexpos + l
    # print(pos)
    f.write("<font color=\""+tokencolour[str(tok.type)]+"\">"+str(tok.value)+"</font>")
    if tok.type == 'COM':
        for i in xrange(tok.lexpos, pos):
            if data[i] == ' ':
                f.write("&nbsp;")
            elif data[i] == '\n':
                f.write("<br>")
            else:
                f.write(data[i])
        f.write("</font>")

f.write("</body></html>")



############################# Debugging issues
'''
    // after // should be Comment and not string, check regex of single line comment

'''
