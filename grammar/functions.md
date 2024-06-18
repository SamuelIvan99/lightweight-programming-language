# Functions

```
functions           : function functions
                    | Ɛ

function            : ID LPAREN formal_params RPAREN COLON type scope

formal_params       : ID COLON type multi_formal_params
                    | ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params
                    | Ɛ

multi_formal_params : COMMA ID COLON type multi_formal_params
                    | COMMA ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params
                    | Ɛ

function_call       : ID LPAREN actual_params RPAREN

actual_params       : expression multi_actual_params
                    | Ɛ

multi_actual_params : COMMA expression multi_actual_params
                    | Ɛ

return_statement    : RETURN expression
```
