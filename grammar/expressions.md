# Expressions

```
expression       : ID LSBRACKET arithmetic_layer RSBRACKET
                 | expression AND comparison_layer
                 | expression OR comparison_layer
                 | comparison_layer

comparison_layer : comparison_layer COMPARATOR arithmetic_layer
                 | arithmetic_layer

arithmetic_layer : artihmetic_layer PLUS term
                 | artihmetic_layer MINUS term
                 | term

term             : term MULTIPLICATION factor
                 | term DIVISION factor
                 | factor

factor           : value
                 | ID
                 | ID LSBRACKET arithmetic_layer RSBRACKET
                 | LPAREN expression LPAREN
                 | function_call
```
