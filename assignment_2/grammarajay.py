Type : TypeName | TypeLit | LPAREN Type LPAREN
TypeName : ID |  QualifiedIdent
TypeLit : ArrayType | StructType | PointerType | FunctionType | InterfaceType | SliceType | MapType | ChannelType
QualifiedIdent = PackageName PERIOD ID
PackageName = ID
ArrayType   = LBRACK ArrayLength RBRACK ElementType
ArrayLength = Expression
ElementType = Type
StructType    : STRUCT LBRACE FieldDecl_1 RBRACE
FieldDecl_1 :  | FieldDecl_1 FieldDecl SEMICOLON
FieldDecl     : LPAREN IdentifierList Type | EmbeddedField RPAREN LBRACK Tag RBRACK
EmbeddedField : LBRACK MUL RBRACK TypeName
Tag           : STRING
IdentifierList : ID identifierlist_1
identifierlist_1 :  | identifierlist_1 COMMA ID
ElementType : Type
PointerType : MUL BaseType
BaseType    : Type
FunctionType   : FUNC Signature
Signature      : Parameters Result_1
Result_1 : | Result
Result         : Parameters | Type
Parameters     : LPAREN Parameters_1 LPAREN
FunctionType_Parameters_Comma_1 : | COMMA
Parameters_1 : | ParameterList FunctionType_Parameters_Comma_1
ParameterList  : ParameterDecl ParameterList_1
ParameterList_1 : | ParameterList_1 COMMA ParameterDecl
ParameterDecl  : ParameterDecl_1 ParameterDecl_2 Type
ParameterDecl_1 : | IdentifierList
ParameterDecl_2 : | ELLIPSIS
InterfaceType      : INTERFACE LBRACE InterfaceType_1 RBRACE
InterfaceType_1 : | InterfaceType_1 MethodSpec SEMICOLON
MethodSpec         : MethodName Signature | InterfaceTypeName
MethodName         : identifier
InterfaceTypeName  : TypeName
SliceType : LBRACK RBRACK ElementType
MapType     : MAP LBRACK KeyType RBRACK ElementType
KeyType     : Type
ChannelType : ChannelType_1 ElementType
ChannelType_1 : CHAN | CHAN ARROW | ARROW CHAN
