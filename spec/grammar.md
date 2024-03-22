# Grammar

```
# Lexical Grammar
SIGNED_TYPE   : i64 | i32 | i16 | i8 | isize
UNSIGNED_TYPE : u64 | u32 | u16 | u8 | usize
FLOAT_TYPE    : f64 | f32
BOOL_TYPE     : bool
CHAR_TYPE     : char

type          : SIGNED_TYPE | UNSIGNED_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE

INTEGRAL_VALUE : -?\d+
FLOAT_VALUE    : -?\d+(\.\d+)?
BOOL_VALUE     : true | false
CHAR_VALUE     : \'.\'

value          : INTEGRAL_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE

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


# Syntactical Grammar
program : statements

statements       : statement statements | Ɛ
statement        : expression_statement | declaration | declaration_init | assignment | while_statement | if_statement | END

declaration      : type ID END
declaration_init : type ID ASSIGN expression END

assignment       : ID ASSIGN expression END

while_statement : WHILE LBRACE expression RBRACE LCURCLYBRACE statements RCURLYBRACE
if_statement    : IF LBRACE expression RBRACE LCURLYBRACE statements RCURLYBRACE else_statement
else_statement  : ELSE LCURLYBRACE statements RCURLYBRACE | ELSE if_statement | Ɛ

expression_statement  : expression END
expression            : expression AND comparison_layer | expression OR comparison_layer | comparison_layer
comparison_layer      : comparison_layer COMPARATOR arithmetic_layer | arithmetic_layer
artihmetic_layer      : artihmetic_layer PLUS term | artihmetic_layer MINUS term | term
term                  : term MULTIPLICATION factor | term DIVISION factor | factor
factor                : value | ID | LBRACE expression RBRACE
