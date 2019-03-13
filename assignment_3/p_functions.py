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
    # func(p,"SourceFile")

def p_PackageClause(p):
    ''' PackageClause  		: PACKAGE ID SEMICOLON '''
    # func(p,"PackageClause")

def p_ImportDeclList(p):
    ''' ImportDeclList 		: ImportDecl SEMICOLON
							| ImportDeclList ImportDecl SEMICOLON '''
    # func(p,"ImportDeclList")

def p_ImportDecl(p):
    ''' ImportDecl     		: IMPORT LPAREN ImportSpecList RPAREN
                            | IMPORT LPAREN RPAREN
							| IMPORT ImportSpec '''
    # func(p,"ImportDecl")

def p_ImportSpecList(p):
    ''' ImportSpecList 		: ImportSpec SEMICOLON
							| ImportSpecList ImportSpec SEMICOLON '''
    # func(p,"ImportSpecList")

def p_ImportSpec(p):
    ''' ImportSpec     		: ID ImportPath
							| PERIOD ImportPath
							| ImportPath '''
    # func(p,"ImportSpec")

def p_ImportPath(p):
    ''' ImportPath     		: STRING '''
    # func(p,"ImportPath")

def p_TopLevelDeclList(p):
    ''' TopLevelDeclList    : TopLevelDecl SEMICOLON
							| TopLevelDeclList TopLevelDecl SEMICOLON '''
    # func(p,"TopLevelDeclList")

def p_TopLevelDecl(p):
    ''' TopLevelDecl   		: Declaration
							| FunctionDecl
							| MethodDecl '''
    # func(p,"TopLevelDecl")

################################################################################
def p_OPENB(p):
    ''' OPENB          		: '''
    # func(p,"OPENB")

def p_CLOSEB(p):
    ''' CLOSEB         		: '''
    # func(p,"CLOSEB")

def p_StartScope(p):
    ''' StartScope         	: '''
    pushScope()

def p_EndScope(p):
    ''' EndScope    		: '''
    popScope()

def p_StructScope(p):
    '''StructScope          : '''
    pushScope(p[-1])

################################################################################
def p_FunctionDecl(p):
    ''' FunctionDecl   		: FUNC ID StartScope Signature EndScope
							| FUNC ID StartScope Signature Block EndScope '''

def p_MethodDecl(p):
    ''' MethodDecl     		: FUNC Parameters ID Signature
                            | FUNC Parameters ID Signature Block '''
    # func(p,"MethodDecl")

def p_Declaration(p):
    ''' Declaration    		: ConstDecl
                            | TypeDecl
							| VarDecl '''

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
    if checkID(p[1], 'curr'):
        raise KeyError("Symbol " + name + " already exists")
    else:
        scopeST[currScope][p[1]] = p[-1].copy()

################################################################################
def p_Type(p):
    ''' Type           		: VARTYPE '''
    p[0] = {}
    p[0]['type'] = p[1]
    p[0]['class'] = 'TYPE'

def p_Type(p):
    ''' Type           		: LiteralType '''
    p[0] = p[1]
    p[0]['class'] = 'TYPE'

def p_Type(p):
    ''' Type           		: ID '''
    if not checkID(p[1], 'curr'):
        raise KeyError("Type not defined")
    else:
        p[0] = (scopeST[currScope].getInfo(p[1])).copy()

def p_LiteralType(p):
    ''' LiteralType    		: ArrayType
							| StructType
							| PointerType
							| SliceType
                            | MapType '''
    p[0] = p[1]

def p_ArrayType(p):
    ''' ArrayType      		: LBRACK Expression RBRACK Type ''' # Must be integer
    p[0] = {}
    p[0]['type'] = 'ARRAY(' + p[4] + ')'
    p[0]['size'] = p[1]['place']

def p_StructType(p):
    ''' StructType     		: STRUCT StructScope LBRACE FieldDeclList RBRACE EndScope
							| STRUCT StructScope LBRACE RBRACE EndScope '''
    p[0] = {}
    p[0]['type'] = 'STRUCT'
    if len(p) == 5:
        p[0]['scopeno'] = p[4]

def p_FieldDeclList(p):
    ''' FieldDeclList  		: FieldDecl SEMICOLON
							| FieldDeclList FieldDecl SEMICOLON '''
    p[0] = currScope

def p_FieldDecl(p):
    ''' FieldDecl      		: IdentifierList Type STRING
							| IdentifierList Type '''
    for iden in p[1]:
        if checkID(iden, 'curr'):
            raise KeyError("Symbol " + iden + " already exists")
        (scopeST[currScope].table)[iden] = p[2].copy()
        scopeST[currScope].update(iden, 'class', 'FIELD')

def p_PointerType(p):
    ''' PointerType    		: MUL Type '''
    p[0] = {}
    p[0]['type'] = 'POINTER(' + p[2] + ')'

def p_SliceType(p):
    ''' SliceType      		: LBRACK RBRACK Type '''
    # func(p,"SliceType")

def p_MapType(p):
    ''' MapType        		: MAP LBRACK Type RBRACK Type '''
    # func(p,"MapType")

################################################################################
# def p_FunctionType(p):
#     ''' FunctionType        : FUNC Signature '''
#     # func(p,"FunctionType")

def p_Signature(p):
    ''' Signature      		: Parameters
                            | Parameters Type '''
                            # | Parameters Parameters
    p[0] = {}
    p[0]['scopeno'] = currScope
    p[0]['parameters'] = p[1]
    if len(p) > 2:
        p[0]['returntype'] = p[2]
        p[0]['']
    else:
        p[0]['returntype'] = {}

def p_Parameters(p):
    ''' Parameters     		: LPAREN RPAREN
							| LPAREN ParameterList RPAREN
							| LPAREN ParameterList COMMA RPAREN '''

def p_ParameterList(p):
    ''' ParameterList  		: ParameterDecl
							| ParameterList COMMA ParameterDecl '''

def p_ParameterDecl(p):
    ''' ParameterDecl  		: Type
                            | IdentifierList Type '''
    # func(p,"ParameterDecl")

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
        if checkID(iden, 'curr'):
            raise KeyError("Symbol " + iden + " already exists")
        (scopeST[currScope].table)[iden] = p[2].copy()
        scopeST[currScope].update(iden, 'class', 'VAR')

        # if p[2][type][0:5] == 'ARRAY':
        #     scopeST[currScope].update(iden, 'size', p[2]['size'])
        # if p[2][type] == 'STRUCT':
        #     scopeST[currScope].update(iden, 'scopeno', p[2]['scopeno'])
        # if p[2][type] == 'SLICE':
        #     scopeST[currScope].update(iden, '', p[2][''])
        # if p[2][type] == 'MAP':
        #     scopeST[currScope].update(iden, '', p[2][''])


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
    if len(p[1]) != len(p[2]):
        raise KeyError("Number of arguments do not match")
    for i in xrange(len(p[1])):
        # scopeST[currScope].update()

################################################################################
def p_Block(p):
    ''' Block          		: LBRACE StatementList RBRACE '''

    # func(p,"Block")

def p_StatementList(p):
    ''' StatementList  		: StatementList Statement SEMICOLON
							| Statement SEMICOLON '''
    # func(p,"StatementList")

def p_Statement(p):
    ''' Statement      		: Declaration
							| LabeledStmt
                            | SimpleStmt
                            | GoStmt
							| ReturnStmt
							| BreakStmt
							| ContinueStmt
							| GotoStmt
                            | FallthroughStmt
							| StartScope Block EndScope
							| IfStmt
                            | SwitchStmt
							| SelectStmt
							| ForStmt
                            | DeferStmt '''
    # func(p,"Statement")

def p_LabeledStmt(p):
    ''' LabeledStmt    		: ID COLON Statement '''
    # func(p,"LabeledStmt")

def p_SimpleStmt(p):
    ''' SimpleStmt     		: ShortVarDecl
                            | EmptyStmt
							| ExpressionStmt
							| SendStmt
                            | IncDecStmt
                            | Assignment '''
    # func(p,"SimpleStmt")

def p_EmptyStmt(p):
    ''' EmptyStmt      		: '''
    # func(p,"EmptyStmt")

def p_ExpressionStmt(p):
    ''' ExpressionStmt 		: Expression '''
    # func(p,"ExpressionStmt")

def p_SendStmt(p):
    ''' SendStmt 		    : Expression ARROW Expression '''
    # func(p,"SendStmt")

def p_IncDecStmt(p):
    ''' IncDecStmt     		: Expression INC
                            | Expression DEC '''
    # func(p,"IncDecStmt")

def p_Assignment(p):
    ''' Assignment     		: ExpressionList assign_op ExpressionList '''
    # func(p,"Assignment")

def p_GoStmt(p):
    '''GoStmt               : GO Expression'''
    # func(p,"GoStmt")

def p_ReturnStmt(p):
    ''' ReturnStmt     		: RETURN
							| RETURN ExpressionList '''
    # func(p,"ReturnStmt")

def p_BreakStmt(p):
    ''' BreakStmt      		: BREAK
							| BREAK ID '''
    # func(p,"BreakStmt")

def p_ContinueStmt(p):
    ''' ContinueStmt   		: CONTINUE
							| CONTINUE ID '''
    # func(p,"ContinueStmt")

def p_GotoStmt(p):
    ''' GotoStmt       		: GOTO ID '''
    # func(p,"GotoStmt")

def p_FallthroughStmt(p):
    ''' FallthroughStmt     : FALLTHROUGH '''
    # func(p,"FallthroughStmt")

################################################################################
def p_IfStmt(p):
    ''' IfStmt         		: IF OPENB Expression Block CLOSEB
							| IF OPENB SimpleStmt SEMICOLON Expression Block CLOSEB
							| IF OPENB Expression Block ELSE Block CLOSEB
							| IF OPENB Expression Block ELSE IfStmt CLOSEB
							| IF OPENB SimpleStmt SEMICOLON Expression Block ELSE IfStmt CLOSEB
							| IF OPENB SimpleStmt SEMICOLON Expression Block ELSE Block CLOSEB '''
    # func(p,"IfStmt")

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

def p_SelectStmt(p):
    ''' SelectStmt     		: SELECT LBRACE RBRACE
							| SELECT LBRACE CommClauseList RBRACE '''
    # func(p,"SelectStmt")

def p_CommClauseList(p):
    ''' CommClauseList     	: CommClause
                            | CommClauseList CommClause '''
    # func(p,"CommClause")

def p_CommClause(p):
    ''' CommClause     		: CommCase COLON StatementList '''
    # func(p,"CommClause")

def p_CommCase(p):
    ''' CommCase       		: CASE SendStmt
							| DEFAULT
							| CASE RecvStmt '''
    # func(p,"CommCase")

def p_RecvStmt(p):
    ''' RecvStmt       		: ExpressionList ASSIGN Expression
							| Expression
							| IdentifierList DEFINE Expression '''
    # func(p,"RecvStmt")

def p_ForStmt(p):
    ''' ForStmt : FOR ForStmt_1 Block '''
    # func(p,"ForStmt")

def p_ForStmt_1(p):
    ''' ForStmt_1 		    : Condition
							| ForClause
							| RangeClause
							| '''
    # func(p,"ForStmt_1")

def p_Condition(p):
    ''' Condition 		    : Expression '''
    # func(p,"Condition")

def p_ForClause(p):
    ''' ForClause 		    : ForClause_1 SEMICOLON ForClause_2 SEMICOLON ForClause_3 '''
    # func(p,"ForClause")

def p_ForClause_1(p):
    ''' ForClause_1 		: SimpleStmt '''
    # func(p,"ForClause_1")

def p_ForClause_2(p):
    ''' ForClause_2 		: Condition
							| '''
    # func(p,"ForClause_2")

def p_ForClause_3(p):
    ''' ForClause_3 		: SimpleStmt '''
    # func(p,"ForClause_3")

def p_RangeClause(p):
    ''' RangeClause 		: RangeClause_1 RANGE Expression '''
    # func(p,"RangeClause")

def p_RangeClause_1(p):
    ''' RangeClause_1 		: ExpressionList ASSIGN
							| IdentifierList DEFINE
							| '''
    # func(p,"RangeClause_1")

def p_DeferStmt(p):
    ''' DeferStmt           : DEFER Expression '''
    # func(p,"DeferStmt")

################################################################################
def p_ExpressionList(p):
    ''' ExpressionList  	: Expression
							| ExpressionList COMMA Expression '''
    # func(p,"ExpressionList")

def p_Expression(p):
    ''' Expression     		: Expression1
							| UnaryExpr assign_op Expression '''
    # func(p,"Expression")

def p_Expression1(p):
    ''' Expression1    		: Expression2
							| Expression1 LOR Expression2 '''
    # func(p,"Expression1")

def p_Expression2(p):
    ''' Expression2    		: Expression3
							| Expression2 LAND Expression3 '''
    # func(p,"Expression2")

def p_Expression3(p):
    ''' Expression3    		: Expression4
							| Expression3 rel_op Expression4 '''
    # func(p,"Expression3")

def p_Expression4(p):
    ''' Expression4    		: Expression5
							| Expression4 add_op Expression5 '''
    # func(p,"Expression4")

def p_Expression5(p):
    ''' Expression5    		: UnaryExpr
							| Expression5 mul_op UnaryExpr '''
    # func(p,"Expression5")

def p_UnaryExpr(p):
    ''' UnaryExpr      		: PrimaryExpr
							| unary_op UnaryExpr '''
    # func(p,"UnaryExpr")

def p_PrimaryExpr(p):
    ''' PrimaryExpr    		: Operand
                            | MethodExpr
							| PrimaryExpr Selector
							| PrimaryExpr Index
							| PrimaryExpr Slice
							| PrimaryExpr TypeAssertion
							| PrimaryExpr Arguments '''
    # func(p,"PrimaryExpr")

# def p_Conversion(p):
#     ''' Conversion        	: Type LPAREN Expression COMMA RPAREN
# 							| Type LPAREN Expression RPAREN '''
#     # func(p,"Conversion")

def p_MethodExpr(p):
    ''' MethodExpr       	: Type PERIOD ID '''
    # func(p,"MethodExpr")

def p_Selector(p):
    ''' Selector       		: PERIOD ID '''
    # func(p,"Selector")

def p_Index(p):
    ''' Index          		: LBRACK Expression RBRACK '''
    # func(p,"Index")

def p_Slice(p):
    ''' Slice          		: LBRACK COLON RBRACK
							| LBRACK COLON Expression RBRACK
							| LBRACK Expression COLON RBRACK
							| LBRACK Expression COLON Expression RBRACK
							| LBRACK COLON Expression COLON Expression RBRACK
							| LBRACK Expression COLON Expression COLON Expression RBRACK '''
    # func(p,"Slice")

def p_TypeAssertion(p):
    ''' TypeAssertion  		: PERIOD LPAREN Type RPAREN '''
    # func(p,"TypeAssertion")

def p_Arguments(p):
    # ''' Arguments      		: LPAREN RPAREN
	# 						| LPAREN ExpressionList RPAREN
	# 						| LPAREN ExpressionList ELLIPSIS RPAREN '''
    ''' Arguments           : LPAREN RPAREN
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
    # func(p,"Arguments")

def p_Operand(p):
    ''' Operand        		: Literal
							| ID
                            | ID PERIOD ID
							| LPAREN Expression RPAREN '''
    # func(p,"Operand")

def p_Literal(p):
    ''' Literal        		: BasicLit
                            | FunctionLit
							| CompositeLit '''
    # func(p,"Literal")

def p_BasicLit(p):
    ''' BasicLit       		: INT
							| FLOAT
							| STRING
							| IMAG '''
    # func(p,"BasicLit")

def p_FunctionLit(p):
    ''' FunctionLit         : FUNC Signature Block '''
    # func(p,"FunctionLit")

def p_CompositeLit(p):
    ''' CompositeLit   		: ID LiteralValue
                            | LiteralType LiteralValue
                            | LBRACK ELLIPSIS RBRACK Operand LiteralValue '''
    # func(p,"CompositeLit")

def p_LiteralValue(p):
    ''' LiteralValue   		: LBRACE RBRACE
							| SEMICOLON RBRACE
							| LBRACE ElementList RBRACE
							| SEMICOLON ElementList RBRACE
							| LBRACE ElementList COMMA RBRACE
							| SEMICOLON ElementList COMMA RBRACE '''
    # func(p,"LiteralValue")

def p_ElementList(p):
    ''' ElementList    		: KeyedElement
							| ElementList COMMA KeyedElement '''
    # func(p,"ElementList")

def p_KeyedElement(p):
    ''' KeyedElement   		: Element
							| Key COLON Element '''
    # func(p,"KeyedElement")

def p_Key(p):
    ''' Key            		: Expression
							| LiteralValue '''
    # func(p,"Key")

def p_Element(p):
    ''' Element        		: Expression
							| LiteralValue '''
    # func(p,"Element")

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
							| AND_NOT_ASSIGN '''
    # func(p,"assign_op")

def p_rel_op(p):
    ''' rel_op         		: EQL
							| NEQ
							| LSS
							| LEQ
							| GTR
							| GEQ '''
    # func(p,"rel_op")

def p_add_op(p):
    ''' add_op         		: ADD
							| SUB
							| OR
							| XOR '''
    # func(p,"add_op")

def p_mul_op(p):
    ''' mul_op         		: MUL
							| QUO
							| REM
							| SHL
							| SHR
							| AND
							| AND_NOT '''
    # func(p,"mul_op")

def p_unary_op(p):
    ''' unary_op       		: ADD
							| SUB
							| NOT
							| XOR
							| MUL
							| AND
							| ARROW '''
    # func(p,"unary_op")
