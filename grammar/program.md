# Lexical Grammar

```
SIGNED_TYPE   : \bi64\b | \bi32\b | \bi16\b | \bi8\b | \bisize\b
UNSIGNED_TYPE : \bu64\b | \bu32\b | \bu16\b | \bu8\b | \busize\b
FLOAT_TYPE    : \bf64\b | \bf32\b
BOOL_TYPE     : \bbool\b
CHAR_TYPE     : \bchar\b
STRING_TYPE   : \bstr\b
ABYSS_TYPE    : \babyss\b

type          : SIGNED_TYPE | UNSIGNED_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE | STRING_TYPE | ABYSS_TYPE

INTEGRAL_VALUE : -?\b\d+(?!\.)\b
FLOAT_VALUE    : -?\b\d+(\.\d+)?\b
BOOL_VALUE     : \btrue\b | \bfalse\b
CHAR_VALUE     : \'.\'
STRING_VALUE   : \"[^\"]*\"
SYSTEM_VALUE   : <[^\"]*>

value          : INTEGRAL_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE | STRING_VALUE

WHILE   : \bwhile\b
FOR     : \bfor\b
IF      : \bif\b
ELSE    : \belse\b
DECLARE : \blet\b
RETURN  : \breturn\b

INCLUDE : \binclude\b
USE     : \buse\b

AND            : \&\&
OR             : \|\|
MINUS          : \-
PLUS           : \+
DIVISION       : \/
MULTIPLICATION : \*

ID : \b[a-zA-Z_][a-zA-Z0-9_\-]*\b

INSERTION   : <<
EXTRACTION  : >>
COMPARATOR  : == | != | < | > | <= | >=
ASSIGN      : =
END         : ;
LPAREN      : \(
RPAREN      : \)
LSBRACKET   : \[
RSBRACKET   : \]
LBRACE      : \{
RBRACE      : \}
COLON       : \:
COMMA       : \,

COMMENT     : //
```

# Syntactical Grammar

```
program : globals


globals : global globals
        | Ɛ

global  : function
        | include
        | scalar_declaration_init END


include : USEC STRING_VALUE
        | USE STRING_VALUE


scope   : LBRACE statements RBRACE
```

-- "ID LSBRACKET arithmetic_layer RSBRACKET" is for indexing an array as in "x[i + 1];"
-- "ID LSBRACKET INTEGRAL_VALUE RSBRACKET" is for declaring an array "let x[100]:i16;"
