Empty = -- epsilon
Digit = "0" .. "9"
Lower = "a" .. "z"
Upper = "A" .. "Z"
Alpha = Lower | Upper
AlphaNum = Alpha | Digit

IType = "i64" | "i32" | "i16" | "i8" | "isize"
UType = "u64" | "u32" | "u16" | "u8" | "usize"
Type = IType | UType | "char"

Declare = Type "" Var "" "=" "" Val

Var = VarFirst VarRest*
VarFirst = Alpha | "_"
VarRest = AlphaNum | "_" | "-"

Val = Digit+

Start = Declare ";"
