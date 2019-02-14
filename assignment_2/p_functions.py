keywords = ['break','default','func','interface','select','case','defer','go','map','struct',
            'chan','else','goto','package','switch','const','fallthrough','if','range','type',
            'continue','for','import','return','var']

n=0
def func(p,value):
    global n
    # value=str.split()
    # value=value[0]
    # print value
    if len(p)==2:
        if p[1] in keywords:
            n+=1
            p[1]=[n,p[1]]
            print "\t",p[1][0],"[label=\""+p[1][1]+"\"]"
        p[0]=p[1]
        return
    s="\t\t"
    key_no = 0
    for i in range(0,len(p)):
        # print p[i]
        if p[i] in keywords:
            key_no+=1
        if i==0:
            # Create a node corresponding to i=0
            n+=1
            p[i]=[n,value]
            print "\t",p[i][0],"[label=\""+p[i][1]+"\"]"
        else:
            if isinstance(p[i],list): # Non-terminal, make edge
                print "\t",p[i][0],'->',p[0][0]
                if i != len(p)-1:
                    s+=str(p[i][0])+"->"
                else:
                    s+=str(p[i][0])
            elif p[i] not in keywords: # Terminal, make node + edge
                n+=1
                p[i]=[n,p[i]]
                # print p[i][1][0]
                if isinstance(p[i][1],str) and (p[i][1][0]=='\"' or p[i][1][0]=='\''):
                    print "\t",p[i][0],"[label="+p[i][1]+"]"
                else:
                    print "\t",p[i][0],"[label=\""+p[i][1]+"\"]"
                print "\t",p[i][0],'->',p[0][0]
                if i != len(p)-1:
                    s+=str(p[i][0])+"->"
                else:
                    s+=str(p[i][0])

    if len(p)-key_no > 2:
        print "\t{\n\t\trank=same;\n" + s + "[style=invis]\n\t}"




def p_SourceFile(p):
    ''' SourceFile     		: PackageClause SEMICOLON ImportDeclList TopLevelDeclList '''
    func(p,"SourceFile")

def p_PackageClause(p):
    ''' PackageClause  		: PACKAGE ID '''
    func(p,"PackageClause")

def p_ImportDeclList(p):
    ''' ImportDeclList 		:
							|  ImportDeclList ImportDecl SEMICOLON
							|  ImportDecl SEMICOLON '''
    func(p,"ImportDeclList")

def p_ImportDecl(p):
    ''' ImportDecl     		: IMPORT LPAREN ImportSpecList RPAREN
							|  IMPORT ImportSpec '''
    func(p,"ImportDecl")

def p_ImportSpecList(p):
    ''' ImportSpecList 		:
							|  ImportSpecList ImportSpec SEMICOLON
							|  ImportSpec SEMICOLON '''
    func(p,"ImportSpecList")

def p_ImportSpec(p):
    ''' ImportSpec     		: ID ImportPath
							|  PERIOD ImportPath
							|  ImportPath '''
    func(p,"ImportSpec")

def p_ImportPath(p):
    ''' ImportPath     		: STRING '''
    func(p,"ImportPath")

def p_Block(p):
    ''' Block          		: LBRACE OPENB StatementList CLOSEB RBRACE '''
    func(p,"Block")

def p_OPENB(p):
    ''' OPENB          		: '''
    func(p,"OPENB")

def p_CLOSEB(p):
    ''' CLOSEB         		: '''
    func(p,"CLOSEB")

def p_BrkBlk(p):
    ''' BrkBlk         		: '''
    func(p,"BrkBlk")

def p_BrkBlkEnd(p):
    ''' BrkBlkEnd      		: '''
    func(p,"BrkBlkEnd")

def p_StatementList(p):
    ''' StatementList  		: StatementList Statement SEMICOLON
							|  Statement SEMICOLON '''
    func(p,"StatementList")

def p_Statement(p):
    ''' Statement      		: Declaration
							|  LabeledStmt
							|  SimpleStmt
							|  ReturnStmt
							|  BreakStmt
							|  ContinueStmt
							|  GotoStmt
							|  Block
							|  IfStmt
							|  SelectStmt
							|  ForStmt '''
    func(p,"Statement")

def p_SimpleStmt(p):
    ''' SimpleStmt     		: EmptyStmt
							|  ExpressionStmt
							| IncDecStmt
							| ShortVarDecl
							| Assignment '''
    func(p,"SimpleStmt")

def p_Assignment(p):
    ''' Assignment     		: ExpressionList assign_op ExpressionList '''
    func(p,"Assignment")

def p_EmptyStmt(p):
    ''' EmptyStmt      		: '''
    func(p,"EmptyStmt")

def p_ExpressionStmt(p):
    ''' ExpressionStmt 		: Expression '''
    func(p,"ExpressionStmt")

def p_IncDecStmt(p):
    ''' IncDecStmt     		: Expression INC
							|  Expression DEC '''
    func(p,"IncDecStmt")

def p_ShortVarDecl(p):
    ''' ShortVarDecl   		: IdentifierList ASSIGN ExpressionList '''
    func(p,"ShortVarDecl")

def p_VarDecl(p):
    ''' VarDecl        		: VAR VarSpec '''
    func(p,"VarDecl")

def p_VarSpec(p):
    ''' VarSpec        		: IdentifierList Type
							|  IdentifierList Type assign_op ExpressionList
							|  IdentifierList assign_op ExpressionList '''
    func(p,"VarSpec")

def p_Declaration(p):
    ''' Declaration    		: TypeDecl
							|  VarDecl '''
    func(p,"Declaration")

def p_FunctionDecl(p):
    ''' FunctionDecl   		: FUNC ID OPENB Signature CLOSEB
							|  FUNC ID OPENB Signature Block CLOSEB '''
    func(p,"FunctionDecl")

def p_Signature(p):
    ''' Signature      		: Parameters
							|  Parameters Result '''
    func(p,"Signature")

def p_Result(p):
    ''' Result         		: LPAREN TypeList RPAREN
							|  Type '''
    func(p,"Result")

def p_Parameters(p):
    ''' Parameters     		: LPAREN RPAREN
							|  LPAREN ParameterList  RPAREN
							|  LPAREN ParameterList COMMA RPAREN '''
    func(p,"Parameters")

def p_ParameterList(p):
    ''' ParameterList  		: ParameterDecl
							|  ParameterList COMMA ParameterDecl '''
    func(p,"ParameterList")

def p_ParameterDecl(p):
    ''' ParameterDecl  		: IdentifierList Type '''
    func(p,"ParameterDecl")

def p_TypeList(p):
    ''' TypeList       		: TypeList COMMA Type
							|  Type '''
    func(p,"TypeList")

def p_IdentifierList(p):
    ''' IdentifierList 		: ID
							|  IdentifierList COMMA ID '''
    func(p,"IdentifierList")

def p_MethodDecl(p):
    ''' MethodDecl     		: FUNC Receiver ID Signature '''
    func(p,"MethodDecl")

def p_Receiver(p):
    ''' Receiver       		: Parameters '''
    func(p,"Receiver")

def p_TopLevelDeclList(p):
    ''' TopLevelDeclList  : TopLevelDeclList TopLevelDecl SEMICOLON
							|  TopLevelDecl SEMICOLON '''
    func(p,"TopLevelDeclList")

def p_Type(p):
    ''' Type           		: LiteralType
							|  ID
							| VARTYPE '''
    func(p,"Type")

def p_SliceType(p):
    ''' SliceType      		: LBRACK RBRACK Type '''
    func(p,"SliceType")

def p_TopLevelDecl(p):
    ''' TopLevelDecl   		: Declaration
							|  FunctionDecl
							|  MethodDecl '''
    func(p,"TopLevelDecl")

def p_LabeledStmt(p):
    ''' LabeledStmt    		: ID COLON Statement '''
    func(p,"LabeledStmt")

def p_ReturnStmt(p):
    ''' ReturnStmt     		: RETURN
							|  RETURN ExpressionList '''
    func(p,"ReturnStmt")

def p_BreakStmt(p):
    ''' BreakStmt      		: BREAK
							|  BREAK ID '''
    func(p,"BreakStmt")

def p_ContinueStmt(p):
    ''' ContinueStmt   		: CONTINUE
							|  CONTINUE ID '''
    func(p,"ContinueStmt")

def p_IfStmt(p):
    ''' IfStmt         		: IF OPENB Expression Block CLOSEB
							|  IF OPENB SimpleStmt SEMICOLON Expression Block CLOSEB
							|  IF OPENB Expression Block ELSE Block CLOSEB
							|  IF OPENB Expression Block ELSE IfStmt CLOSEB
							|  IF OPENB SimpleStmt SEMICOLON Expression Block ELSE IfStmt CLOSEB
							|  IF OPENB SimpleStmt SEMICOLON Expression Block ELSE Block CLOSEB '''
    func(p,"IfStmt")

def p_EmptyExpr(p):
    ''' EmptyExpr      		: '''
    func(p,"EmptyExpr")

def p_Empty(p):
    ''' Empty          		: '''
    func(p,"Empty")

# def p_ForStmt(p):
#     ''' ForStmt        :   FOR OPENB SimpleStmt SEMICOLON BrkBlk ExpressionStmt SEMICOLON SimpleStmt Block BrkBlkEnd CLOSEB
# 					   |  FOR OPENB Expression BrkBlk Block BrkBlkEnd CLOSEB
# 					   |  FOR BrkBlk Block BrkBlkEnd
# 					   |  FOR OPENB SimpleStmt SEMICOLON BrkBlk EmptyExpr SEMICOLON SimpleStmt Block BrkBlkEnd CLOSEB
# 					   |  FOR OPENB EmptyStmt Empty BrkBlk Expression Empty EmptyStmt Block BrkBlkEnd CLOSEB '''
#     # print "ForStmt"

def p_ForStmt(p):
    ''' ForStmt : FOR ForStmt_1 Block '''
    func(p,"ForStmt")

def p_ForStmt_1(p):
    ''' ForStmt_1 		    : Condition
							| ForClause
							| RangeClause
							| '''
    func(p,"ForStmt_1")

def p_Condition(p):
    ''' Condition 		    : Expression '''
    func(p,"Condition")

def p_ForClause(p):
    ''' ForClause 		    : ForClause_1 SEMICOLON ForClause_2 SEMICOLON ForClause_3 '''
    func(p,"ForClause")

def p_ForClause_1(p):
    ''' ForClause_1 		  : SimpleStmt '''
    func(p,"ForClause_1")

def p_ForClause_2(p):
    ''' ForClause_2 		  : Condition
							| '''
    func(p,"ForClause_2")

def p_ForClause_3(p):
    ''' ForClause_3 		  : SimpleStmt '''
    func(p,"ForClause_3")

def p_RangeClause(p):
    ''' RangeClause 		  : RangeClause_1 RANGE Expression '''
    func(p,"RangeClause")

def p_RangeClause_1(p):
    ''' RangeClause_1 		: ExpressionList ASSIGN
							| IdentifierList DEFINE
							| '''
    func(p,"RangeClause_1")

def p_GotoStmt(p):
    ''' GotoStmt       		: GOTO Label '''
    func(p,"GotoStmt")

def p_SelectStmt(p):
    ''' SelectStmt     		: SELECT LBRACE  RBRACE
							| SELECT LBRACE CommClause RBRACE '''
    func(p,"SelectStmt")

def p_CommClause(p):
    ''' CommClause     		: CommCase COLON StatementList '''
    func(p,"CommClause")

def p_CommCase(p):
    ''' CommCase       		: CASE SendStmt
							| DEFAULT
							| CASE RecvStmt '''
    func(p,"CommCase")

def p_RecvStmt(p):
    ''' RecvStmt       		: ExpressionList ASSIGN Expression
							| Expression
							| IdentifierList DEFINE Expression '''
    func(p,"RecvStmt")

def p_SendStmt(p):
    ''' SendStmt 		      : Channel ARROW Expression '''
    func(p,"SendStmt")

def p_Channel(p):
    ''' Channel  		      : Expression '''
    func(p,"Channel")

def p_Label(p):
    ''' Label       		  : ID '''
    func(p,"Label")

def p_TypeDecl(p):
    ''' TypeDecl       		: TYPE TypeSpec '''
    func(p,"TypeDecl")

def p_TypeSpec(p):
    ''' TypeSpec       		: ID Type '''
    func(p,"TypeSpec")

def p_MapType(p):
    ''' MapType        		: MAP LBRACK Type RBRACK Type '''
    func(p,"MapType")

def p_StructType(p):
    ''' StructType     		: STRUCT LBRACE FieldDeclList RBRACE
							|  STRUCT SEMICOLON FieldDeclList RBRACE
							|  STRUCT LBRACE RBRACE
							|  STRUCT SEMICOLON RBRACE '''
    func(p,"StructType")

def p_FieldDeclList(p):
    ''' FieldDeclList  		: FieldDecl SEMICOLON
							|  FieldDeclList FieldDecl SEMICOLON '''
    func(p,"FieldDeclList")

def p_FieldDecl(p):
    ''' FieldDecl      		: IdentifierList Type STRING
							|  IdentifierList Type '''
    func(p,"FieldDecl")

def p_PointerType(p):
    ''' PointerType    		: MUL Type '''
    func(p,"PointerType")

def p_ArrayType(p):
    ''' ArrayType      		: LBRACK Expression RBRACK Type '''
    func(p,"ArrayType")

def p_Operand(p):
    ''' Operand        		: Literal
							|  ID
							|  LPAREN Expression RPAREN '''
    func(p,"Operand")

def p_Literal(p):
    ''' Literal        		: BasicLit
							|  CompositeLit '''
    func(p,"Literal")

def p_BasicLit(p):
    ''' BasicLit       		: INT
							|  FLOAT
							|  STRING
							| IMAG '''
    func(p,"BasicLit")

def p_CompositeLit(p):
    ''' CompositeLit   		: LiteralType LiteralValue '''
    func(p,"CompositeLit")

def p_LiteralType(p):
    ''' LiteralType    		: StructType
							|  ArrayType
							|  PointerType
							|  LBRACK ELLIPSIS RBRACK Operand
							|  SliceType
							|  MapType '''
    func(p,"LiteralType")

def p_LiteralValue(p):
    ''' LiteralValue   		: LBRACE RBRACE
							|  SEMICOLON RBRACE
							|  LBRACE ElementList RBRACE
							|  SEMICOLON ElementList RBRACE
							|  LBRACE ElementList COMMA RBRACE
							|  SEMICOLON ElementList COMMA RBRACE '''
    func(p,"LiteralValue")

def p_ElementList(p):
    ''' ElementList    		: KeyedElement
							|  ElementList COMMA KeyedElement '''
    func(p,"ElementList")

def p_KeyedElement(p):
    ''' KeyedElement   		: Element
							|  Key COLON Element '''
    func(p,"KeyedElement")

def p_Key(p):
    ''' Key            		: Expression
							|  LiteralValue '''
    func(p,"Key")

def p_Element(p):
    ''' Element        		: Expression
							|  LiteralValue '''
    func(p,"Element")

def p_Expression(p):
    ''' Expression     		:  Expression1
							|  UnaryExpr assign_op Expression '''
    func(p,"Expression")

def p_Expression1(p):
    ''' Expression1    		:  Expression2
							|  Expression1 LOR Expression2 '''
    func(p,"Expression1")

def p_Expression2(p):
    ''' Expression2    		:  Expression3
							|  Expression2 LAND Expression3 '''
    func(p,"Expression2")

def p_Expression3(p):
    ''' Expression3    		:  Expression4
							|  Expression3 rel_op Expression4 '''
    func(p,"Expression3")

def p_Expression4(p):
    ''' Expression4    		:  Expression5
							|  Expression4 add_op Expression5 '''
    func(p,"Expression4")

def p_mulExpr(p):
    ''' Expression5    		:  UnaryExpr
							|  Expression5 mul_op UnaryExpr '''
    func(p,"Expression5")

def p_UnaryExpr(p):
    ''' UnaryExpr      		:  PrimaryExpr
							|  unary_op UnaryExpr '''
    func(p,"UnaryExpr")

def p_rel_op(p):
    ''' rel_op         		:  EQL
							|  NEQ
							|  LSS
							|  LEQ
							|  GTR
							|  GEQ '''
    func(p,"rel_op")

def p_add_op(p):
    ''' add_op         		:  ADD
							|  SUB
							|  OR
							|  XOR '''
    func(p,"add_op")

def p_mul_op(p):
    ''' mul_op         		:  MUL
							|  QUO
							|  REM
							|  SHL
							|  SHR
							|  AND
							|  AND_NOT '''
    func(p,"mul_op")

def p_unary_op(p):
    ''' unary_op       		:  ADD
							|  SUB
							|  NOT
							|  XOR
							|  MUL
							|  AND
							|  ARROW '''
    func(p,"unary_op")

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
    func(p,"assign_op")

def p_PrimaryExpr(p):
    ''' PrimaryExpr    		: Operand
							|  PrimaryExpr Selector
							|  PrimaryExpr Index
							|  PrimaryExpr Slice
							|  PrimaryExpr TypeAssertion
							|  PrimaryExpr Arguments
							|  ID StructLiteral '''
    func(p,"PrimaryExpr")

def p_StructLiteral(p):
    ''' StructLiteral  		: LBRACE KeyValList RBRACE '''
    func(p,"StructLiteral")

def p_KeyValList(p):
    ''' KeyValList     		:
							|  Expression COLON Expression
							|  Expression COLON Expression COMMA KeyValList '''
    func(p,"KeyValList")

def p_Selector(p):
    ''' Selector       		: PERIOD ID '''
    func(p,"Selector")

def p_Index(p):
    ''' Index          		: LBRACK Expression RBRACK '''
    func(p,"Index")

def p_Slice(p):
    ''' Slice          		: LBRACK COLON RBRACK
							|  LBRACK COLON Expression RBRACK
							|  LBRACK Expression COLON RBRACK
							|  LBRACK Expression COLON Expression RBRACK
							|  LBRACK COLON Expression COLON Expression RBRACK
							|  LBRACK Expression COLON Expression COLON Expression RBRACK '''
    func(p,"Slice")

def p_TypeAssertion(p):
    ''' TypeAssertion  		: PERIOD LPAREN Type RPAREN '''
    func(p,"TypeAssertion")

def p_Arguments(p):
    ''' Arguments      		: LPAREN RPAREN
							|  LPAREN ExpressionList RPAREN
							|  LPAREN ExpressionList ELLIPSIS RPAREN '''
    func(p,"Arguments")

def p_ExpressionList(p):
    ''' ExpressionList  	: Expression
							|  ExpressionList COMMA Expression '''
    func(p,"ExpressionList")
