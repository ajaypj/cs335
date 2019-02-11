def p_SourceFile:
    ''' SourceFile       : PackageClause SEMICOLON SourceFile1 SourceFile2 '''

def p_SourceFile1:
    ''' SourceFile1      : SourceFile1 ImportDecl SEMICOLON
						  |   '''

def p_SourceFile2:
    ''' SourceFile2      : SourceFile2 TopLevelDecl SEMICOLON
						  |   '''

def p_PackageClause:
    ''' PackageClause    : PACKAGE PackageName '''

def p_PackageName:
    ''' PackageName      : ID '''

def p_ImportDecl:
    ''' ImportDecl       : IMPORT ImportDecl1 '''

def p_ImportDecl1:
    ''' ImportDecl1      : ImportSpec
						  | LPAREN ImportDecl2 RPAREN '''

def p_ImportDecl2:
    ''' ImportDecl2      : ImportDecl2 ImportSpec SEMICOLON
						  |   '''

def p_ImportSpec:
    ''' ImportSpec       : PERIOD ImportPath
						  | PackageName ImportPath
						  | ImportPath '''

def p_ImportPath:
    ''' ImportPath       : string_lit '''

def p_TopLevelDecl:
    ''' TopLevelDecl     : Declaration
						  | FunctionDecl
						  | MethodDecl '''

def p_Declaration:
    ''' Declaration      : ConstDecl
						  | TypeDecl
						  | VarDecl '''

def p_ConstDecl:
    ''' ConstDecl        : CONST ConstDecl1 '''

def p_ConstDecl1:
    ''' ConstDecl1       : ConstSpec
						  | LPAREN ConstDecl2 RPAREN '''

def p_ConstDecl2:
    ''' ConstDecl2       : ConstDecl2 ConstSpec SEMICOLON '''

def p_ConstSpec:
    ''' ConstSpec        : IdentifierList Type ASSIGN ExpressionList
						  | IdentifierList ASSIGN ExpressionList
						  | IdentifierList '''

def p_IdentifierList:
    ''' IdentifierList   : ID IdentifierList1 '''

def p_IdentifierList1:
    ''' IdentifierList1  : IdentifierList1 COMMA ID
						  |   '''

def p_ExpressionList:
    ''' ExpressionList   : Expression ExpressionList1 '''

def p_ExpressionList1:
    ''' ExpressionList1  : ExpressionList1 COMMA Expression
						  |   '''

def p_TypeDecl:
    ''' TypeDecl         : TYPE TypeDecl1 '''

def p_TypeDecl1:
    ''' TypeDecl1        : TypeSpec
						  | LPAREN TypeDecl2 RPAREN '''

def p_TypeDecl2:
    ''' TypeDecl2        : TypeDecl2 TypeSpec SEMICOLON
						  |   '''

def p_TypeSpec:
    ''' TypeSpec         : AliasDecl
						  | TypeDef '''

def p_AliasDecl:
    ''' AliasDecl        : ID ASSIGN Type '''

def p_TypeDef:
    ''' TypeDef          : ID Type '''

def p_VarDecl:
    ''' VarDecl          : VAR VarDecl1 '''

def p_VarDecl1:
    ''' VarDecl1         : VarSpec
						  | LPAREN VarDecl2 RPAREN '''

def p_VarDecl2:
    ''' VarDecl2         : VarDecl2 VarSpec SEMICOLON
						  |   '''

def p_VarSpec:
    ''' VarSpec          : IdentifierList VarSpec1 '''

def p_VarSpec1:
    ''' VarSpec1         : Type ASSIGN ExpressionList
						  | ASSIGN ExpressionList
						  | Type '''

def p_FunctionDecl:
    ''' FunctionDecl     : FUNC FunctionName Signature
						  | FUNC FunctionName Signature FunctionBody '''

def p_FunctionName:
    ''' FunctionName     : ID '''

def p_FunctionBody:
    ''' FunctionBody     : Block '''

def p_Signature:
    ''' Signature        : Parameters
						  | Parameters Result '''

def p_Result:
    ''' Result           : Parameters
						  | Type '''

def p_Parameters:
    ''' Parameters       : LPAREN Parameters1 RPAREN '''

def p_Parameters1:
    ''' Parameters1      : ParameterList
						  | ParameterList COMMA
						  |   '''

def p_ParameterList:
    ''' ParameterList    : ParameterDecl ParameterList1 '''

def p_ParameterList1:
    ''' ParameterList1   : ParameterList1 COMMA ParameterDecl
						  |   '''

def p_ParameterDecl:
    ''' ParameterDecl    : ParameterDecl1 ParameterDecl2 Type '''

def p_ParameterDecl1:
    ''' ParameterDecl1   : IdentifierList
						  |   '''

def p_ParameterDecl2:
    ''' ParameterDecl2   : ELLIPSIS
						  |   '''

def p_MethodDecl:
    ''' MethodDecl       : FUNC Receiver MethodName Signature
						  | FUNC Receiver MethodName Signature FunctionBody '''

def p_Receiver:
    ''' Receiver         : Parameters '''

def p_MethodName:
    ''' MethodName       : ID '''

def p_Block:
    ''' Block : LBRACE StatementList RBRACE '''

def p_StatementList:
    ''' StatementList : StatementList1 '''

def p_StatementList1:
    ''' StatementList1 : StatementList1 Statement SEMICOLON
						  |   '''

def p_Statement:
    ''' Statement   : Declaration
						  | LabeledStmt
						  | SimpleStmt
						  | GoStmt
						  | ReturnStmt
						  | BreakStmt
						  | ContinueStmt
						  | GotoStmt '''

def p_Statement:
    ''' Statement   : FallthroughStmt
						  | Block
						  | IfStmt
						  | SwitchStmt
						  | SelectStmt
						  | ForStmt
						  | DeferStmt '''

def p_Declaration:
    ''' Declaration : ConstDecl
						  | TypeDecl
						  | VarDecl '''

def p_LabeledStmt:
    ''' LabeledStmt : Label COLON Statement '''

def p_Label:
    ''' Label       : ID '''

def p_SimpleStmt:
    ''' SimpleStmt  : EmptyStmt
						  | ExpressionStmt
						  | SendStmt
						  | IncDecStmt
						  | Assignment
						  | ShortVarDecl '''

def p_EmptyStmt:
    ''' EmptyStmt   : '''

def p_ExpressionStmt:
    ''' ExpressionStmt : Expression '''

def p_SendStmt:
    ''' SendStmt : Channel ARROW Expression '''

def p_Channel:
    ''' Channel  : Expression '''

def p_IncDecStmt:
    ''' IncDecStmt : Expression IncDecStmt_1 '''

def p_IncDecStmt_1:
    ''' IncDecStmt_1 : INC
						  | DEC '''

def p_Assignment:
    ''' Assignment : ExpressionList assign_op ExpressionList '''

def p_assign_op:
    ''' assign_op : assign_op_1 ASSIGN '''

def p_assign_op_1:
    ''' assign_op_1 : add_op
						  | mul_op
						  |   '''

def p_ShortVarDecl:
    ''' ShortVarDecl : IdentifierList DEFINE ExpressionList '''

def p_GoStmt:
    ''' GoStmt : GO Expression '''

def p_ReturnStmt:
    ''' ReturnStmt : RETURN ReturnStmt_1 '''

def p_ReturnStmt_1:
    ''' ReturnStmt_1 : ExpressionList
						  |   '''

def p_BreakStmt:
    ''' BreakStmt : BREAK BreakStmt_1 '''

def p_BreakStmt_1:
    ''' BreakStmt_1 : Label
						  |   '''

def p_ContinueStmt:
    ''' ContinueStmt : CONTINUE ContinueStmt_1 '''

def p_ContinueStmt_1:
    ''' ContinueStmt_1 : Label
						  |   '''

def p_GotoStmt:
    ''' GotoStmt : GOTO Label '''

def p_FallthroughStmt:
    ''' FallthroughStmt : FALLTHROUGH '''

def p_IfStmt:
    ''' IfStmt : IF IfStmt_1 Expression Block IfStmt_2 '''

def p_IfStmt_1:
    ''' IfStmt_1 : SimpleStmt SEMICOLON
						  |   '''

def p_IfStmt_2:
    ''' IfStmt_2 : ELSE IfStmt_2_1
						  |   '''

def p_IfStmt_2_1:
    ''' IfStmt_2_1 : IfStmt
						  | Block '''

def p_SwitchStmt:
    ''' SwitchStmt : ExprSwitchStmt
						  | TypeSwitchStmt '''

def p_ExprSwitchStmt:
    ''' ExprSwitchStmt : SWITCH ExprSwitchStmt_1 ExprSwitchStmt_2 LBRACE ExprSwitchStmt_3 RBRACE '''

def p_ExprSwitchStmt_1:
    ''' ExprSwitchStmt_1 : SimpleStmt SEMICOLON
						  |   '''

def p_ExprSwitchStmt_2:
    ''' ExprSwitchStmt_2 : Expression
						  |   '''

def p_ExprSwitchStmt_3:
    ''' ExprSwitchStmt_3 : ExprSwitchStmt_3 ExprCaseClause
						  |   '''

def p_ExprCaseClause:
    ''' ExprCaseClause : ExprSwitchCase COLON StatementList '''

def p_ExprSwitchCase:
    ''' ExprSwitchCase : CASE ExpressionList
						  | DEFAULT '''

def p_TypeSwitchStmt:
    ''' TypeSwitchStmt  : SWITCH TypeSwitchStmt_1 TypeSwitchGuard LBRACE TypeSwitchStmt_2 RBRACE '''

def p_TypeSwitchStmt_1:
    ''' TypeSwitchStmt_1 : SimpleStmt SEMICOLON
						  |   '''

def p_TypeSwitchStmt_2:
    ''' TypeSwitchStmt_2 : TypeSwitchStmt_2 TypeCaseClause
						  |   '''

def p_TypeSwitchGuard:
    ''' TypeSwitchGuard : TypeSwitchGuard_1 PrimaryExpr PERIOD LPAREN TYPE RPAREN '''

def p_TypeSwitchGuard_1:
    ''' TypeSwitchGuard_1 : ID DEFINE
						  |   '''

def p_TypeCaseClause:
    ''' TypeCaseClause  : TypeSwitchCase COLON StatementList '''

def p_TypeSwitchCase:
    ''' TypeSwitchCase  : CASE TypeList
						  | DEFAULT '''

def p_TypeList:
    ''' TypeList        : Type TypeList_1 '''

def p_TypeList_1:
    ''' TypeList_1 : TypeList_1 COMMA Type
						  |   '''

def p_SelectStmt:
    ''' SelectStmt : SELECT LBRACE SelectStmt_1 RBRACE '''

def p_SelectStmt_1:
    ''' SelectStmt_1 : SelectStmt_1 CommClause
						  |   '''

def p_CommClause:
    ''' CommClause : CommCase COLON StatementList '''

def p_CommCase:
    ''' CommCase   : CASE CommCase_1
						  | DEFAULT '''

def p_CommCase_1:
    ''' CommCase_1 : SendStmt
						  | RecvStmt '''

def p_RecvStmt:
    ''' RecvStmt   : RecvStmt_1 RecvExpr '''

def p_RecvStmt_1:
    ''' RecvStmt_1 : ExpressionList ASSIGN
						  | IdentifierList DEFINE
						  |   '''

def p_RecvExpr:
    ''' RecvExpr   : Expression '''

def p_ForStmt:
    ''' ForStmt : FOR ForStmt_1 Block '''

def p_ForStmt_1:
    ''' ForStmt_1 : Condition
						  | ForClause
						  | RangeClause
						  |   '''

def p_Condition:
    ''' Condition : Expression '''

def p_ForClause:
    ''' ForClause : ForClause_1 SEMICOLON ForClause_2 SEMICOLON ForClause_3 '''

def p_ForClause_1:
    ''' ForClause_1 : InitStmt
						  |   '''

def p_ForClause_2:
    ''' ForClause_2 : Condition
						  |   '''

def p_ForClause_3:
    ''' ForClause_3 : PostStmt
						  |   '''

def p_InitStmt:
    ''' InitStmt : SimpleStmt '''

def p_PostStmt:
    ''' PostStmt : SimpleStmt '''

def p_RangeClause:
    ''' RangeClause : RangeClause_1 RANGE Expression '''

def p_RangeClause_1:
    ''' RangeClause_1 : ExpressionList ASSIGN
						  | IdentifierList DEFINE
						  |   '''

def p_DeferStmt:
    ''' DeferStmt : DEFER Expression '''

def p_TopLevelDecl:
    ''' TopLevelDecl  : Declaration
						  | FunctionDecl
						  | MethodDecl '''
