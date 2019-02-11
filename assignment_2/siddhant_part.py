def p_Operand:
    ''' Operand         : LPAREN Expression RPAREN
						| OperandName
						| Literal '''

def p_OperandName:
    ''' OperandName     : ID
						| QualifiedIdent '''

def p_QualifiedIdent:
    ''' QualifiedIdent  : PackageName PERIOD ID '''

def p_PackageName:
    ''' PackageName     : ID '''

def p_Literal:
    ''' Literal         : BasicLiteral
						| CompositeLit
						| FunctionLit '''

def p_BasicLiteral:
    ''' BasicLiteral    : INT
						| FLOAT
						| IMAG
						| STRING
						| RUNE '''

def p_CompositeLit:
    ''' CompositeLit    : LiteralType LiteralValue '''

def p_LiteralType:
    ''' LiteralType     : StructType
						| ArrayType
						| LBRACK ELLIPSIS RBRACK ElementType
						| SliceType
						| MapType
						| TypeName '''

def p_LiteralValue:
    ''' LiteralValue    : LBRACE LiteralValue1 RBRACE '''

def p_LiteralValue1:
    ''' LiteralValue1   : ElementList COMMA
						| ElementList '''

def p_ElementList:
    ''' ElementList     : KeyedElement ElementList1
						| '''

def p_KeyedElement:
    ''' KeyedElement    : KeyedElement1 Element '''

def p_KeyedElement1:
    ''' KeyedElement1   : Key COLON
						| '''

def p_Key:
    ''' Key             : FieldName
						| Expression
						| LiteralValue '''

def p_FieldName:
    ''' FieldName       : ID '''

def p_Element:
    ''' Element         : Expression
						| LiteralValue '''

def p_FunctionLit:
    ''' FunctionLit     : FUNC Signature FunctionBody '''

def p_PrimaryExpr:
    ''' PrimaryExpr     : Operand
						| Conversion
						| MethodExpr
						| PrimaryExpr Selector
						| PrimaryExpr Index
						| PrimaryExpr Slice
						| PrimaryExpr TypeAssertion
						| PrimaryExpr Arguments '''

def p_Conversion:
    ''' Conversion      : Type LPAREN Expression RPAREN
						| Type LPAREN Expression COMMA RPAREN '''

def p_Selector:
    ''' Selector        : PERIOD ID '''

def p_Index:
    ''' Index           : LBRACK Expression RBRACK '''

def p_Slice:
    ''' Slice           : LBRACK Slice1 COLON Slice1 RBRACK
						| LBRACK Slice1 COLON Expression COLON Expression RBRACK '''

def p_Slice1:
    ''' Slice1          : Expression
						| '''

def p_TypeAssertion:
    ''' TypeAssertion   : PERIOD LPAREN Type RPAREN '''

def p_Arguments:
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

def p_MethodExpr:
    ''' MethodExpr      : ReceiverType PERIOD MethodName '''

def p_Receivertype:
    ''' Receivertype    : Type '''

def p_Expression:
    ''' Expression      : UnaryExpr
						| Expression binary_op Expression '''

def p_UnaryExpr:
    ''' UnaryExpr       : PrimaryExpr
						| unary_op UnaryExpr '''

def p_binary_op:
    ''' binary_op       : LOR
						| LAND
						| rel_op
						| add_op
						| mul_op '''

def p_rel_op:
    ''' rel_op          : EQL
						| NEQ
						| LSS
						| LEQ
						| GTR
						| GEQ '''

def p_add_op:
    ''' add_op          : ADD
						| SUB
						| OR
						| XOR '''

def p_mul_op:
    ''' mul_op          : MUL
						| QUO
						| REM
						| SHL
						| SHR
						| AND
						| AND_NOT '''

def p_unary_op:
    ''' unary_op        : ADD
						| SUB
						| NOT
						| XOR
						| MUL
						| AND
						| ARROW '''
