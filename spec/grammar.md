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

program     : statements
statements  : statement END statements | Ɛ
statement   : declaration | Ɛ
declaration : type ID initializer
initializer : ASSIGN primitive | Ɛ

```