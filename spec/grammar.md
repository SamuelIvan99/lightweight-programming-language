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

WHILE      : LBRACE conditions RBRACE LCURLYBRACE statements RCURLYBRACE
conditions : term COMPARATOR conditions | term
term       : ID | primitive
COMPARATOR : == | != | < | > | <= | >=

I think i messed up here, right now it would accept:
x <= y != z for example -> how to decide what does it mean..
Q: Do we want keywords like AND or OR ?
------------------------
Other approach:

CONDITIONS : regex
maybe this:  \w+\s*(==|!=|<|>|<=|>=)\s*\w+

-------------------------
New , corrected and improved while grammar:

WHILE      : LBRACE conditions RBRACE LCURLYBRACE statements RCURLYBRACE
conditions : term | term COMPARATOR term | OPERATOR conditions
                            START                   END
term       : ID | primitive
COMPARATOR : == | != | < | > | <= | >=

x<5 AND y>10 OR z==1
-------------------------
WHILE      : LBRACE conditions logical_operation RBRACE LCURLYBRACE statements RCURLYBRACE
conditions : single_condition | multiple_condition
single_condition   : term
multiple_condition : term COMPARATOR multiple_condition
logical_operation  : LOGICAL multiple_condition logical_operation | Ɛ
LOGICAL            : AND | OR




--------------------------- PRIME SUSPECT

WHILE              : LBRACE conditions RBRACE LCURLYBRACE statements RCURLYBRACE
conditions         : single_condition | multiple_condition
single_condition   : term
multiple_condition : term COMPARATOR term logical_operation
logical_operation  : LOGICAL term COMPARATOR term logical_operation | Ɛ
LOGICAL            : AND | OR
term               : ID | primitive
COMPARATOR         : == | != | < | > | <= | >=

-------------------------- IMPLEMENT THIS


<!-- For me: The way statementS is declared, makes it so that you dont need to write END at
any of the other statement(s). This includes all the childs, so dont have to explicitly say
END at the end of declaration or var_assignment -->
```
