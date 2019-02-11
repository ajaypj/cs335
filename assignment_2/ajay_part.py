def p_Type:
    ''' Type : TypeName | TypeLit | LPAREN Type LPAREN '''
def p_TypeName:
    ''' TypeName : ID |  QualifiedIdent '''
def p_TypeLit:
    ''' TypeLit : ArrayType | StructType | PointerType | FunctionType | InterfaceType | SliceType | MapType | ChannelType '''
def p_QualifiedIdent:
    ''' QualifiedIdent = PackageName PERIOD ID '''
def p_PackageName:
    ''' PackageName = ID '''
def p_ArrayType:
    ''' ArrayType   = LBRACK ArrayLength RBRACK ElementType '''
def p_ArrayLength:
    ''' ArrayLength = Expression '''
def p_ElementType:
    ''' ElementType = Type '''
def p_StructType:
    ''' StructType    : STRUCT LBRACE FieldDecl_1 RBRACE '''
def p_FieldDecl_1:
    ''' FieldDecl_1 :  | FieldDecl_1 FieldDecl SEMICOLON '''
def p_FieldDecl:
    ''' FieldDecl     : LPAREN IdentifierList Type | EmbeddedField RPAREN LBRACK Tag RBRACK '''
def p_EmbeddedField:
    ''' EmbeddedField : LBRACK MUL RBRACK TypeName '''
def p_Tag:
    ''' Tag           : STRING '''
def p_IdentifierList:
    ''' IdentifierList : ID identifierlist_1 '''
def p_identifierlist_1:
    ''' identifierlist_1 :  | identifierlist_1 COMMA ID '''
def p_ElementType:
    ''' ElementType : Type '''
def p_PointerType:
    ''' PointerType : MUL BaseType '''
def p_BaseType:
    ''' BaseType    : Type '''
def p_FunctionType:
    ''' FunctionType   : FUNC Signature '''
def p_Signature:
    ''' Signature      : Parameters Result_1 '''
def p_Result_1:
    ''' Result_1 : | Result '''
def p_Result:
    ''' Result         : Parameters | Type '''
def p_Parameters:
    ''' Parameters     : LPAREN Parameters_1 LPAREN '''
def p_FunctionType_Parameters_Comma_1:
    ''' FunctionType_Parameters_Comma_1 : | COMMA '''
def p_Parameters_1:
    ''' Parameters_1 : | ParameterList FunctionType_Parameters_Comma_1 '''
def p_ParameterList:
    ''' ParameterList  : ParameterDecl ParameterList_1 '''
def p_ParameterList_1:
    ''' ParameterList_1 : | ParameterList_1 COMMA ParameterDecl '''
def p_ParameterDecl:
    ''' ParameterDecl  : ParameterDecl_1 ParameterDecl_2 Type '''
def p_ParameterDecl_1:
    ''' ParameterDecl_1 : | IdentifierList '''
def p_ParameterDecl_2:
    ''' ParameterDecl_2 : | ELLIPSIS '''
def p_InterfaceType:
    ''' InterfaceType      : INTERFACE LBRACE InterfaceType_1 RBRACE '''
def p_InterfaceType_1:
    ''' InterfaceType_1 : | InterfaceType_1 MethodSpec SEMICOLON '''
def p_MethodSpec:
    ''' MethodSpec         : MethodName Signature | InterfaceTypeName '''
def p_MethodName:
    ''' MethodName         : identifier '''
def p_InterfaceTypeName:
    ''' InterfaceTypeName  : TypeName '''
def p_SliceType:
    ''' SliceType : LBRACK RBRACK ElementType '''
def p_MapType:
    ''' MapType     : MAP LBRACK KeyType RBRACK ElementType '''
def p_KeyType:
    ''' KeyType     : Type '''
def p_ChannelType:
    ''' ChannelType : ChannelType_1 ElementType '''
def p_ChannelType_1:
    ''' ChannelType_1 : CHAN | CHAN ARROW | ARROW CHAN '''
