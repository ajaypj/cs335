import re
import argparse
import ply.lex as lex
import ply.yacc as yacc

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

tokens = operators + numbers + strings + special + ['ID'] + list(reserved.values())


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



def p_SourceFile(p):
    ''' SourceFile       : PackageClause SEMICOLON SourceFile1 SourceFile2 '''
    print "Parsed"

def p_SourceFile1(p):
    ''' SourceFile1      : SourceFile1 ImportDecl SEMICOLON
						  |   '''

def p_SourceFile2(p):
    ''' SourceFile2      : SourceFile2 TopLevelDecl SEMICOLON
						  |   '''

def p_PackageClause(p):
    ''' PackageClause    : PACKAGE PackageName '''
    print "PackageClause"

def p_PackageName(p):
    ''' PackageName      : ID '''
    print "PackageName"

def p_ImportDecl(p):
    ''' ImportDecl       : IMPORT ImportDecl1 '''

def p_ImportDecl1(p):
    ''' ImportDecl1      : ImportSpec
						  | LPAREN ImportDecl2 RPAREN '''

def p_ImportDecl2(p):
    ''' ImportDecl2      : ImportDecl2 ImportSpec SEMICOLON
						  |   '''

def p_ImportSpec(p):
    ''' ImportSpec       : PERIOD ImportPath
						  | PackageName ImportPath
						  | ImportPath '''

def p_ImportPath(p):
    ''' ImportPath       : STRING '''

def p_TopLevelDecl(p):
    ''' TopLevelDecl     : Declaration
						  | FunctionDecl
						  | MethodDecl '''

def p_Declaration(p):
    ''' Declaration      : ConstDecl
						  | TypeDecl
						  | VarDecl '''

def p_ConstDecl(p):
    ''' ConstDecl        : CONST ConstDecl1 '''

def p_ConstDecl1(p):
    ''' ConstDecl1       : ConstSpec
						  | LPAREN ConstDecl2 RPAREN '''

def p_ConstDecl2(p):
    ''' ConstDecl2       : ConstDecl2 ConstSpec SEMICOLON
                         | '''

def p_ConstSpec(p):
    ''' ConstSpec        : IdentifierList Type ASSIGN ExpressionList
						  | IdentifierList ASSIGN ExpressionList
						  | IdentifierList '''

def p_ExpressionList(p):
    ''' ExpressionList   : Expression ExpressionList1 '''

def p_ExpressionList1(p):
    ''' ExpressionList1  : ExpressionList1 COMMA Expression
						  |   '''

def p_TypeDecl(p):
    ''' TypeDecl         : TYPE TypeDecl1 '''

def p_TypeDecl1(p):
    ''' TypeDecl1        : TypeSpec
						  | LPAREN TypeDecl2 RPAREN '''

def p_TypeDecl2(p):
    ''' TypeDecl2        : TypeDecl2 TypeSpec SEMICOLON
						  |   '''

def p_TypeSpec(p):
    ''' TypeSpec         : AliasDecl
						  | TypeDef '''

def p_AliasDecl(p):
    ''' AliasDecl        : ID ASSIGN Type '''
    print "AliasDecl"

def p_TypeDef(p):
    ''' TypeDef          : ID Type '''
    print "TypeDef"

def p_VarDecl(p):
    ''' VarDecl          : VAR VarDecl1 '''
    print "VarDecl"


def p_VarDecl1(p):
    ''' VarDecl1         : VarSpec
						  | LPAREN VarDecl2 RPAREN '''

def p_VarDecl2(p):
    ''' VarDecl2         : VarDecl2 VarSpec SEMICOLON
						  |   '''

def p_VarSpec(p):
    ''' VarSpec          : IdentifierList VarSpec1 '''

def p_VarSpec1(p):
    ''' VarSpec1         : Type ASSIGN ExpressionList
						  | ASSIGN ExpressionList
						  | Type '''

def p_FunctionDecl(p):
    ''' FunctionDecl     : FUNC FunctionName Signature
						  | FUNC FunctionName Signature FunctionBody '''

def p_FunctionName(p):
    ''' FunctionName     : ID '''
    print "FunctionName"

def p_FunctionBody(p):
    ''' FunctionBody     : Block '''

def p_Signature(p):
    ''' Signature        : Parameters
						  | Parameters Result '''

def p_Result(p):
    ''' Result           : Parameters
						  | Type '''


def p_MethodDecl(p):
    ''' MethodDecl       : FUNC Receiver MethodName Signature
						  | FUNC Receiver MethodName Signature FunctionBody '''

def p_Receiver(p):
    ''' Receiver         : Parameters '''


def p_Block(p):
    ''' Block : LBRACE StatementList RBRACE '''

def p_StatementList(p):
    ''' StatementList : StatementList1 '''

def p_StatementList1(p):
    ''' StatementList1 : StatementList1 Statement SEMICOLON
						  |   '''

def p_Statement(p):
    ''' Statement   : Declaration
					  | LabeledStmt
					  | SimpleStmt
					  | GoStmt
					  | ReturnStmt
					  | BreakStmt
					  | ContinueStmt
					  | GotoStmt
                      | FallthroughStmt
    				  | Block
					  | IfStmt
					  | SwitchStmt
					  | SelectStmt
					  | ForStmt
					  | DeferStmt'''



def p_LabeledStmt(p):
    ''' LabeledStmt : Label COLON Statement '''

def p_Label(p):
    ''' Label       : ID '''
    print "Label"

def p_SimpleStmt(p):
    ''' SimpleStmt  : EmptyStmt
						  | ExpressionStmt
						  | SendStmt
						  | IncDecStmt
						  | Assignment
						  | ShortVarDecl '''

def p_EmptyStmt(p):
    ''' EmptyStmt   : '''

def p_ExpressionStmt(p):
    ''' ExpressionStmt : Expression '''

def p_SendStmt(p):
    ''' SendStmt : Channel ARROW Expression '''

def p_Channel(p):
    ''' Channel  : Expression '''

def p_IncDecStmt(p):
    ''' IncDecStmt : Expression IncDecStmt_1 '''

def p_IncDecStmt_1(p):
    ''' IncDecStmt_1 : INC
						  | DEC '''

def p_Assignment(p):
    ''' Assignment : ExpressionList assign_op ExpressionList '''

def p_assign_op(p):
    ''' assign_op : ADD_ASSIGN
                | SUB_ASSIGN
                | MUL_ASSIGN
                | QUO_ASSIGN
                | REM_ASSIGN
                | AND_ASSIGN
                | OR_ASSIGN
                | XOR_ASSIGN
                | SHL_ASSIGN
                | SHR_ASSIGN
                | AND_NOT_ASSIGN '''




def p_ShortVarDecl(p):
    ''' ShortVarDecl : IdentifierList DEFINE ExpressionList '''

def p_GoStmt(p):
    ''' GoStmt : GO Expression '''

def p_ReturnStmt(p):
    ''' ReturnStmt : RETURN ReturnStmt_1 '''

def p_ReturnStmt_1(p):
    ''' ReturnStmt_1 : ExpressionList
						  |   '''

def p_BreakStmt(p):
    ''' BreakStmt : BREAK BreakStmt_1 '''

def p_BreakStmt_1(p):
    ''' BreakStmt_1 : Label
						  |   '''

def p_ContinueStmt(p):
    ''' ContinueStmt : CONTINUE ContinueStmt_1 '''

def p_ContinueStmt_1(p):
    ''' ContinueStmt_1 : Label
						  |   '''

def p_GotoStmt(p):
    ''' GotoStmt : GOTO Label '''

def p_FallthroughStmt(p):
    ''' FallthroughStmt : FALLTHROUGH '''

def p_IfStmt(p):
    ''' IfStmt : IF IfStmt_1 Expression Block IfStmt_2 '''

def p_IfStmt_1(p):
    ''' IfStmt_1 : SimpleStmt SEMICOLON
						  |   '''

def p_IfStmt_2(p):
    ''' IfStmt_2 : ELSE IfStmt_2_1
						  |   '''

def p_IfStmt_2_1(p):
    ''' IfStmt_2_1 : IfStmt
						  | Block '''

def p_SwitchStmt(p):
    ''' SwitchStmt : ExprSwitchStmt
						  | TypeSwitchStmt '''

def p_ExprSwitchStmt(p):
    ''' ExprSwitchStmt : SWITCH ExprSwitchStmt_1 ExprSwitchStmt_2 LBRACE ExprSwitchStmt_3 RBRACE '''

def p_ExprSwitchStmt_1(p):
    ''' ExprSwitchStmt_1 : SimpleStmt SEMICOLON
						  |   '''

def p_ExprSwitchStmt_2(p):
    ''' ExprSwitchStmt_2 : Expression
						  |   '''

def p_ExprSwitchStmt_3(p):
    ''' ExprSwitchStmt_3 : ExprSwitchStmt_3 ExprCaseClause
						  |   '''

def p_ExprCaseClause(p):
    ''' ExprCaseClause : ExprSwitchCase COLON StatementList '''

def p_ExprSwitchCase(p):
    ''' ExprSwitchCase : CASE ExpressionList
						  | DEFAULT '''

def p_TypeSwitchStmt(p):
    ''' TypeSwitchStmt  : SWITCH TypeSwitchStmt_1 TypeSwitchGuard LBRACE TypeSwitchStmt_2 RBRACE '''

def p_TypeSwitchStmt_1(p):
    ''' TypeSwitchStmt_1 : SimpleStmt SEMICOLON
						  |   '''

def p_TypeSwitchStmt_2(p):
    ''' TypeSwitchStmt_2 : TypeSwitchStmt_2 TypeCaseClause
						  |   '''

def p_TypeSwitchGuard(p):
    ''' TypeSwitchGuard : TypeSwitchGuard_1 PrimaryExpr PERIOD LPAREN TYPE RPAREN '''

def p_TypeSwitchGuard_1(p):
    ''' TypeSwitchGuard_1 : ID DEFINE
						  |   '''
    print "TypeSwitchGuard_1"

def p_TypeCaseClause(p):
    ''' TypeCaseClause  : TypeSwitchCase COLON StatementList '''

def p_TypeSwitchCase(p):
    ''' TypeSwitchCase  : CASE TypeList
						  | DEFAULT '''

def p_TypeList(p):
    ''' TypeList        : Type TypeList_1 '''

def p_TypeList_1(p):
    ''' TypeList_1 : TypeList_1 COMMA Type
						  |   '''

def p_SelectStmt(p):
    ''' SelectStmt : SELECT LBRACE SelectStmt_1 RBRACE '''

def p_SelectStmt_1(p):
    ''' SelectStmt_1 : SelectStmt_1 CommClause
						  |   '''

def p_CommClause(p):
    ''' CommClause : CommCase COLON StatementList '''

def p_CommCase(p):
    ''' CommCase   : CASE CommCase_1
						  | DEFAULT '''

def p_CommCase_1(p):
    ''' CommCase_1 : SendStmt
						  | RecvStmt '''

def p_RecvStmt(p):
    ''' RecvStmt   : RecvStmt_1 RecvExpr '''

def p_RecvStmt_1(p):
    ''' RecvStmt_1 : ExpressionList ASSIGN
						  | IdentifierList DEFINE
						  |   '''

def p_RecvExpr(p):
    ''' RecvExpr   : Expression '''

def p_ForStmt(p):
    ''' ForStmt : FOR ForStmt_1 Block '''

def p_ForStmt_1(p):
    ''' ForStmt_1 : Condition
						  | ForClause
						  | RangeClause
						  |   '''

def p_Condition(p):
    ''' Condition : Expression '''

def p_ForClause(p):
    ''' ForClause : ForClause_1 SEMICOLON ForClause_2 SEMICOLON ForClause_3 '''

def p_ForClause_1(p):
    ''' ForClause_1 : InitStmt
						  |   '''

def p_ForClause_2(p):
    ''' ForClause_2 : Condition
						  |   '''

def p_ForClause_3(p):
    ''' ForClause_3 : PostStmt
						  |   '''

def p_InitStmt(p):
    ''' InitStmt : SimpleStmt '''

def p_PostStmt(p):
    ''' PostStmt : SimpleStmt '''

def p_RangeClause(p):
    ''' RangeClause : RangeClause_1 RANGE Expression '''

def p_RangeClause_1(p):
    ''' RangeClause_1 : ExpressionList ASSIGN
						  | IdentifierList DEFINE
						  |   '''

def p_DeferStmt(p):
    ''' DeferStmt : DEFER Expression '''




#################### Ajay
def p_Type(p):
    ''' Type : TypeName
			 | TypeLit
			 | LPAREN Type RPAREN '''
    if p[1]=='(':
        print "LPAREN Type RPAREN"


def p_TypeName(p):
    ''' TypeName : ID
				 |  QualifiedIdent '''
    print "TypeName",p[1]
def p_TypeLit(p):
    ''' TypeLit : ArrayType
				 | StructType
				 | PointerType
				 | FunctionType
				 | InterfaceType
				 | SliceType
				 | MapType
				 | ChannelType '''


def p_ArrayType(p):
    ''' ArrayType   : LBRACK ArrayLength RBRACK ElementType '''

###############  Have changed Expression to INT HERE
def p_ArrayLength(p):
    ''' ArrayLength : INT '''
def p_ElementType(p):
    ''' ElementType : Type '''
def p_StructType(p):
    ''' StructType    : STRUCT LBRACE FieldDecl_1 RBRACE '''
def p_FieldDecl_1(p):
    ''' FieldDecl_1 :
						 | FieldDecl_1 FieldDecl SEMICOLON '''
def p_FieldDecl(p):
    ''' FieldDecl     : LPAREN IdentifierList Type
						 | EmbeddedField RPAREN LBRACK Tag RBRACK '''
def p_EmbeddedField(p):
    ''' EmbeddedField : LBRACK MUL RBRACK TypeName '''
def p_Tag(p):
    ''' Tag           : STRING '''
def p_IdentifierList(p):
    ''' IdentifierList : ID
                        | ID COMMA IdentifierList'''
    print "IdentifierList"

def p_PointerType(p):
    ''' PointerType : MUL BaseType '''
def p_BaseType(p):
    ''' BaseType    : Type '''
def p_FunctionType(p):
    ''' FunctionType   : FUNC Signature '''

def p_Parameters(p):
    ''' Parameters     : LPAREN RPAREN
                        | LPAREN Parameters_1 RPAREN '''

def p_FunctionType_Parameters_Comma_1(p):
    ''' FunctionType_Parameters_Comma_1 :
						 | COMMA '''
def p_Parameters_1(p):
    ''' Parameters_1 : ParameterList FunctionType_Parameters_Comma_1 '''
# def p_ParameterList(p):
#     ''' ParameterList  : ParameterDecl ParameterList_1  '''
#
# def p_ParameterList_1(p):
#     ''' ParameterList_1 :
# 						 | ParameterList_1 COMMA ParameterDecl '''

def p_ParameterList(p):
    ''' ParameterList  : ParameterDecl COMMA ParameterList
                        | ParameterDecl'''


def p_ParameterDecl(p):
    ''' ParameterDecl  : IdentifierList ELLIPSIS Type
                       | ELLIPSIS Type
                       | IdentifierList Type
                       | Type '''

def p_InterfaceType(p):
    ''' InterfaceType      : INTERFACE LBRACE InterfaceType_1 RBRACE '''

def p_InterfaceType_1(p):
    ''' InterfaceType_1 :
						 | InterfaceType_1 MethodSpec SEMICOLON '''
def p_MethodSpec(p):
    ''' MethodSpec         : MethodName Signature
						 | InterfaceTypeName '''

def p_MethodName(p):
    ''' MethodName         : ID '''
    print "MethodName"

def p_InterfaceTypeName(p):
    ''' InterfaceTypeName  : TypeName '''

def p_SliceType(p):
    ''' SliceType : LBRACK RBRACK ElementType '''

def p_MapType(p):
    ''' MapType     : MAP LBRACK KeyType RBRACK ElementType '''

def p_KeyType(p):
    ''' KeyType     : Type '''

def p_ChannelType(p):
    ''' ChannelType : ChannelType_1 ElementType '''

def p_ChannelType_1(p):
    ''' ChannelType_1 : CHAN
					 | CHAN ARROW
					 | ARROW CHAN '''


###############   Siddhant

def p_Operand(p):
    ''' Operand         : LPAREN Expression RPAREN
						| OperandName
						| Literal '''
def p_OperandName(p):
    ''' OperandName     : ID
						| QualifiedIdent '''
    print "OperandName"
def p_QualifiedIdent(p):
    ''' QualifiedIdent  : ID PERIOD ID '''
    print "QualifiedIdent"
def p_Literal(p):
    ''' Literal         : BasicLiteral
						| CompositeLit
						| FunctionLit '''
def p_BasicLiteral(p):
    ''' BasicLiteral    : INT
						| FLOAT
						| IMAG
						| STRING'''
						# | RUNE '''

def p_CompositeLit(p):
    ''' CompositeLit    : LiteralType LiteralValue '''
def p_LiteralType(p):
    ''' LiteralType     : StructType
						| ArrayType
						| LBRACK ELLIPSIS RBRACK ElementType
						| SliceType
						| MapType
						| TypeName '''
def p_LiteralValue(p):
    ''' LiteralValue    : LBRACE LiteralValue1 RBRACE
                        | LBRACE RBRACE '''
def p_LiteralValue1(p):
    ''' LiteralValue1   : ElementList COMMA
						| ElementList '''
def p_ElementList(p):
    ''' ElementList     : KeyedElement
						| ElementList COMMA KeyedElement '''
def p_KeyedElement(p):
    ''' KeyedElement    : Key COLON Element
                        | Element '''
def p_Key(p):
    ''' Key             : ID
						| Expression
						| LiteralValue '''
    print "Key"
def p_Element(p):
    ''' Element         : Expression
						| LiteralValue '''

def p_FunctionLit(p):
    ''' FunctionLit     : FUNC Signature FunctionBody '''
    print "p_FunctionLit"

def p_PrimaryExpr(p):
    ''' PrimaryExpr     : Operand
						| Conversion
						| MethodExpr
						| PrimaryExpr Selector
						| PrimaryExpr Index
						| PrimaryExpr Slice
						| PrimaryExpr TypeAssertion
						| PrimaryExpr Arguments '''
def p_Conversion(p):
    ''' Conversion      : Type LPAREN Expression RPAREN
						| Type LPAREN Expression COMMA RPAREN '''
def p_Selector(p):
    ''' Selector        : PERIOD ID '''
    print "Selector"
def p_Index(p):
    ''' Index           : LBRACK Expression RBRACK '''
def p_Slice(p):
    ''' Slice           : LBRACK Expression COLON Expression RBRACK
						| LBRACK Expression COLON RBRACK
                        | LBRACK COLON Expression RBRACK
                        | LBRACK COLON RBRACK
                        | LBRACK Expression COLON Expression COLON Expression RBRACK
                        | LBRACK COLON Expression COLON Expression RBRACK '''
def p_TypeAssertion(p):
    ''' TypeAssertion   : PERIOD LPAREN Type RPAREN '''
def p_Arguments(p):
    ''' Arguments       : LPAREN RPAREN
						| LPAREN ExpressionList ELLIPSIS COMMA RPAREN
						| LPAREN ExpressionList ELLIPSIS RPAREN
						| LPAREN ExpressionList COMMA RPAREN
						| LPAREN ExpressionList RPAREN
						| LPAREN Type COMMA ExpressionList ELLIPSIS COMMA RPAREN
						| LPAREN Type COMMA ExpressionList ELLIPSIS RPAREN
						| LPAREN Type COMMA ExpressionList COMMA RPAREN
						| LPAREN Type COMMA ExpressionList RPAREN
						| LPAREN Type ELLIPSIS COMMA RPAREN
						| LPAREN Type ELLIPSIS RPAREN
						| LPAREN Type COMMA RPAREN
						| LPAREN Type RPAREN '''

def p_MethodExpr(p):
    ''' MethodExpr      : ReceiverType PERIOD MethodName '''
def p_ReceiverType(p):
    ''' ReceiverType    : Type '''

def p_Expression(p):
    ''' Expression      : UnaryExpr
						| Expression binary_op Expression '''
def p_UnaryExpr(p):
    ''' UnaryExpr       : PrimaryExpr
						| unary_op UnaryExpr '''
def p_binary_op(p):
    ''' binary_op       : LOR
						| LAND
						| rel_op
						| add_op
						| mul_op '''
def p_rel_op(p):
    ''' rel_op          : EQL
						| NEQ
						| LSS
						| LEQ
						| GTR
						| GEQ '''
def p_add_op(p):
    ''' add_op          : ADD
						| SUB
						| OR
						| XOR '''
def p_mul_op(p):
    ''' mul_op          : MUL
						| QUO
						| REM
						| SHL
						| SHR
						| AND
						| AND_NOT '''
def p_unary_op(p):
    ''' unary_op        : ADD
						| SUB
						| NOT
						| XOR
						| MUL
						| AND
						| ARROW '''






precedence = (
    ('nonassoc','ID','STRING','INT','FLOAT','BREAK',  'DEFAULT',  'FUNC',  'INTERFACE',  'SELECT',  'CASE',  'DEFER',  'GO',  'MAP',  'STRUCT',
    'CHAN',  'ELSE',  'GOTO',  'PACKAGE',  'SWITCH',  'CONST',  'FALLTHROUGH',  'IF',
    'RANGE',  'TYPE',  'CONTINUE',  'FOR',  'IMPORT',  'RETURN',  'VAR'),
    ('left', 'COMMA'),
    ('right', 'ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'QUO_ASSIGN', 'REM_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN', 'SHL_ASSIGN', 'SHR_ASSIGN'),
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
    ('left', 'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'ARROW', 'PERIOD')
)

# precedence =(
#     ('left','COMMA'),
#     ('right','EQL','ADD_ASSIGN','SUB_ASSIGN','MUL_ASSIGN','QUO_ASSIGN',
#     'REM_ASSIGN','SHL_ASSIGN','SHR_ASSIGN','AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN'),
#     ('right','COND'),
#     ('',''),
#     (),
#     (),
#     (),
#     (),
#     (),
#     (),
#     (),
#     (),
# )



############################################################# Build the parser




parser = yacc.yacc()

f = open(args["in"], "r")
data = f.read()
f.close()


result = parser.parse(data,debug=1)
print (result)
