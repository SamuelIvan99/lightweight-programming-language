# Grammar

```

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

value          : INT_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE

// name of the variable, class, function
ID : [a-zA-Z_][a-zA-Z0-9_\-]* 

ASSIGN : =
END    : ;
LBRACE : (
RBRACE : )
LCURLYBRACE : {
RCURLYBRACE : }

COMPARATORS          : == | != | < | > | <= | >=
LOGICAL_OPERATORS    : AND | OR | NEGATION
logical_operators_or_comparators : LOGICAL_OPERATORS | COMPARATORS
expression : expression + term | expression - term
expression : expression LOGICAL_OPERATORS_OR_COMPARATORS expression
expression : term
term       : term * factor | term / factor | factor
factor     : value | ID | LBRACE expression RBRACE

program          : statements
statements       : statement END statements | Ɛ
statement        : declaration | declaration_with_initialization | var_assignment | WHILE | Ɛ
declaration      : type ID
declaration_with_initialization : type ID ASSIGN value

var_assignment : ID ASSIGN value

expression
--------------------------- WHILE STATEMENT

WHILE              : WHILE_NAME LBRACE conditions RBRACE LCURLYBRACE statements RCURLYBRACE
conditions         : single_condition | multiple_condition
single_condition   : term
multiple_condition : term COMPARATOR term logical_operation
logical_operation  : LOGICAL_OPERATOR term COMPARATOR term logical_operation | Ɛ

WHILE_NAME         : while



<!-- These namings can be subject to change. If we change something, don't forget to change the implementation as well, so it represents the grammar correctly, to avoid confusion. (From looking at the grammar here, and looking at mismatching names in the implementation.) -->
--------------------------

--------------------- IF statement
if_statement : "if" LBRACE expression RBRACE LCURLYBRACE statements RCURLYBRACE else_statement?
else_statement : "else" LCURLYBRACE statements RCURLYBRACE | "else" if_statement

```
