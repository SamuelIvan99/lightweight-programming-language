IType = i64|i32|i16|i8|isize
UType = u64|u32|u16|u8|usize
FType = f32|f64
BType = bool
CType = char
Type  = IType|UType|FType|BType|CType
Ass   = =
End   = ;
Space = \s
Blank = Space|ε

IPrim  = -?\d+
FPrim  = -?\d+(\.\d+)?
BPrim  = true|false
CPrim  = "."
Prim   = IPrim|UPrim|FPrim|BPrim|CPrim

Id = [a-zA-Z_][a-zA-Z0-9_\-]*

Declaration = Type Whitespace Id Ass Prim
