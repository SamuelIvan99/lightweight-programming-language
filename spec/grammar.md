# Lexical Grammar

```
SIGNED_TYPE   : i64 | i32 | i16 | i8 | isize
UNSIGNED_TYPE : u64 | u32 | u16 | u8 | usize
FLOAT_TYPE    : f64 | f32
BOOL_TYPE     : bool
CHAR_TYPE     : char
STRING_TYPE   : str
ABYSS_TYPE    : abyss


type          : SIGNED_TYPE | UNSIGNED_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE | STRING_TYPE
return_type   : type | ABYSS_TYPE

INTEGRAL_VALUE : -?\d+
FLOAT_VALUE    : -?\d+(\.\d+)?
BOOL_VALUE     : true | false
CHAR_VALUE     : \'.\'
STRING_VALUE   : \"[^\"]*\"

value          : INTEGRAL_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE | STRING_VALUE

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

INSERTION   : <<
EXTRACTION  : >>
COMPARATOR  : == | != | < | > | <= | >=
ASSIGN      : =
END         : ;
LPAREN      : (
RPAREN      : )
LSBRACKET   : [
RSBRACKET   : ]
LBRACE      : {
RBRACE      : }
COMMENT     : #
COLON       : :
COMMA       : ,
```

# Syntactical Grammar

```
program : functions

var_name            : ID | array_name
array_name          : ID LSBRACKET arithmetic_layer RSBRACKET

functions           : function functions | Ɛ
function            : ID LPAREN formal_params RPAREN COLON return_type scope

formal_params       : var_name type multi_formal_params | Ɛ
multi_formal_params : COMMA var_name type multi_formal_params | Ɛ

function_call       : ID LPAREN actual_params RPAREN

actual_params       : expression multi_actual_params | Ɛ
multi_actual_params : COMMA expression multi_actual_params | Ɛ

# This is how scope is implemented, i don't know if this is how we should do it
scope               : LBRACE new_scope statements pop_scope RBRACE
new_scope           : Ɛ
pop_scope           : Ɛ

statements          : statement statements | Ɛ
statement           : expression END | declaration END | declaration_init END | assignment END | scope | while_statement | if_statement | END

while_statement     : WHILE LPAREN expression RPAREN scope
if_statement        : IF LPAREN expression RPAREN scope else_statement
else_statement      : ELSE scope | ELSE if_statement | Ɛ

declaration         : var_name COLON type
declaration_init    : var_name COLON type ASSIGN expression

assignment          : var_name ASSIGN expression


insertions          : var_name INSERTION expression multi_insertions | Ɛ
multi_insertions    : INSERTION expression multi_insertions | Ɛ

expression          : ID LSBRACKET arithmetic_layer RSBRACKET | expression AND comparison_layer | expression OR comparison_layer | comparison_layer
comparison_layer    : comparison_layer COMPARATOR arithmetic_layer | arithmetic_layer
artihmetic_layer    : artihmetic_layer PLUS term | artihmetic_layer MINUS term | term
term                : term MULTIPLICATION factor | term DIVISION factor | factor
factor              : value | var_name | LPAREN expression LPAREN | function_call
```
