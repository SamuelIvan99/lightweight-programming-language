# Lexical Grammar
```
SIGNED_TYPE   : i64 | i32 | i16 | i8 | isize
UNSIGNED_TYPE : u64 | u32 | u16 | u8 | usize
FLOAT_TYPE    : f64 | f32
BOOL_TYPE     : bool
CHAR_TYPE     : char
ABYSS_TYPE    : abyss
STRING_TYPE   : str

type          : SIGNED_TYPE | UNSIGNED_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE | STRING_TYPE

INTEGRAL_VALUE : -?\d+
FLOAT_VALUE    : -?\d+(\.\d+)?
BOOL_VALUE     : true | false
CHAR_VALUE     : \'.\'
STRING_VALUE   : \"[^\"]*\"

value          : INTEGRAL_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE | STRING_VALUE

array_value    : ID LSBRACKET artihmetic_layer RSBRACKET

WHILE  : while
IF     : if
ELSE   : else

AND            : &&
OR             : ||
MINUS          : -
PLUS           : +
DIVISION       : /
MULTIPLICATION : *

ID : [a-zA-Z_][a-zA-Z0-9_\-]*

COMPARATOR  : == | != | < | > | <= | >=
ASSIGN      : =
END         : ;
LBRACE      : (
RBRACE      : )
LCURLYBRACE : {
RCURLYBRACE : }
COMMENT     : #
COLON       : :
COMMA       : ,
```

# Syntactical Grammar
```
program : functions

scope             : LBRACE statements RBRACE
functions         : function functions | Ɛ
function          : ID LBRACE params RBRACE COLON return_type scope
return_type       : type | ABYSS_TYPE
params            : param_declaration multi_params | Ɛ
multi_params      : COMMA param_declaration multi_params | Ɛ
param_declaration : type ID

function_call : ID LPAREN actual_params RPAREN
actual_params : expression multi_actual_params | Ɛ
multi_actual_params : COMMA expression multi_actual_params | Ɛ

statements       : statement statements | Ɛ
statement        : expression_statement | declaration | declaration_init | assignment | while_statement | if_statement | END

declaration      : type ID END | type ID LSBRACKET term RSBRACKET END
declaration_init : type ID ASSIGN expression END

assignment       : ID ASSIGN expression END | ID LSBRACKET term RSBRACKET ASSIGN expression END

while_statement : WHILE LBRACE expression RBRACE LCURCLYBRACE statements RCURLYBRACE
if_statement    : IF LBRACE expression RBRACE scope else_statement
else_statement  : ELSE scope | ELSE if_statement | Ɛ

expression_statement  : expression END
expression            : expression AND comparison_layer | expression OR comparison_layer | comparison_layer
comparison_layer      : comparison_layer COMPARATOR arithmetic_layer | arithmetic_layer
artihmetic_layer      : artihmetic_layer PLUS term | artihmetic_layer MINUS term | term
term                  : term MULTIPLICATION factor | term DIVISION factor | factor
factor                : value | array_value | ID | LPAREN expression LPAREN | function_call
```
