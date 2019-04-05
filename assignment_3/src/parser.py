import re
import argparse
import ply.lex as lex
import ply.yacc as yacc
from lexer import *
from symbol import *

parser = argparse.ArgumentParser(description = "argument parser")
parser.add_argument("--in", help = 'Specify input file', required = True)
parser.add_argument("--out", help = 'Specify output file', required = True)
args = vars(parser.parse_args())

################################### Symbol Table #############################################
scopeStack = [0]
scopeNo = 0
currScope = 0
scopeST = {}
scopeST[0] = symbolTable()
labelNo=0
# Stores parent of label
labelDic={}
labelDic['0']=None
currLabel="0"

def checkID(identifier, typeOf):
    if typeOf == 'global':
        return scopeST[0].getInfo(identifier)

    if typeOf == 'curr':
        return scopeST[currScope].getInfo(identifier)

    if typeOf == 'recent':
        for scope in scopeStack[::-1]:
            if scopeST[scope].getInfo(identifier) is not None:
                return scopeST[scope].getInfo(identifier)
        return None

    # else:
    #     if scopeST[typeOf].getInfo(identifier) is not None:
    #         return True
    #     return False

    return None

def pushScope(name=None):
    global currScope
    global scopeNo
    scopeNo += 1
    lastScope = currScope
    currScope = scopeNo
    scopeStack.append(currScope)
    scopeST[currScope] = symbolTable(lastScope)

def popScope():
    global currScope
    currScope = scopeStack.pop()
    currScope = scopeStack[-1]

var_no=0
lineno=0

def new_var():
    global var_no
    retVal='var_'+str(var_no)
    var_no+=1
    return retVal

def createLabel():
    global labelNo
    retVal='label_'+str(labelNo)
    labelNo+=1
    return retVal

class expr():
    def __init__(self):
        self.place = new_var()
        self.cls = ''
        self.type=''
        self.value=None
        self.extra={}
        self.code=[]

def p_error(p):
    print "ERROR HERE"
    exit()
    return

################################################################################
def p_SourceFile(p):
    ''' SourceFile     		: PackageClause ImportDeclList TopLevelDeclList
                            | PackageClause ImportDeclList
                            | PackageClause TopLevelDeclList
                            | PackageClause '''
    print currScope
    for item in scopeST[currScope].table:
        print item, (scopeST[currScope].table)[item]

def p_PackageClause(p):
    ''' PackageClause  		: PACKAGE ID SEMICOLON '''


def p_ImportDeclList(p):
    ''' ImportDeclList 		: ImportDecl SEMICOLON
							| ImportDeclList ImportDecl SEMICOLON '''


def p_ImportDecl(p):
    ''' ImportDecl     		: IMPORT LPAREN ImportSpecList RPAREN
                            | IMPORT LPAREN RPAREN
							| IMPORT ImportSpec '''

def p_ImportSpecList(p):
    ''' ImportSpecList 		: ImportSpec SEMICOLON
							| ImportSpecList ImportSpec SEMICOLON '''

def p_ImportSpec(p):
    ''' ImportSpec     		: ID ImportPath
							| PERIOD ImportPath
							| ImportPath '''

def p_ImportPath(p):
    ''' ImportPath     		: STRING '''

def p_TopLevelDeclList(p):
    ''' TopLevelDeclList    : TopLevelDecl SEMICOLON
							| TopLevelDeclList TopLevelDecl SEMICOLON '''

def p_TopLevelDecl(p):
    ''' TopLevelDecl   		: Declaration
							| FunctionDecl '''
    p[0]=p[1]
							# | MethodDecl '''

################################################################################
def p_StartScope(p):
    ''' StartScope         	: '''
    pushScope()

def p_EndScope(p):
    ''' EndScope    		: '''
    str = ''
    for i in xrange(len(scopeStack)-1):
        str += '\t\t'
    print str, currScope
    for item in scopeST[currScope].table:
        print str, item, (scopeST[currScope].table)[item]
    print ''
    popScope()

def p_StructScope(p):
    '''StructScope          : '''
    pushScope(p[-1])

################################################################################
def p_FunctionDecl(p):
    ''' FunctionDecl   		: FUNC ID StartScope Signature EndScope
							| FUNC ID StartScope Signature Block EndScope '''
    if checkID(p[2], 'curr'):
        raise Exception("Line "+str(p.lineno(2))+": "+"Symbol "+p[2]+" already exists.")
    else:
        (scopeST[currScope].table)[p[2]] = p[4].copy()
        scopeST[currScope].update(p[2], 'cls', 'FUNC')
    if len(p)==7:
        for i in p[5]:
            irf.write(i)
            irf.write('\n')
        irf.write('\n')

# def p_MethodDecl(p):
#     ''' MethodDecl     		: FUNC Parameters ID Signature
#                             | FUNC Parameters ID Signature Block '''
#     # func(p,"MethodDecl")

def p_Declaration(p):
    ''' Declaration    		: ConstDecl
                            | TypeDecl
							| VarDecl '''
    p[0]=[]

def p_ConstDecl(p):
    ''' ConstDecl           : '''

def p_TypeDecl(p):
    ''' TypeDecl       		: TYPE TypeSpec
                            | TYPE LPAREN TypeSpecList RPAREN
                            | TYPE LPAREN RPAREN '''

def p_TypeSpecList(p):
    ''' TypeSpecList       	: TypeSpec SEMICOLON
                            | TypeSpecList TypeSpec SEMICOLON '''

def p_TypeSpec(p):
    ''' TypeSpec       		: ID ASSIGN Type
                            | ID Type '''
    if checkID(p[1], 'curr') is not None:
        raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+p[1]+" already exists.")
    elif len(p) == 4:
        (scopeST[currScope].table)[p[1]] = p[3].copy()
    else:
        (scopeST[currScope].table)[p[1]] = p[2].copy()

################################################################################
def p_Type1(p):
    ''' Type           		: VARTYPE '''
    p[0] = {'type' : p[1], 'cls' : 'TYPENAME'}

def p_Type2(p):
    ''' Type           		: LiteralType '''
    p[0] = p[1]
    p[0]['cls'] = 'TYPENAME'

def p_Type3(p):
    ''' Type           		: ID '''
    if checkID(p[1], 'recent') is None:
        raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+p[1]+" doesn't exist.")
    elif checkID(p[1], 'recent')['cls'] != 'TYPENAME':
        raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+p[1]+" is not a typename.")
    else:
        p[0] = (checkID(p[1], 'recent')).copy()

def p_LiteralType(p):
    ''' LiteralType    		: ArrayType
							| StructType
							| PointerType '''
							# | SliceType
                            # | MapType '''
    p[0] = p[1]

def p_ArrayType(p):
    ''' ArrayType      		: LBRACK Expression RBRACK Type ''' # Must be integer
    p[0] = {}
    p[0]['type'] = 'ARRAY(' + p[4]['type'] + ')'
    # p[0]['size'] will be calculated

def p_StructType(p):
    ''' StructType     		: STRUCT StructScope LBRACE FieldDeclList RBRACE EndScope
							| STRUCT StructScope LBRACE RBRACE EndScope '''
    p[0] = {}
    p[0]['type'] = 'STRUCT'
    if len(p) == 7:
        p[0]['scopeno'] = p[4]
        p[0]['type'] += ' '+str(p[4])

def p_FieldDeclList(p):
    ''' FieldDeclList  		: FieldDecl SEMICOLON
							| FieldDeclList FieldDecl SEMICOLON '''
    p[0] = currScope

def p_FieldDecl(p):
    ''' FieldDecl      		: IdentifierList Type STRING
							| IdentifierList Type '''
    for iden in p[1]:
        if checkID(iden, 'curr') is not None:
            raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+iden+" already exists.")
        (scopeST[currScope].table)[iden] = p[2].copy()
        scopeST[currScope].update(iden, 'cls', 'FIELD')

def p_PointerType(p):
    ''' PointerType    		: MUL Type '''
    p[0] = {}
    p[0]['type'] = 'POINTER(' + p[2]['type'] + ')'

# def p_SliceType(p):
#     ''' SliceType      		: LBRACK RBRACK Type '''
#     # func(p,"SliceType")
#
# def p_MapType(p):
#     ''' MapType        		: MAP LBRACK Type RBRACK Type '''
#     # func(p,"MapType")

################################################################################
# def p_FunctionType(p):
#     ''' FunctionType        : FUNC Signature '''
#     # func(p,"FunctionType")

def p_Signature1(p):
    ''' Signature      		: Parameters
                            | Parameters Type '''
    p[0] = {}
    p[0]['scopeno'] = currScope
    p[0]['parameters'] = p[1]
    if len(p) > 2:
        p[0]['return'] = [p[2]['type']]
    else:
        p[0]['return'] = ['VOID']

def p_Signature2(p):
    ''' Signature      		: Parameters Parameters '''
    p[0] = {}
    p[0]['scopeno'] = currScope
    p[0]['parameters'] = p[1]
    p[0]['return'] = p[2]

def p_Parameters(p):
    ''' Parameters     		: LPAREN RPAREN
							| LPAREN ParameterList RPAREN
							| LPAREN ParameterList COMMA RPAREN '''
    if len(p) > 3:
        p[0] = p[2]

def p_ParameterList(p):
    ''' ParameterList  		: ParameterDecl
							| ParameterList COMMA ParameterDecl '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]

def p_ParameterDecl(p):
    ''' ParameterDecl  		: Type
                            | IdentifierList Type '''
    if len(p) == 2:
        p[0] = [p[1]['type']]
    else:
        p[0] = []
        for iden in p[1]:
            p[0].append(p[2]['type'])
            if checkID(iden, 'curr') is not None:
                raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+iden+" already exists.")
            (scopeST[currScope].table)[iden] = p[2].copy()
            scopeST[currScope].update(iden, 'cls', 'VAR')

# def p_InterfaceType(p):
#     ''' InterfaceType 		: INTERFACE LBRACE RBRACE
#                             | INTERFACE LBRACE MethodSpecList RBRACE '''
#     # func(p,"InterfaceType")
#
# def p_MethodSpecList(p):
#     ''' MethodSpecList      : MethodSpec SEMICOLON
#                             | MethodSpecList MethodSpec SEMICOLON '''
#     # func(p,"MethodSpecList")
#
# def p_MethodSpec(p):
#     ''' MethodSpec        	: ID Signature
#                             | ID Type '''
#     # func(p,"MethodSpec")
#
# def p_ChannelType(p):
#     ''' ChannelType 		: CHAN Type
#                             | CHAN ARROW Type
#                             | ARROW CHAN Type '''
#     # func(p,"ChannelType")

################################################################################
def p_VarDecl(p):
    ''' VarDecl        		: VAR VarSpec
                            | VAR LPAREN VarSpecList RPAREN
                            | VAR LPAREN RPAREN '''

def p_VarSpecList(p):
    ''' VarSpecList       	: VarSpec SEMICOLON
                            | VarSpecList VarSpec SEMICOLON '''

def p_VarSpec(p):
    ''' VarSpec        		: IdentifierList Type
							| IdentifierList Type ASSIGN ExpressionList
                            | IdentifierList Type ASSIGN LBRACE ExpressionList RBRACE '''
    for iden in p[1]:
        if checkID(iden, 'curr') is not None:
            raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+iden+" already exists.")
        (scopeST[currScope].table)[iden] = p[2].copy()
        scopeST[currScope].update(iden, 'cls', 'VAR')

# def p_VarSpec(p):
#     '''	VarSpec			    : IdentifierList ASSIGN ExpressionList
#     						| IdentifierList ASSIGN LBRACE ExpressionList RBRACE '''
#     for iden in p[1]:
#         # scopeST[currScope].update()

def p_IdentifierList(p):
    ''' IdentifierList 		: ID
							| IdentifierList COMMA ID '''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_ShortVarDecl(p):
    ''' ShortVarDecl   		: IdentifierList DEFINE ExpressionList '''
    if len(p[1]) != len(p[3]):
        raise Exception("Line "+str(p.lineno(2))+": "+"Number of arguments do not match.")
    # for i in xrange(len(p[1])):
    #     scopeST[currScope].update()

################################################################################
def p_Block(p):
    ''' Block          		: LBRACE StatementList RBRACE
                            | LBRACE RBRACE '''
    if len(p) > 3:
        p[0]=p[2]
    else:
        p[0]=[]
    # func(p,"Block")

def p_StatementList(p):
    ''' StatementList  		: StatementList Statement SEMICOLON
							| Statement SEMICOLON '''
    # print p[1]
    # print p[2]
    if len(p)==3:
        # print p[1]
        p[0]=p[1]
    else:
        p[0]=p[1]+p[2]
    # func(p,"StatementList")

def p_Statement(p):
    ''' Statement      		: Declaration
                            | SimpleStmt
							| ReturnStmt
							| BreakStmt
							| ContinueStmt
                            | LabeledStmt
							| GotoStmt
							| StartScope Block EndScope
							| IfStmt
                            | ForStmt
                            | SwitchStmt
                            | FallthroughStmt
    '''
    # | GoStmt
    # | SelectStmt
    # | RecvStmt
    # | DeferStmt
    # func(p,"Statement")
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=p[2]

def p_SimpleStmt(p):
    ''' SimpleStmt     		: ShortVarDecl
                            | EmptyStmt
							| ExpressionStmt
                            | IncDecStmt
                            | Assignment '''
                            # | SendStmt
    p[0]=p[1]

def p_EmptyStmt(p):
    ''' EmptyStmt      		: '''
    # func(p,"EmptyStmt")
    p[0]=[]

def p_ExpressionStmt(p):
    ''' ExpressionStmt 		: Expression '''
    p[0]=p[1].code
    # func(p,"ExpressionStmt")

# def p_SendStmt(p):
#     ''' SendStmt 		    : Expression ARROW Expression '''
#     func(p,"SendStmt")

def p_IncDecStmt(p):
    ''' IncDecStmt     		: Expression INC
                            | Expression DEC '''
    # Check that Expression is a variable or UnaryExpr
    p[0]=p[1].code
    str=''
    if p[2]=='++':
        str='+'
    else:
        str='-'
    str+=p[1].place+','+p[1].place+',1'
    p[0]+=[str]

def p_Assignment(p):
    ''' Assignment     		: ExpressionList assign_op ExpressionList '''
        # Break assign_op into multiple parts
    if len(p[1])!=len(p[3]):
        raise Exception("Line "+str(p.lineno(2))+": "+"Number of expressions do not match.")
    p[0]=[]
    for i in range(len(p[1])):
        p[0]+=p[3][i].code

    for i in range(len(p[1])):
        if len(p[2])==2:
            if p[1][i].type == 'float' and p[3][i].type == 'int':
                var = new_var()
                p[0] += ['=inttofloat'+','+var+','+p[3][i].place]
                p[0] += ['float'+p[2][0]+','+p[1][i].place +","+p[1][i].place +","+var]
            elif p[1][i].type != p[3][i].type:
                raise Exception("Line "+str(p.lineno(2))+": "+"Type mismatch ["+str(i)+"].")
            elif p[1][i].type == 'float' or p[1][i].type == 'int':
                p[0] += [p[1][i].type+p[2][0]+','+p[1][i].place +","+p[1][i].place +","+p[3][i].place]
            elif p[1][i].type == 'string' and p[2][0] == '+':
                p[0] += [p[1][i].type+p[2][0]+','+p[1][i].place +","+p[1][i].place +","+p[3][i].place]
            else:
                raise Exception("Line "+str(p.lineno(2))+": "+"Can't perform operation"+p[2]+"["+str(i)+"].")
        else:
            if p[1][i].type == 'float' and p[3][i].type == 'int':
                var = new_var()
                p[0] += ['=inttofloat'+','+var+','+p[3][i].place]
                p[0] += [p[2][0]+','+p[1][i].place +","+var]
            elif p[1][i].type != p[3][i].type:
                raise Exception("Line "+str(p.lineno(2))+": "+"Type mismatch ["+str(i)+"].")
            else:
                p[0] += [p[2][0]+','+p[1][i].place +","+p[3][i].place]
    # print p[0]

def p_ReturnStmt(p):
    ''' ReturnStmt     		: RETURN
							| RETURN ExpressionList '''
    if len(p)==3:
        p[0]=p[2][0].code
        p[0]+=["=,retVal,"+p[2][0].place]
    # func(p,"ReturnStmt")

### Not Done
def p_BreakStmt(p):
    ''' BreakStmt      		: BREAK
							| BREAK ID '''
    # global currLabel
    if len(p)==2:
        # if currLabel in labelDic.keys():
        gt=labelDic[currLabel]
        if gt is not None:
            p[0]=["goto,"+gt]
        else:
            raise Exception("Line "+str(p.lineno(1))+": "+"Nothing to Break.")
    else:
        # check if ID in Label
        if p[2] in labelDic.keys():
            p[0]=["goto,"+p[2]]
        else:
            raise Exception("Line "+str(p.lineno(2))+": "+"Label "+ p[2]+" doesn't exist.")

def p_ContinueStmt(p):
    ''' ContinueStmt   		: CONTINUE
							| CONTINUE ID '''
    if len(p)==2:
        if currLabel != "0":
            p[0]=["goto,"+currLabel]
        else:
            raise Exception("Line "+str(p.lineno(1))+": "+"Nothing To continue.")
    else:
        if p[2] in labelDic.keys():
            p[0]=["goto,"+p[2]]
        else:
            raise Exception("Line "+str(p.lineno(2))+": "+"Label "+p[2]+" doesn't exist.")

# Doubt
def p_LabeledStmt(p):
    ''' LabeledStmt    		: ID COLON Statement '''
    labelDic[p[1]]="Created"
    p[0]=[p[1]+':',p[2].code]

def p_GotoStmt(p):
    ''' GotoStmt       		: GOTO ID '''
    if p[2] in labelDic.keys():
        p[0]=["goto,"+p[2]]

################################################################################
def p_IfStmt(p):
    ''' IfStmt         		: IF Expression StartScope Block EndScope'''
                            # | IF SimpleStmt SEMICOLON Expression Block ELSE IfStmt
                            # | IF SimpleStmt SEMICOLON Expression Block ELSE Block
                            # | IF SimpleStmt SEMICOLON Expression Block
    endLabel=createLabel()

    p[0]=p[2].code
    # Consider gotoPos goes to Label if positive,similarly gotoZeroNeg
    p[0]+=["gotoZeroNeg,"+p[2].place+","+endLabel]
    p[0]+=p[4]
    p[0]+=[endLabel+":"]

def p_IfStmt1(p):
    ''' IfStmt         		: IF Expression StartScope Block EndScope ELSE StartScope Block EndScope'''
    p[0]=p[2].code
    # Printed in the format  Else ifLabel If endLabel
    ifLabel=createLabel()
    endLabel=createLabel()
    p[0]+=["gotoPos,"+p[2].place+","+ifLabel]
    p[0]+=p[8]
    p[0]+=["goto,"+endLabel]
    p[0]+=[ifLabel+":"]
    p[0]+=p[4]

def p_IfStmt2(p):
    ''' IfStmt         		: IF Expression StartScope Block EndScope ELSE IfStmt '''
    p[0]=p[2].code
    ifLabel=createLabel()
    endLabel=createLabel()
    p[0]+=["gotoPos,"+p[2].place+","+ifLabel]
    p[0]+=p[7]
    p[0]+=["goto,"+endLabel]
    p[0]+=[ifLabel+":"]
    p[0]+=p[4]

def p_ForStmt(p):
    ''' ForStmt : FOR ForSig StartScope Block EndScope '''
    forLabel=createLabel()
    endLabel=createLabel()
    p[0]=p[2][0]
    p[0]+=[forLabel+":"]
    p[0]+=p[2][1].code
    p[0]+=["gotoNeg,"+p[2][1].place+","+endLabel]
    p[0]+=p[4]
    p[0]+=p[2][2]
    p[0]+=["goto,"+forLabel]
    p[0]+=[endLabel+":"]

def p_ForSig(p):
    ''' ForSig 		    : ForClause'''
#     ''' ForSig 		    : Condition
#     | ForClause
#     | RangeClause '''
#     # func(p,"ForSig")
    p[0]=p[1]

def p_Condition(p):
    ''' Condition 		    : Expression '''
    p[0]=p[1]
    # func(p,"Condition")

def p_ForClause(p):
    ''' ForClause 		    : SimpleStmt SEMICOLON Condition SEMICOLON SimpleStmt '''
    p[0]=[p[1],p[3],p[5]]
    # func(p,"ForClause")

# def p_RangeClause(p):
#     ''' RangeClause 		: RangeClause_1 RANGE Expression '''
#     # func(p,"RangeClause")
#
# def p_RangeClause_1(p):
#     ''' RangeClause_1 		: ExpressionList ASSIGN
# 							| IdentifierList DEFINE
# 							| '''
#     # func(p,"RangeClause_1")

def p_SwitchStmt(p):
    ''' SwitchStmt          : ExprSwitchStmt '''
    # func(p,"SwitchStmt")

def p_ExprSwitchStmt(p):
    ''' ExprSwitchStmt      : SWITCH SimpleStmt SEMICOLON Expression LBRACE ExprCaseClauseList RBRACE
                            | SWITCH SimpleStmt SEMICOLON Expression LBRACE RBRACE
                            | SWITCH Expression LBRACE ExprCaseClauseList RBRACE
                            | SWITCH Expression LBRACE RBRACE
                            | SWITCH LBRACE ExprCaseClauseList RBRACE
                            | SWITCH LBRACE RBRACE '''
    # func(p,"ExprSwitchStmt")

def p_ExprCaseClauseList(p):
    ''' ExprCaseClauseList  : ExprCaseClause
                            | ExprCaseClauseList ExprCaseClause '''
    # func(p,"ExprCaseClauseList")

def p_ExprCaseClause(p):
    ''' ExprCaseClause      : ExprSwitchCase COLON StatementList '''
    # func(p,"ExprCaseClause")

def p_ExprSwitchCase(p):
    ''' ExprSwitchCase      : CASE ExpressionList
                            | DEFAULT
                            | CASE Expression '''
    # func(p,"ExprSwitchCase")

def p_FallthroughStmt(p):
    ''' FallthroughStmt     : FALLTHROUGH '''
    # func(p,"FallthroughStmt")

# def p_GoStmt(p):
#     '''GoStmt               : GO Expression'''
#     # func(p,"GoStmt")
#
# def p_SelectStmt(p):
#     ''' SelectStmt     		: SELECT LBRACE RBRACE
# 							| SELECT LBRACE CommClauseList RBRACE '''
#     # func(p,"SelectStmt")
#
# def p_CommClauseList(p):
#     ''' CommClauseList     	: CommClause
#                             | CommClauseList CommClause '''
#     # func(p,"CommClause")
#
# def p_CommClause(p):
#     ''' CommClause     		: CommCase COLON StatementList '''
#     # func(p,"CommClause")
#
# def p_CommCase(p):
#     ''' CommCase       		: CASE SendStmt
# 							| DEFAULT
# 							| CASE RecvStmt '''
#     # func(p,"CommCase")
#
# def p_RecvStmt(p):
#     ''' RecvStmt       		: ExpressionList ASSIGN Expression
# 							| Expression
# 							| IdentifierList DEFINE Expression '''
#     # func(p,"RecvStmt")
#
# def p_DeferStmt(p):
#     ''' DeferStmt           : DEFER Expression '''
#     # func(p,"DeferStmt")

##########################       Expression   ##########################
def p_ExpressionList(p):
    ''' ExpressionList  	: Expression
							| ExpressionList COMMA Expression '''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]

def p_Expression(p):
    ''' Expression     		: Expression1 '''
                            # | UnaryExpr assign_op Expression
    p[0] = p[1]

def p_Expression1(p):
    ''' Expression1    		: Expression2
							| Expression1 LOR Expression2 '''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=expr()
        p[0].code=p[1].code+p[3].code+[p[2]+','+p[0].place+','+p[1].place+','+p[3].place]
        p[0].type='bool'
        p.set_lineno(0,p.lineno(2))

def p_Expression2(p):
    ''' Expression2    		: Expression3
							| Expression2 LAND Expression3 '''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=expr()
        p[0].code=p[1].code+p[3].code+[p[2]+','+p[0].place+','+p[1].place+','+p[3].place]
        p[0].type='bool'
        p.set_lineno(0,p.lineno(2))

def p_Expression3(p):
    ''' Expression3    		: Expression4
							| Expression3 rel_op Expression4 '''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=expr()
        p[0].code=p[1].code+p[3].code
        if p[1].type == 'float' and p[3].type == 'int':
            var = new_var()
            p[0].code.append('=inttofloat'+','+var+','+p[3].place)
            p[0].code.append('float'+p[2]+','+p[0].place+','+p[1].place+','+var)
        elif p[1].type == 'int' and p[3].type == 'float':
            var = new_var()
            p[0].code.append('=inttofloat'+','+var+','+p[1].place)
            p[0].code.append('float'+p[2]+','+p[0].place+','+var+','+p[3].place)
        elif p[1].type == 'int' and p[3].type == 'int':
            p[0].code.append('int'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
        elif p[1].type == 'float' and p[3].type == 'float':
            p[0].code.append('float'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
        elif p[1].type == 'string' and p[3].type == 'string':
            p[0].code.append('string'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
        else:
            raise Exception("Line "+str(p.lineno(2))+": "+"Can't compare these types.")
        p[0].type = 'bool'
        p.set_lineno(0,p.lineno(2))

def p_Expression4(p):
    ''' Expression4    		: Expression5
							| Expression4 add_op Expression5 '''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=expr()
        p[0].code=p[1].code+p[3].code
        if p[1].type == 'float' and p[3].type == 'int':
            var = new_var()
            p[0].code.append('=inttofloat'+','+var+','+p[3].place)
            p[0].code.append('float'+p[2]+','+p[0].place+','+p[1].place+','+var)
            p[0].type = 'float'
        elif p[1].type == 'int' and p[3].type == 'float':
            var = new_var()
            p[0].code.append('=inttofloat'+','+var+','+p[1].place)
            p[0].code.append('float'+p[2]+','+p[0].place+','+var+','+p[3].place)
            p[0].type = 'float'
        elif p[1].type == 'int' and p[3].type == 'int':
            p[0].code.append('int'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
            p[0].type = 'int'
        elif p[1].type == 'float' and p[3].type == 'float':
            p[0].code.append('float'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
            p[0].type = 'float'
        elif p[1].type == 'string' and p[3].type == 'string' and p[2] == '+':
            p[0].code.append('string'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
            p[0].type = 'string'
        else:
            raise Exception("Line "+str(p.lineno(2))+": "+"Can't perform "+p[2]+" on these types.")
        p.set_lineno(0,p.lineno(2))

def p_Expression5(p):
    ''' Expression5    		: UnaryExpr
							| Expression5 mul_op UnaryExpr '''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=expr()
        p[0].code=p[1].code+p[3].code
        if p[1].type == 'float' and p[3].type == 'int':
            var = new_var()
            p[0].code.append('=inttofloat'+','+var+','+p[3].place)
            p[0].code.append('float'+p[2]+','+p[0].place+','+p[1].place+','+var)
            p[0].type = 'float'
        elif p[1].type == 'int' and p[3].type == 'float':
            var = new_var()
            p[0].code.append('=inttofloat'+','+var+','+p[1].place)
            p[0].code.append('float'+p[2]+','+p[0].place+','+var+','+p[3].place)
            p[0].type = 'float'
        elif p[1].type == 'int' and p[3].type == 'int':
            p[0].code.append('int'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
            p[0].type = 'int'
        elif p[1].type == 'float' and p[3].type == 'float':
            p[0].code.append('float'+p[2]+','+p[0].place+','+p[1].place+','+p[3].place)
            p[0].type = 'float'
        else:
            raise Exception("Line "+str(p.lineno(2))+": "+"Can't perform "+p[2]+" on these types.")
        p.set_lineno(0,p.lineno(2))

def p_UnaryExpr(p):
    ''' UnaryExpr      		: PrimaryExpr
							| unary_op UnaryExpr '''
    if len(p)==2:
        if p[1].cls == 'FUNC':
            raise Exception("Line "+str(p.lineno(1))+": "+"No arguments passed.")
        p[0]=p[1]
    else:
        p[0]=expr()
        p[0].code=p[2].code+[p[1]+','+p[0].place+','+p[2].place]
        if p[1] == '*':
            p[0].type = (p[2].type)[8:-1]
        else:
            p[0].type = p[2].type
        p.set_lineno(0,p.lineno(1))

def p_PrimaryExpr(p):
    ''' PrimaryExpr    		: Operand '''
                            # | MethodExpr
    p[0]=p[1]
    p.set_lineno(0,p.lineno(1))

def p_PrimaryExpr1(p):
    ''' PrimaryExpr    		: PrimaryExpr Selector '''
    # PrimaryExpr should be struct

def p_Selector(p):
    ''' Selector       		: PERIOD ID '''
    # func(p,"Selector")

def p_PrimaryExpr2(p):
    ''' PrimaryExpr    		: PrimaryExpr Index '''
    # PrimaryExpr Should be array

def p_Index(p):
    ''' Index          		: LBRACK Expression RBRACK '''

# def p_PrimaryExpr3(p):
#     ''' PrimaryExpr    		: PrimaryExpr Slice
#     '''

# def p_PrimaryExpr4(p):
#     ''' PrimaryExpr    		: PrimaryExpr TypeAssertion
#     '''

def p_PrimaryExpr5(p):
    ''' PrimaryExpr    		: PrimaryExpr Arguments
    '''
    dic = checkID(p[1].place,'global')
    if dic is None:
        raise Exception("Line "+str(p.lineno(1))+": "+"Expected function name.")
    elif dic["cls"] != "FUNC":
        raise Exception("Line "+str(p.lineno(1))+": "+"Expected function name.")

    # PrimaryExpr should be function
    if len(p[2]) != len(dic['parameters']):
        raise Exception("Line "+str(p.lineno(2))+": "+str(len(dic['parameters']))+" parameters expected for "+p[1].place+".")
    else:
        for i in xrange(len(p[2])):
            if p[2][i].type != dic['parameters'][i]:
                raise Exception("Line "+str(p.lineno(2))+": "+str(i)+"th type doesn't match for "+p[1].place+".")

        # Function call
        p[0] = expr()
        p[0].cls = 'VAR'
        for i in xrange(len(p[2])):
            p[0].code+=p[2][i].code
            p[0].code+=["=,param_"+str(i)+p[2][i].place]
        p[0].code=["jump,"+p[1].place]
        p[0].code+=["="+p[0].place+',retVal']
        p[0].type=dic["return"][0]
    ### Multiple returns
    p.set_lineno(0,p.lineno(1))

def p_Arguments(p):
    ''' Arguments           : LPAREN RPAREN
                            | LPAREN ExpressionList COMMA RPAREN
                            | LPAREN ExpressionList RPAREN '''
    # | LPAREN Type COMMA ExpressionList COMMA RPAREN
    # | LPAREN Type COMMA ExpressionList RPAREN
    # | LPAREN Type COMMA RPAREN
    # | LPAREN Type RPAREN '''
    if len(p)==3:
        p[0]=[]
    else:
        p[0]=p[2]
    p.set_lineno(0,p.lineno(1))

# def p_Conversion(p):
#     ''' Conversion        	: Type LPAREN Expression COMMA RPAREN
# 							| Type LPAREN Expression RPAREN '''
#     # func(p,"Conversion")
#
# def p_MethodExpr(p):
#     ''' MethodExpr       	: Type PERIOD ID '''
#     func(p,"MethodExpr")
#
# def p_Slice(p):
#     ''' Slice          		: LBRACK COLON RBRACK
# 							| LBRACK COLON Expression RBRACK
# 							| LBRACK Expression COLON RBRACK
# 							| LBRACK Expression COLON Expression RBRACK
# 							| LBRACK COLON Expression COLON Expression RBRACK
# 							| LBRACK Expression COLON Expression COLON Expression RBRACK '''
#     func(p,"Slice")
#
# def p_TypeAssertion(p):
#     ''' TypeAssertion  		: PERIOD LPAREN Type RPAREN '''
#     func(p,"TypeAssertion")

def p_Operand(p):
    ''' Operand        		: Literal'''
    p[0]=p[1]
    p[0].cls = 'VAR'

def p_Operand1(p):
    ''' Operand        		: ID'''
    dic = checkID(p[1],'recent')
    if dic is None:
        raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+p[1]+" doesn't exist.")

    p[0]=expr()
    p[0].cls=dic["cls"]
    if p[0].cls=="VAR":
        p[0].type=dic["type"]
        if dic['type'] == 'STRUCT':
            p[0].extra["scopeno"] = dic["scopeno"]
    elif p[0].cls=="FUNC":
        p[0].extra["return"]=dic["return"]
        p[0].extra["parameters"]=dic["parameters"]
    else:
        raise Exception("Line "+str(p.lineno(1))+": "+"Symbol "+p[1]+" cannot be an operand.")
    p[0].place=p[1]
    p.set_lineno(0,p.lineno(1))

# def p_Operand2(p):# Doubt
#     ''' Operand        		: ID PERIOD ID'''

def p_Operand3(p):
    ''' Operand        		: LPAREN Expression RPAREN '''
    p[0]=p[2]
    p[0].cls = 'VAR'
    p.set_lineno(0,p.lineno(1))

def p_Literal(p):
    ''' Literal        		: BasicLit '''
                            # | FunctionLit
							# | CompositeLit
    p[0]=p[1]

def p_BasicLit(p):
    ''' BasicLit       		: INT '''
    p[0]=expr()
    p[0].type='int'
    # p[0].value=int(p[1])
    p[0].code=["="+','+p[0].place+","+p[1]]
    p.set_lineno(0,p.lineno(1))

def p_BasicLit1(p):
    ''' BasicLit       		: FLOAT '''
    p[0]=expr()
    p[0].type='float'
    # p[0].value=float(p[1])
    p[0].code=["=,"+p[0].place+","+p[1]]
    p.set_lineno(0,p.lineno(1))

def p_BasicLit2(p):
    ''' BasicLit       		: STRING '''
    p[0]=expr()
    p[0].type='string'
    # p[0].value=p[1]
    p[0].code=["=,"+p[0].place+","+p[1]]
    p.set_lineno(0,p.lineno(1))

def p_BasicLit3(p):
    ''' BasicLit       		: IMAG '''
    p[0]=expr()
    p[0].type='complex'
    # p[0].value=complex(p[1])
    p[0].code=["=,"+p[0].place+","+p[1]]
    p.set_lineno(0,p.lineno(1))

# def p_FunctionLit(p):
#     ''' FunctionLit         : FUNC Signature Block '''
#
# def p_CompositeLit(p):
#     ''' CompositeLit   		: ID LiteralValue
#                             | LiteralType LiteralValue
#                             | LBRACK ELLIPSIS RBRACK Operand LiteralValue '''
#
# def p_LiteralValue(p):
#     ''' LiteralValue   		: LBRACE RBRACE
# 							| SEMICOLON RBRACE
# 							| LBRACE ElementList RBRACE
# 							| SEMICOLON ElementList RBRACE
# 							| LBRACE ElementList COMMA RBRACE
# 							| SEMICOLON ElementList COMMA RBRACE '''
#     # func(p,"LiteralValue")
#
# def p_ElementList(p):
#     ''' ElementList    		: KeyedElement
# 							| ElementList COMMA KeyedElement '''
#     # func(p,"ElementList")
#
# def p_KeyedElement(p):
#     ''' KeyedElement   		: Element
# 							| Key COLON Element '''
#     # func(p,"KeyedElement")
#
# def p_Key(p):
#     ''' Key            		: Expression
# 							| LiteralValue '''
#     # func(p,"Key")
#
# def p_Element(p):
#     ''' Element        		: Expression
# 							| LiteralValue '''

def p_assign_op(p):
    ''' assign_op      		: ASSIGN
							| ADD_ASSIGN
							| SUB_ASSIGN
							| MUL_ASSIGN
							| QUO_ASSIGN
							| REM_ASSIGN
							| AND_ASSIGN
							| OR_ASSIGN
							| XOR_ASSIGN
							| SHL_ASSIGN
							| SHR_ASSIGN
							| AND_NOT_ASSIGN
    '''
    p[0]=p[1]
    p.set_lineno(0,p.lineno(1))
    # func(p,"assign_op")

def p_rel_op(p):
    ''' rel_op         		: EQL
							| NEQ
							| LSS
							| LEQ
							| GTR
							| GEQ
    '''
    p[0]=p[1]

def p_add_op(p):
    ''' add_op         		: ADD
							| SUB
							| OR
							| XOR '''
    p[0]=p[1]

def p_mul_op(p):
    ''' mul_op         		: MUL
							| QUO
							| REM
							| SHL
							| SHR
							| AND
							| AND_NOT '''
    p[0]=p[1]

def p_unary_op(p):
    ''' unary_op       		: ADD
							| SUB
							| NOT
							| XOR
							| MUL
							| AND '''
							# | ARROW '''
    p[0]=p[1]

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

irf = open(args["out"], "w")
result = parser.parse(data,debug=1)
irf.close()
# print (result)
