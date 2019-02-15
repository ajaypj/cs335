SourceFile     		: PackageClause SEMICOLON ImportDeclList TopLevelDeclList
PackageClause  		: PACKAGE ID
ImportDeclList 		: |  ImportDeclList ImportDecl SEMICOLON |  ImportDecl SEMICOLON
ImportDecl     		: IMPORT LPAREN ImportSpecList RPAREN |  IMPORT ImportSpec
ImportSpecList 		: |  ImportSpecList ImportSpec SEMICOLON |  ImportSpec SEMICOLON
ImportSpec     		: ID ImportPath |  PERIOD ImportPath |  ImportPath
ImportPath     		: STRING
Block          		: LBRACE OPENB StatementList CLOSEB RBRACE
OPENB          		:
CLOSEB         		:
BrkBlk         		:
BrkBlkEnd      		:
StatementList  		: StatementList Statement SEMICOLON |  Statement SEMICOLON
Statement      		: DeferStmt|Declaration |  LabeledStmt |  SimpleStmt |  ReturnStmt |  BreakStmt |  ContinueStmt |  GotoStmt |  Block |  IfStmt |  SelectStmt |  ForStmt
SimpleStmt     		: EmptyStmt |  ExpressionStmt | IncDecStmt | ShortVarDecl | Assignment
Assignment     		: ExpressionList assign_op ExpressionList
EmptyStmt      		:
ExpressionStmt 		: Expression SEMICOLON | Expression
IncDecStmt     		: Expression INC |  Expression DEC
ShortVarDecl   		: IdentifierList DEFINE ExpressionList
VarDecl        		: VAR VarSpec
VarSpec        		: IdentifierList Type |  IdentifierList Type assign_op ExpressionList |  IdentifierList assign_op ExpressionList
Declaration    		: TypeDecl |  VarDecl
FunctionDecl   		: FUNC ID OPENB Signature CLOSEB |  FUNC ID OPENB Signature Block CLOSEB
Signature      		: Parameters |  Parameters Result
Result         		: LPAREN TypeList RPAREN |  Type
Parameters     		: LPAREN RPAREN |  LPAREN ParameterList  RPAREN |  LPAREN ParameterList COMMA RPAREN
ParameterList  		: ParameterDecl |  ParameterList COMMA ParameterDecl
ParameterDecl  		: IdentifierList Type
TypeList       		: TypeList COMMA Type |  Type
IdentifierList 		: ID |  IdentifierList COMMA ID
MethodDecl     		: FUNC Receiver ID Signature
Receiver       		: Parameters
TopLevelDeclList  : TopLevelDeclList TopLevelDecl SEMICOLON |  TopLevelDecl SEMICOLON
Type           		: LiteralType |  ID | VARTYPE
SliceType      		: LBRACK RBRACK Type
TopLevelDecl   		: Declaration |  FunctionDecl |  MethodDecl
LabeledStmt    		: ID COLON Statement
ReturnStmt     		: RETURN |  RETURN ExpressionList
BreakStmt      		: BREAK |  BREAK ID
ContinueStmt   		: CONTINUE |  CONTINUE ID
IfStmt         		: IF OPENB Expression Block CLOSEB |  IF OPENB SimpleStmt SEMICOLON Expression Block CLOSEB |  IF OPENB Expression Block ELSE Block CLOSEB |  IF OPENB Expression Block ELSE IfStmt CLOSEB |  IF OPENB SimpleStmt SEMICOLON Expression Block ELSE IfStmt CLOSEB |  IF OPENB SimpleStmt SEMICOLON Expression Block ELSE Block CLOSEB
EmptyExpr      		:
Empty          		:
ForStmt_1 		    : Condition | ForClause | RangeClause |
Condition 		    : Expression
ForClause 		    : ForClause_1 SEMICOLON ForClause_2 SEMICOLON ForClause_3
ForClause_1 		  : SimpleStmt
ForClause_2 		  : Condition |
ForClause_3 		  : SimpleStmt
RangeClause 		  : RangeClause_1 RANGE Expression
RangeClause_1 		: ExpressionList ASSIGN | IdentifierList DEFINE |
GotoStmt       		: GOTO Label
SelectStmt     		: SELECT LBRACE  RBRACE | SELECT LBRACE CommClause RBRACE
CommClause     		: CommCase COLON StatementList
CommCase       		: CASE SendStmt | DEFAULT | CASE RecvStmt
RecvStmt       		: ExpressionList ASSIGN Expression | Expression | IdentifierList DEFINE Expression
SendStmt 		      : Channel ARROW Expression
Channel  		      : Expression
Label       		  : ID
TypeDecl       		: TYPE TypeSpec
TypeSpec       		: ID Type
MapType        		: MAP LBRACK Type RBRACK Type
StructType     		: STRUCT LBRACE FieldDeclList RBRACE |  STRUCT SEMICOLON FieldDeclList RBRACE |  STRUCT LBRACE RBRACE |  STRUCT SEMICOLON RBRACE
FieldDeclList  		: FieldDecl SEMICOLON |  FieldDeclList FieldDecl SEMICOLON
FieldDecl      		: IdentifierList Type STRING |  IdentifierList Type
PointerType    		: MUL Type
ArrayType      		: LBRACK Expression RBRACK Type
Operand        		: Literal |  ID |  LPAREN Expression RPAREN
Literal        		: BasicLit |  CompositeLit | FunctionLit
FunctionLit         : FUNC Signature Block
BasicLit       		: INT |  FLOAT |  STRING | IMAG
CompositeLit   		: LiteralType LiteralValue
LiteralType    		: StructType |  ArrayType |  PointerType |  LBRACK ELLIPSIS RBRACK Operand |  SliceType |  MapType | ID | InterfaceType
LiteralValue   		: LBRACE RBRACE |  SEMICOLON RBRACE |  LBRACE ElementList RBRACE |  SEMICOLON ElementList RBRACE |  LBRACE ElementList COMMA RBRACE |  SEMICOLON ElementList COMMA RBRACE | ChannelType
ChannelType         : CHAN Type | CHAN ARROW Type | ARROW CHAN Type
ElementList    		: KeyedElement |  ElementList COMMA KeyedElement
KeyedElement   		: Element |  Key COLON Element
Key            		: Expression |  LiteralValue
Element        		: Expression |  LiteralValue
Expression     		:  Expression1 |  UnaryExpr assign_op Expression
Expression1    		:  Expression2 |  Expression1 LOR Expression2
Expression2    		:  Expression3 |  Expression2 LAND Expression3
Expression3    		:  Expression4 |  Expression3 rel_op Expression4
Expression4    		:  Expression5 |  Expression4 add_op Expression5
Expression5    		:  UnaryExpr |  Expression5 mul_op UnaryExpr
UnaryExpr      		:  PrimaryExpr |  unary_op UnaryExpr
rel_op         		:  EQL |  NEQ |  LSS |  LEQ |  GTR |  GEQ
add_op         		:  ADD |  SUB |  OR |  XOR
mul_op         		:  MUL |  QUO |  REM |  SHL |  SHR |  AND |  AND_NOT
unary_op       		:  ADD |  SUB |  NOT |  XOR |  MUL |  AND |  ARROW
assign_op      		: ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | QUO_ASSIGN | REM_ASSIGN | AND_ASSIGN | OR_ASSIGN | XOR_ASSIGN | SHL_ASSIGN | SHR_ASSIGN | AND_NOT_ASSIGN
PrimaryExpr    		: Operand |  PrimaryExpr Selector |  PrimaryExpr Index |  PrimaryExpr Slice |  PrimaryExpr TypeAssertion |  PrimaryExpr Arguments |  ID StructLiteral
StructLiteral  		: LBRACE KeyValList RBRACE
KeyValList     		: |  Expression COLON Expression |  Expression COLON Expression COMMA KeyValList
Selector       		: PERIOD ID
Index          		: LBRACK Expression RBRACK
Slice          		: LBRACK COLON RBRACK |  LBRACK COLON Expression RBRACK |  LBRACK Expression COLON RBRACK |  LBRACK Expression COLON Expression RBRACK |  LBRACK COLON Expression COLON Expression RBRACK |  LBRACK Expression COLON Expression COLON Expression RBRACK
TypeAssertion  		: PERIOD LPAREN Type RPAREN
Arguments      		: LPAREN RPAREN |  LPAREN ExpressionList RPAREN |  LPAREN ExpressionList ELLIPSIS RPAREN
ExpressionList  	: Expression |  ExpressionList COMMA Expression
