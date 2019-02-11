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
strings = ['STRING']
special = ['COM']

tokens = operators + numbers + strings + special + ['ID'] + list(reserved.values())

tokenclass = {
    'ADD' : 'ARITHMETIC_OPERATORS',
    'SUB' : 'ARITHMETIC_OPERATORS',
    'MUL' : 'ARITHMETIC_OPERATORS',
    'QUO' : 'ARITHMETIC_OPERATORS',
    'REM' : 'ARITHMETIC_OPERATORS',
    'AND' : 'ARITHMETIC_OPERATORS',
    'OR' : 'ARITHMETIC_OPERATORS',
    'XOR' : 'ARITHMETIC_OPERATORS',
    'SHL' : 'ARITHMETIC_OPERATORS',
    'SHR' : 'ARITHMETIC_OPERATORS',
    'AND_NOT' : 'ARITHMETIC_OPERATORS',

    'ADD_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'SUB_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'MUL_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'QUO_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'REM_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'AND_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'OR_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'XOR_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'SHL_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'SHR_ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'AND_NOT_ASSIGN' : 'ASSIGNMENT_OPERATORS',

    'LAND' : 'LOGICAL_OPERATORS',
    'LOR' : 'LOGICAL_OPERATORS',
    'ARROW' : 'OTHER_OPERATORS',
    'INC' : 'OTHER_OPERATORS',
    'DEC' : 'OTHER_OPERATORS',
    'EQL' : 'RELATIONAL_OPERATORS',
    'LSS' : 'RELATIONAL_OPERATORS',
    'GTR' : 'RELATIONAL_OPERATORS',
    'ASSIGN' : 'ASSIGNMENT_OPERATORS',
    'NOT' : 'LOGICAL_OPERATORS',
    'NEQ' : 'RELATIONAL_OPERATORS',
    'LEQ' : 'RELATIONAL_OPERATORS',
    'GEQ' : 'RELATIONAL_OPERATORS',
    'DEFINE' : 'OTHER_OPERATORS',
    'ELLIPSIS' : 'OTHER_OPERATORS',

    'LPAREN' : 'PUNCTUATION',
    'LBRACK' : 'PUNCTUATION',
    'LBRACE' : 'PUNCTUATION',
    'COMMA' : 'PUNCTUATION',
    'PERIOD' : 'PUNCTUATION',
    'RPAREN' : 'PUNCTUATION',
    'RBRACK' : 'PUNCTUATION',
    'RBRACE' : 'PUNCTUATION',
    'SEMICOLON' : 'PUNCTUATION',
    'COLON' : 'PUNCTUATION',

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
decimal_lit = r'0|([1-9][\d]*)'
octal_lit = r'0[0-7]+'
hexal_lit = r'0[xX][\dA-F]+'
t_INT = '('+decimal_lit+')|('+octal_lit+')|('+hexal_lit+')'

decimals = r'[0-9]+'
exponent = r'[eE][+-]?[0-9]+'
float_lit = '('+decimals+'\.'+decimals+exponent+')|('+decimals+exponent+')|('+decimals+'\.'+decimals+')'

t_FLOAT = float_lit
t_IMAG = '(('+decimals+')|('+float_lit+'))'+'i'

###################################### Strings
t_STRING = r'(\'[^\']*\')|(\"[^\"]*\")'

###################################### Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_\d]*'
    t.type = reserved.get(t.value,'ID')
    return t

###################################### Comments
def t_COM(t):
    r'(/\*(.|\n)*\*/)|(//.*\n)'
    t.lexer.lineno += t.value.count('\n')
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
f.write("<html><body bgcolor=\"" + classcolour['BACKGROUND'] + "\">")
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
        elif data[i] == '\t':
            f.write("&nbsp;&nbsp;&nbsp;&nbsp;")
        elif data[i] == '\n':
            f.write("<br>")
        else:
            f.write("<font color=\"white\">" + data[i] + "</font>")
    pos = tok.lexpos + l
    # print(pos)
    f.write("<font color=\"" + classcolour[tokenclass[tok.type]] + "\">")
    if tok.type == 'COM':
        for i in xrange(tok.lexpos, pos):
            if data[i] == ' ':
                f.write("&nbsp;")
            elif data[i] == '\t':
                f.write("&nbsp;&nbsp;&nbsp;&nbsp;")
            elif data[i] == '\n':
                f.write("<br>")
            else:
                f.write(data[i])
    else:
        f.write(str(tok.value))
    f.write("</font>")

f.write("</body></html>")
f.close()
