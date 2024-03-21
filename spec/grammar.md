# Grammar

```

INTEGRAL_TYPE : i64 | i32 | i16 | i8 | isize | u64 | u32 | u16 | u8 | usize
FLOAT_TYPE    : f64 | f32
BOOL_TYPE     : bool
CHAR_TYPE     : char
type          : INTEGRAL_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE

INTEGRAL_VALUE       : -?\d+
FLOAT_VALUE     : -?\d+(\.\d+)?
BOOL_VALUE      : true | false
CHAR_VALUE      : \".*\"
value           : INTEGRAL_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE

<!-- name of the variable, class, function -->
ID : [a-zA-Z_][a-zA-Z0-9_\-]*

ASSIGN : =
END    : ;
LBRACE : (
RBRACE : )
LCURLYBRACE : {
RCURLYBRACE : }

MINUS          : -
PLUS           : +
DIVISION       : /
MULTIPLICATION : *

COMPARATOR          : == | != | < | > | <= | >=
LOGICAL_OPERATOR    : AND | OR | NEGATION

logical_operator_or_comparator : LOGICAL_OPERATOR | COMPARATOR

expression            : expression AND comparison_layer | expression OR comparison_layer | comparison_layer
comparison_layer      : comparison_layer COMPARATOR arithmetic_layer | arithmetic_layer
arithmetic_layer      : arithmetic_layer + term | arithmetic_layer - term | term
term                  : term * factor | term / factor | factor
factor                : value | ID | LBRACE expression RBRACE


program     : statements
statements  : statement END statements | Ɛ
statement   : var_declaration | var_assignment | WHILE | IF | ELSE | Ɛ
var_declaration : type ID initializer
initializer : ASSIGN value | Ɛ

var_assignment : ID ASSIGN value

WHILE              : WHILE_NAME LBRACE expression RBRACE LCURLYBRACE statements RCURLYBRACE

<!-- How to implement this optinality "?" -->
if_statement : IF_NAME LBRACE expression RBRACE LCURLYBRACE statements RCURLYBRACE else_statement?

else_statement : ELSE_NAME LCURLYBRACE statements RCURLYBRACE | ELSE_NAME if_statement

WHILE_NAME = while
IF_NAME = if
ELSE_NAME = else
```
