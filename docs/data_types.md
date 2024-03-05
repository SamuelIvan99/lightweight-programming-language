# Data Types

Every value is of a certain data type, which tells us what kind of data is being specified so we know how to work with that data. We define two data type subsets: scalar and compound.

We have to defiune the types of all variables at compile time.

## Scalar Types

Scalar type represents a single value. We have four primary scalar types: integers, floating-point numbers, Booleans, and characters.

### Integer types

An integer is a number without a fractional component.

Signed and unsigned refer to whether it’s possible for the number to be negative—in other words, whether the number needs to have a sign with it (signed) or whether it will only ever be positive and can therefore be represented without a sign (unsigned).

#### Signed

| DataType | BitSize |
| -------- | ------- |
| i8       | 8       |
| i16      | 16      |
| i32      | 32      |
| i64      | 64      |
| iSize    | arch\*  |

#### Unsigned

| DataType | BitSize |
| -------- | ------- |
| u8       | 8       |
| u16      | 16      |
| u32      | 32      |
| u64      | 64      |
| uSize    | arch\*  |

\* Types depend on the architecture of the computer program is running on. 64 bits if on a 64-bit architecture and 32 bits if on a 32-bit architecture.

### Floating-Point Types

Floating-point numbers are numbers with decimal points. All floating-point types are signed.

| DataType | BitSize |
| -------- | ------- |
| f32      | 32      |
| f64      | 64      |

### Boolean Type

Boolean type has two possible values: `true` and `false`

| DataType | BitSize |
| -------- | ------- |
| bool     | 8       |

### Character Type

`char` type is the language’s most primitive alphabetic type.

| DataType | BitSize |
| -------- | ------- |
| char     | 8/32    |

## Compound Types

Compound types can group multiple values into one type.

### Array Type

Every element of an array must have the same type. Arrays have a fixed length.

We write the values in an array as a comma-separated list inside square brackets.
