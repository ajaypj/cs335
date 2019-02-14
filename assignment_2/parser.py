import re
import argparse
import ply.lex as lex
import ply.yacc as yacc
from p_functions import *

parser = argparse.ArgumentParser(description = "argument parser")
parser.add_argument("--in", help = 'Specify input', required = True)
# parser.add_argument("--out", help = 'Specify output file', required = True)
args = vars(parser.parse_args())


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

operators = ['ADD','SUB','MUL','QUO','REM','AND','OR','COND','XOR','SHL','SHR','AND_NOT','ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','QUO_ASSIGN','REM_ASSIGN','AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN','SHL_ASSIGN','SHR_ASSIGN','AND_NOT_ASSIGN','LAND','LOR','ARROW','INC','DEC','EQL','LSS','GTR','ASSIGN','NOT','NEQ','LEQ','GEQ','DEFINE','ELLIPSIS','LPAREN','LBRACK','LBRACE','COMMA','PERIOD','RPAREN','RBRACK','RBRACE','SEMICOLON','COLON']
numbers = ['INT','FLOAT','IMAG']
strings = ['STRING']
special = ['COM']

tokens = operators + numbers + strings + special + ['ID'] + ['VARTYPE'] + list(reserved.values())


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

t_COND=r'\?='

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

t_VARTYPE = r'int16|int8|int32|int64|int|bool|string|uint|uint16|uint32|uint64|uintptr|float32|float64|complex64|complex128'


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
    pass

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

#######################################   PARSING PART    ###########################
#######################################                   ########################
################### Bismay
def p_error(p):
    print "ERROR HERE"
    print p.lineno(1)," token = "
    return

################################################################################


precedence = (
    ('nonassoc','ID','STRING','INT','FLOAT','IMAG'),
    ('left', 'COMMA' ),
    ('right', 'ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN'),
    ('left','LBRACE','RBRACE' ),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQL', 'NEQ'),
    ('left', 'LSS', 'GTR', 'LEQ', 'GEQ'),
    ('left', 'SHL', 'SHR'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'QUO', 'REM'),
    ('right', 'NOT', 'INC', 'DEC'),
    ('left', 'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK','ARROW', 'PERIOD'),
    ('nonassoc','BREAK',  'DEFAULT',  'FUNC',
     'INTERFACE', 'SELECT',  'CASE',  'DEFER',  'GO',  'MAP',  'STRUCT',
     'CHAN',  'ELSE',  'GOTO',  'PACKAGE',  'SWITCH',  'CONST',  'FALLTHROUGH',
     'IF', 'RANGE',  'TYPE',  'CONTINUE',  'FOR',  'IMPORT',  'RETURN',  'VAR')
)

# precedence =(
#     ('nonassoc','ID'),
#     ('left','LBRACE'),
# )



############################################################# Build the parser





parser = yacc.yacc()

f = open(args["in"], "r")
data = f.read()
f.close()

print "digraph b {"
result = parser.parse(data,debug=1)
print "}"
# print (result)
