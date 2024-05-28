# Lexical Grammar

```
SIGNED_TYPE   : i64 | i32 | i16 | i8 | isize
UNSIGNED_TYPE : u64 | u32 | u16 | u8 | usize
FLOAT_TYPE    : f64 | f32
BOOL_TYPE     : bool
CHAR_TYPE     : char
STRING_TYPE   : str
ABYSS_TYPE    : abyss

type          : SIGNED_TYPE | UNSIGNED_TYPE | FLOAT_TYPE | BOOL_TYPE | CHAR_TYPE | STRING_TYPE | ABYSS_TYPE

INTEGRAL_VALUE : -?\b\d+(?!\.)\b
FLOAT_VALUE    : -?\b\d+(\.\d+)?\b
BOOL_VALUE     : true | false
CHAR_VALUE     : \'.\'
STRING_VALUE   : \"[^\"]*\"

value          : INTEGRAL_VALUE | FLOAT_VALUE | BOOL_VALUE | CHAR_VALUE | STRING_VALUE

WHILE   : while
FOR     : for
IF      : if
ELSE    : else
DECLARE : let
RETURN  : return

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
COMMENT     : //
COLON       : :
COMMA       : ,
```

# Syntactical Grammar

```
program                 : globals

globals                 : global globals | Ɛ
global                  : function | include | scalar_declaration_init END

include                 : USEC STRING_VALUE | USE STRING_VALUE

functions               : function functions | Ɛ
function                : ID LPAREN formal_params RPAREN COLON type scope

formal_params           : ID COLON type multi_formal_params | ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params  | ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params | Ɛ
multi_formal_params     : COMMA ID COLON type multi_formal_params | COMMA ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params  | Ɛ

function_call           : ID LPAREN actual_params RPAREN

actual_params           : expression multi_actual_params | Ɛ
multi_actual_params     : COMMA expression multi_actual_params | Ɛ

scope                   : LBRACE statements RBRACE

statements              : statement statements | Ɛ
statement               : expression END | scalar_declaration END | array_declaration END | scalar_declaration_init END | array_declaration_init END | scalar_assignment END | array_assignment END | scope | while_statement | for_statement | if_statement | return_statement END | insertion_statement END | END

for_init                : scalar_declaration_init | scalar_assignment | array_declaration_init | array_assignment | expression | Ɛ
for_condition           : expression | Ɛ
for_increment           : scalar_assignment | array_assignment | expression | Ɛ

for_statement           : FOR LPAREN for_init END for_condition END for_increment RPAREN scope
while_statement         : WHILE LPAREN expression RPAREN scope
if_statement            : IF LPAREN expression RPAREN scope else_statement
else_statement          : ELSE scope | ELSE if_statement | Ɛ

return_statement        : RETURN expression

scalar_declaration      : DECLARE ID COLON type
array_declaration       : DECLARE ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type

scalar_declaration_init : DECLARE ID COLON type ASSIGN expression
array_declaration_init  : DECLARE ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type ASSIGN array_init | DECLARE ID LSBRACKET RSBRACKET COLON type ASSIGN array_init
array_init              : LBRACE value multi_array_init RBRACE | STRING_VALUE
multi_array_init        : COMMA value multi_array_init | Ɛ

scalar_assignment       : ID ASSIGN expression
array_assignment        : ID LSBRACKET arithmetic_layer RSBRACKET ASSIGN expression

insertion_statement     : expression INSERTION expression multi_insertion
multi_insertion         : INSERTION expression multi_insertion | Ɛ

expression              : ID LSBRACKET arithmetic_layer RSBRACKET | expression AND comparison_layer | expression OR comparison_layer | comparison_layer
comparison_layer        : comparison_layer COMPARATOR arithmetic_layer | arithmetic_layer
arithmetic_layer        : artihmetic_layer PLUS term | artihmetic_layer MINUS term | term
term                    : term MULTIPLICATION factor | term DIVISION factor | factor
factor                  : value | ID | ID LSBRACKET arithmetic_layer RSBRACKET | LPAREN expression LPAREN | function_call
```

-- "ID LSBRACKET arithmetic_layer RSBRACKET" is for indexing an array as in "x[i + 1];"
-- "ID LSBRACKET INTEGRAL_VALUE RSBRACKET" is for declaring an array "let x[100]:i16;"
