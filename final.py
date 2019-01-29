import re
import argparse
import ply.lex as lex

parser = argparse.ArgumentParser(description = "argument parser")
parser.add_argument("--cfg", help = 'Specify CFG', required = True)
parser.add_argument("--in", help = 'Specify input', required = True)
parser.add_argument("--out", help = 'Specify output file', required = True)
args = vars(parser.parse_args())

def get_cfg(cfg_file):
    cfg = open(cfg_file)
    classcolour = dict()
    line = cfg.readline()
    while line:
    	col = line.split()
    	# print(token_col)
    	classcolour[col[0]] = col[1]
    	line = cfg.readline()
    cfg.close()
    return classcolour

classcolour = get_cfg(args["cfg"])

#################################   Tokens
reserved = {
    'break' : 'BREAK',
    'default' : 'DEFAULT',
    'func' : 'FUNC',
    'interface' : 'INTERFACE',
    'select' : 'SELECT',
    'case' : 'CASE',
    'defer' : 'DEFER',
    'go' : 'GO',
    'map' : 'MAP',
    'struct' : 'STRUCT',
    'chan' : 'CHAN',
    'else' : 'ELSE',
    'goto' : 'GOTO',
    'package' : 'PACKAGE',
    'switch' : 'SWITCH',
    'const' : 'CONST',
    'fallthrough' : 'FALLTHROUGH',
    'if' : 'IF',
    'range' : 'RANGE',
    'type' : 'TYPE',
    'continue' : 'CONTINUE',
    'for' : 'FOR',
    'import' : 'IMPORT',
    'return' : 'RETURN',
    'var' : 'VAR',
}

operators = ['ADD','SUB','MUL','QUO','REM','AND','OR','XOR','SHL','SHR','AND_NOT','ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','QUO_ASSIGN','REM_ASSIGN','AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN','SHL_ASSIGN','SHR_ASSIGN','AND_NOT_ASSIGN','LAND','LOR','ARROW','INC','DEC','EQL','LSS','GTR','ASSIGN','NOT','NEQ','LEQ','GEQ','DEFINE','ELLIPSIS','LPAREN','LBRACK','LBRACE','COMMA','PERIOD','RPAREN','RBRACK','RBRACE','SEMICOLON','COLON']
numbers = ['INT','FLOAT','IMAG']
strings = ['CHAR','STRING']

tokens = operators + numbers + strings + ['ID','COM'] + list(reserved.values())

tokenclass = {
    'ADD' : 'OPERATORS',
    'SUB' : 'OPERATORS',
    'MUL' : 'OPERATORS',
    'QUO' : 'OPERATORS',
    'REM' : 'OPERATORS',
    'AND' : 'OPERATORS',
    'OR' : 'OPERATORS',
    'XOR' : 'OPERATORS',
    'SHL' : 'OPERATORS',
    'SHR' : 'OPERATORS',
    'AND_NOT' : 'OPERATORS',
    'ADD_ASSIGN' : 'OPERATORS',
    'SUB_ASSIGN' : 'OPERATORS',
    'MUL_ASSIGN' : 'OPERATORS',
    'QUO_ASSIGN' : 'OPERATORS',
    'REM_ASSIGN' : 'OPERATORS',
    'AND_ASSIGN' : 'OPERATORS',
    'OR_ASSIGN' : 'OPERATORS',
    'XOR_ASSIGN' : 'OPERATORS',
    'SHL_ASSIGN' : 'OPERATORS',
    'SHR_ASSIGN' : 'OPERATORS',
    'AND_NOT_ASSIGN' : 'OPERATORS',
    'LAND' : 'OPERATORS',
    'LOR' : 'OPERATORS',
    'ARROW' : 'OPERATORS',
    'INC' : 'OPERATORS',
    'DEC' : 'OPERATORS',
    'EQL' : 'OPERATORS',
    'LSS' : 'OPERATORS',
    'GTR' : 'OPERATORS',
    'ASSIGN' : 'OPERATORS',
    'NOT' : 'OPERATORS',
    'NEQ' : 'OPERATORS',
    'LEQ' : 'OPERATORS',
    'GEQ' : 'OPERATORS',
    'DEFINE' : 'OPERATORS',
    'ELLIPSIS' : 'OPERATORS',
    'LPAREN' : 'OPERATORS',
    'LBRACK' : 'OPERATORS',
    'LBRACE' : 'OPERATORS',
    'COMMA' : 'OPERATORS',
    'PERIOD' : 'OPERATORS',
    'RPAREN' : 'OPERATORS',
    'RBRACK' : 'OPERATORS',
    'RBRACE' : 'OPERATORS',
    'SEMICOLON' : 'OPERATORS',
    'COLON' : 'OPERATORS',

    'BREAK' : 'KEYWORDS',
    'DEFAULT' : 'KEYWORDS',
    'FUNC' : 'KEYWORDS',
    'INTERFACE' : 'KEYWORDS',
    'SELECT' : 'KEYWORDS',
    'CASE' : 'KEYWORDS',
    'DEFER' : 'KEYWORDS',
    'GO' : 'KEYWORDS',
    'MAP' : 'KEYWORDS',
    'STRUCT' : 'KEYWORDS',
    'CHAN' : 'KEYWORDS',
    'ELSE' : 'KEYWORDS',
    'GOTO' : 'KEYWORDS',
    'PACKAGE' : 'KEYWORDS',
    'SWITCH' : 'KEYWORDS',
    'CONST' : 'KEYWORDS',
    'FALLTHROUGH' : 'KEYWORDS',
    'IF' : 'KEYWORDS',
    'RANGE' : 'KEYWORDS',
    'TYPE' : 'KEYWORDS',
    'CONTINUE' : 'KEYWORDS',
    'FOR' : 'KEYWORDS',
    'IMPORT' : 'KEYWORDS',
    'RETURN' : 'KEYWORDS',
    'VAR' : 'KEYWORDS',

    'INT' : 'NUMBERS',
    'FLOAT' : 'NUMBERS',
    'IMAG' : 'NUMBERS',

    'CHAR' : 'STRINGS',
    'STRING' : 'STRINGS',

    'ID' : 'IDENTIFIERS',
    'COM' : 'COMMENTS',
}

################################### Operators and delimiters
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_QUO = r'/'
t_REM = r'%'

t_AND = r'\&'
t_OR = r'\|'
t_XOR = r'\^'
t_SHL = r'<<'
t_SHR = r'>>'
t_AND_NOT = r'\&\^'

t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_QUO_ASSIGN = r'/='
t_REM_ASSIGN = r'%='

t_AND_ASSIGN = r'\&='
t_OR_ASSIGN = r'\|='
t_XOR_ASSIGN = r'\^='
t_SHL_ASSIGN = r'<<='
t_SHR_ASSIGN = r'>>='
t_AND_NOT_ASSIGN = r'\&\^='

t_LAND = r'\&\&'
t_LOR = r'\|\|'
t_ARROW = r'<-'
t_INC = r'\+\+'
t_DEC = r'--'

t_EQL = r'=='
t_LSS = r'<'
t_GTR = r'>'
t_ASSIGN = r'='
t_NOT = r'!'

t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_DEFINE = r':='
t_ELLIPSIS = r'\.\.\.'

t_LPAREN = r'\('
t_LBRACK = r'\['
t_LBRACE = r'\{'
t_COMMA = r','
t_PERIOD = r'\.'

t_RPAREN = r'\)'
t_RBRACK = r'\]'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COLON = r':'

##################################### Numbers
decimal_lit = r'[1-9][\d]*'
octal_lit = r'0[0-7]+'
hexal_lit = r'0[xX][\dA-F]+'
t_INT = '('+decimal_lit+')|('+octal_lit+')|('+hexal_lit+')'

decimals = r'[0-9]+'
exponent = r'[eE][+-]?[0-9]+'
float_lit = '('+decimals+'\.'+decimals+exponent+')|('+decimals+exponent+')|('+decimals+'\.'+decimals+')'

t_FLOAT = float_lit
t_IMAG = '(('+decimals+')|('+float_lit+'))'+'i'

###################################### Strings
t_CHAR = r'\'[^\']\''
t_STRING = r'\"[^\"]*\"'

###################################### Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_\d]*'
    t.type = reserved.get(t.value,'ID')
    return t

###################################### Comments
def t_COM(t):
    r'(/\*(.|\n)*\*/)|(//.*\n)'
    return t

####################################### Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

####################################### A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

####################################### Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

####################################### Build the lexer
lexer = lex.lex()

#######################################    HTML PART    ###########################
#######################################                 ########################

f = open(args["in"], "r")
data = f.read()
f.close()

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
    f.write("<font color=\"" + classcolour[tokenclass[str(tok.type)]] + "\">")
    if tok.type == 'COM':
        for i in xrange(tok.lexpos, pos):
            if data[i] == ' ':
                f.write("&nbsp;")
            elif data[i] == '\n':
                f.write("<br>")
            else:
                f.write(data[i])
    else:
        f.write(str(tok.value))
    f.write("</font>")

f.write("</body></html>")
f.close()
