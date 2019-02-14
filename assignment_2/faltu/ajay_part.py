def p_Type(p):
    ''' Type : TypeName | TypeLit | LPAREN Type LPAREN '''
def p_TypeName(p):
    ''' TypeName : ID |  QualifiedIdent '''
def p_TypeLit(p):
    ''' TypeLit : ArrayType | StructType | PointerType | FunctionType | InterfaceType | SliceType | MapType | ChannelType '''
def p_QualifiedIdent(p):
    ''' QualifiedIdent = PackageName PERIOD ID '''
def p_PackageName(p):
    ''' PackageName = ID '''
def p_ArrayType(p):
    ''' ArrayType   = LBRACK ArrayLength RBRACK ElementType '''
def p_ArrayLength(p):
    ''' ArrayLength = Expression '''
def p_ElementType(p):
    ''' ElementType = Type '''
def p_StructType(p):
    ''' StructType    : STRUCT LBRACE FieldDecl_1 RBRACE '''
def p_FieldDecl_1(p):
    ''' FieldDecl_1 :  | FieldDecl_1 FieldDecl SEMICOLON '''
def p_FieldDecl(p):
    ''' FieldDecl     : LPAREN IdentifierList Type | EmbeddedField RPAREN LBRACK Tag RBRACK '''
def p_EmbeddedField(p):
    ''' EmbeddedField : LBRACK MUL RBRACK TypeName '''
def p_Tag(p):
    ''' Tag           : STRING '''
def p_IdentifierList(p):
    ''' IdentifierList : ID identifierlist_1 '''
def p_identifierlist_1(p):
    ''' identifierlist_1 :  | identifierlist_1 COMMA ID '''
def p_ElementType(p):
    ''' ElementType : Type '''
def p_PointerType(p):
    ''' PointerType : MUL BaseType '''
def p_BaseType(p):
    ''' BaseType    : Type '''
def p_FunctionType(p):
    ''' FunctionType   : FUNC Signature '''
def p_Signature(p):
    ''' Signature      : Parameters Result_1 '''
def p_Result_1(p):
    ''' Result_1 : | Result '''
def p_Result(p):
    ''' Result         : Parameters | Type '''
def p_Parameters(p):
    ''' Parameters     : LPAREN Parameters_1 LPAREN '''
def p_FunctionType_Parameters_Comma_1(p):
    ''' FunctionType_Parameters_Comma_1 : | COMMA '''
def p_Parameters_1(p):
    ''' Parameters_1 : | ParameterList FunctionType_Parameters_Comma_1 '''
def p_ParameterList(p):
    ''' ParameterList  : ParameterDecl ParameterList_1 '''
def p_ParameterList_1(p):
    ''' ParameterList_1 : | ParameterList_1 COMMA ParameterDecl '''
def p_ParameterDecl(p):
    ''' ParameterDecl  : ParameterDecl_1 ParameterDecl_2 Type '''
def p_ParameterDecl_1(p):
    ''' ParameterDecl_1 : | IdentifierList '''
def p_ParameterDecl_2(p):
    ''' ParameterDecl_2 : | ELLIPSIS '''
def p_InterfaceType(p):
    ''' InterfaceType      : INTERFACE LBRACE InterfaceType_1 RBRACE '''
def p_InterfaceType_1(p):
    ''' InterfaceType_1 : | InterfaceType_1 MethodSpec SEMICOLON '''
def p_MethodSpec(p):
    ''' MethodSpec         : MethodName Signature | InterfaceTypeName '''
def p_MethodName(p):
    ''' MethodName         : identifier '''
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
    ''' ChannelType_1 : CHAN | CHAN ARROW | ARROW CHAN '''
