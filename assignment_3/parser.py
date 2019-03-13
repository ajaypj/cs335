import re
import argparse
import ply.lex as lex
import ply.yacc as yacc
from lexer import *
from p_functions import *

parser = argparse.ArgumentParser(description = "argument parser")
parser.add_argument("--in", help = 'Specify input file', required = True)
# parser.add_argument("--out", help = 'Specify output file', required = True)
args = vars(parser.parse_args())

################################### Symbol Table #############################################
scopeStack = [0]
scopeNo = 0
currScope = 0
scopeST = {}
scopeST[0] = symbolTable()

def checkID(identifier, typeOf):
    if typeOf == 'global':
        if scopeST[0].getInfo(identifier) is not None:
            return True
        return False

    if typeOf == 'curr':
        if scopeST[currScope].getInfo(identifier) is not None:
            return True
        return False

    if typeOf == 'recent':
        for scope in scopeStack[::-1]:
            if scopeST[scope].getInfo(identifier) is not None:
                info = scopeST[scope].getInfo(identifier)
                if typeOf == "**" or info['type'] == typeOf:
                    return True
    else:
        if scopeST[typeOf].getInfo(identifier) is not None:
            return True
        return False


    return False

def pushScope(name=None):
    global currScope
    global scopeNo
    scopeNo += 1
    lastScope = currScope
    currScope = scopeNo
    scopeStack.append(currScope)
    scopeST[currscope] = symbolTable(lastScope)
    if name is not None:
        #

def popScope():
    global currScope
    currScope = scopeStack.pop()
    currScope = scopeStack[-1]

################################### Precedence #############################################
precedence = (
    ('nonassoc','ID','STRING','INT','FLOAT','IMAG','STRUCT'),
    ('left','COMMA'),
    ('left','LBRACE','RBRACE' ),
    ('right','ASSIGN','ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','QUO_ASSIGN','REM_ASSIGN','AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN','SHL_ASSIGN','SHR_ASSIGN'),
    ('right','DEFINE'),
    ('left','LOR'),
    ('left','LAND'),
    ('left','OR'),
    ('left','XOR'),
    ('left','AND'),
    ('left','EQL','NEQ'),
    ('left','LSS','GTR','LEQ','GEQ'),
    ('left','SHL','SHR'),
    ('left','ADD','SUB'),
    ('left','MUL','QUO','REM'),
    ('right','NOT','INC','DEC'),
    ('left','LPAREN','RPAREN','LBRACK','RBRACK','ARROW','PERIOD'),
    ('nonassoc','BREAK','DEFAULT','FUNC',
     'INTERFACE','SELECT','CASE','DEFER','GO','MAP',
     'CHAN','ELSE','GOTO','PACKAGE','SWITCH','CONST','FALLTHROUGH',
     'IF','RANGE','TYPE','CONTINUE','FOR','IMPORT','RETURN','VAR')
)

########################### Build the parser ###################################
parser = yacc.yacc()

f = open(args["in"], "r")
data = f.read()
f.close()

result = parser.parse(data,debug=1)
# print (result)
