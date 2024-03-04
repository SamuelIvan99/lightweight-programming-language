# Data Types

## Integer types

### Signed

| DataType | BitSize |
| -------- | ------- |
| i8       | 8       |
| i16      | 16      |
| i32      | 32      |
| i64      | 64      |
| iSize    | arch\*  |

### Unsigned

| DataType | BitSize |
| -------- | ------- |
| u8       | 8       |
| u16      | 16      |
| u32      | 32      |
| u64      | 64      |
| uSize    | arch\*  |

\* Types depend on the architecture of the computer program is running on. 64 bits if on a 64-bit architecture and 32 bits if on a 32-bit architecture.

## Floating-Point Types

| DataType | BitSize |
| -------- | ------- |
| f32      | 32      |
| f64      | 64      |

## Boolean Type

Boolean type has two possible values: `true` and `false`

| DataType | BitSize |
| -------- | ------- |
| bool     | 8       |

## Character Type

| DataType | BitSize |
| -------- | ------- |
| char     | 8/32    |

## Compound Types

Compound types can group multiple values into one type.

### Array Type

Every element of an array must have the same type. Arrays have a fixed length.

We write the values in an array as a comma-separated list inside square brackets.
