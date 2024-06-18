# Array Declaration and Assignment

```
array_declaration       : DECLARE ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type

array_declaration_init  : DECLARE ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type ASSIGN array_init
                        | DECLARE ID LSBRACKET RSBRACKET COLON type ASSIGN array_init

array_init              : LBRACE value multi_array_init RBRACE
                        | STRING_VALUE

multi_array_init        : COMMA value multi_array_init
                        | Ɛ

array_assignment        : ID LSBRACKET arithmetic_layer RSBRACKET ASSIGN expression
```
