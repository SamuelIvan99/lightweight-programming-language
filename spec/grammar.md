ITYPE = i64|i32|i16|i8|isize
UTYPE = u64|u32|u16|u8|usize
FTYPE = f64|f32
BTYPE = bool
CTYPE = char
TYPE  = ITYPE|UTYPE|FTYPE|BTYPE|CYPET

IPRIM  = -?\d+
FPRIM  = -?\d+(\.\d+)?
BPRIM  = true|false
CPRIM  = "."
PRIM   = IPRIM|UPRIM|FPRIM|BPRIM|CRIMP

ID = [a-zA-Z_][a-zA-Z0-9_\-]*

ASS    = =
END    = ;
SPACES = \s+
BLANK  = SPACES|ε

DECLARE = TYPE SPACES ID BLANK ASS BLANK PRIM

Stat = Stat ; Stat
Stat = DECLARE|ε