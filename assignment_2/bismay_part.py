def p_SourceFile(p):
    ''' SourceFile       : PackageClause SEMICOLON SourceFile1 SourceFile2 '''

def p_SourceFile1(p):
    ''' SourceFile1      : SourceFile1 ImportDecl SEMICOLON
						  |   '''

def p_SourceFile2(p):
    ''' SourceFile2      : SourceFile2 TopLevelDecl SEMICOLON
						  |   '''

def p_PackageClause(p):
    ''' PackageClause    : PACKAGE PackageName '''

def p_PackageName(p):
    ''' PackageName      : ID '''

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
    ''' ImportPath       : string_lit '''

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
    ''' ConstDecl2       : ConstDecl2 ConstSpec SEMICOLON '''

def p_ConstSpec(p):
    ''' ConstSpec        : IdentifierList Type ASSIGN ExpressionList
						  | IdentifierList ASSIGN ExpressionList
						  | IdentifierList '''

def p_IdentifierList(p):
    ''' IdentifierList   : ID IdentifierList1 '''

def p_IdentifierList1(p):
    ''' IdentifierList1  : IdentifierList1 COMMA ID
						  |   '''

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

def p_TypeDef(p):
    ''' TypeDef          : ID Type '''

def p_VarDecl(p):
    ''' VarDecl          : VAR VarDecl1 '''

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

def p_FunctionBody(p):
    ''' FunctionBody     : Block '''

def p_Signature(p):
    ''' Signature        : Parameters
						  | Parameters Result '''

def p_Result(p):
    ''' Result           : Parameters
						  | Type '''

def p_Parameters(p):
    ''' Parameters       : LPAREN Parameters1 RPAREN '''

def p_Parameters1(p):
    ''' Parameters1      : ParameterList
						  | ParameterList COMMA
						  |   '''

def p_ParameterList(p):
    ''' ParameterList    : ParameterDecl ParameterList1 '''

def p_ParameterList1(p):
    ''' ParameterList1   : ParameterList1 COMMA ParameterDecl
						  |   '''

def p_ParameterDecl(p):
    ''' ParameterDecl    : ParameterDecl1 ParameterDecl2 Type '''

def p_ParameterDecl1(p):
    ''' ParameterDecl1   : IdentifierList
						  |   '''

def p_ParameterDecl2(p):
    ''' ParameterDecl2   : ELLIPSIS
						  |   '''

def p_MethodDecl(p):
    ''' MethodDecl       : FUNC Receiver MethodName Signature
						  | FUNC Receiver MethodName Signature FunctionBody '''

def p_Receiver(p):
    ''' Receiver         : Parameters '''

def p_MethodName(p):
    ''' MethodName       : ID '''

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
						  | GotoStmt '''

def p_Statement(p):
    ''' Statement   : FallthroughStmt
						  | Block
						  | IfStmt
						  | SwitchStmt
						  | SelectStmt
						  | ForStmt
						  | DeferStmt '''

def p_Declaration(p):
    ''' Declaration : ConstDecl
						  | TypeDecl
						  | VarDecl '''

def p_LabeledStmt(p):
    ''' LabeledStmt : Label COLON Statement '''

def p_Label(p):
    ''' Label       : ID '''

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
    ''' assign_op : assign_op_1 ASSIGN '''

def p_assign_op_1(p):
    ''' assign_op_1 : add_op
						  | mul_op
						  |   '''

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

def p_TopLevelDecl(p):
    ''' TopLevelDecl  : Declaration
						  | FunctionDecl
						  | MethodDecl '''
