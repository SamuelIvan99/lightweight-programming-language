# Grammar

```

INT_TYPE      : i64 | i32 | i16 | i8 | isize
UNSIGNED_TYPE : u64 | u32 | u16 | u8 | usize
FLOAT_TYPE    : f64 | f32
BOOL_TYPE     : bool
CHAR_TYPE     : char
type          : INT_TYPE | UNSIGNED_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE

INT       : -?\d+
FLOAT     : -?\d+(\.\d+)?
BOOL      : true | false
CHAR      : \".*\"
primitive : INT | FLOAT | BOOL | CHAR

ID : [a-zA-Z_][a-zA-Z0-9_\-]*

ASSIGN : =
END    : ;
LBRACE : (
RBRACE : )
LCURLYBRACE : {
RCURLYBRACE : }

program     : statements
statements  : statement END statements | Ɛ
statement   : declaration | var_assignment | WHILE | Ɛ
declaration : type ID initializer
initializer : ASSIGN primitive | Ɛ

------------------------

var_assignment : ID ASSIGN primitive

--------------------------- WHILE STATEMENT

WHILE              : WHILE_NAME LBRACE conditions RBRACE LCURLYBRACE statements RCURLYBRACE
conditions         : single_condition | multiple_condition
single_condition   : term
multiple_condition : term COMPARATOR term logical_operation
logical_operation  : LOGICAL_OPERATOR term COMPARATOR term logical_operation | Ɛ
LOGICAL_OPERATOR   : AND | OR
WHILE_NAME         : while
term               : ID | primitive
COMPARATOR         : == | != | < | > | <= | >=

<!-- These namings can be subject to change. If we change something, don't forget to change the implementation as well, so it represents the grammar correctly, to avoid confusion. (From looking at the grammar here, and looking at mismatching names in the implementation.) -->
--------------------------

```
