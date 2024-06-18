# For Statement

```
statements : statement statements
           | Ɛ

statement  : expression END
           | scalar_declaration END
           | array_declaration END
           | scalar_declaration_init END
           | array_declaration_init END
           | scalar_assignment END
           | array_assignment END
           | scope
           | while_statement
           | for_statement
           | if_statement
           | return_statement END
           | insertion_statement END
           | END


for_statement   : FOR LPAREN for_init END for_condition END for_increment RPAREN scope

for_init        : scalar_declaration_init
                | scalar_assignment
                | array_declaration_init
                | array_assignment
                | expression
                | Ɛ

for_condition   : expression
                | Ɛ

for_increment   : scalar_assignment
                | array_assignment
                | expression
                | Ɛ
 
 
if_statement    : IF LPAREN expression RPAREN scope else_statement
 
else_statement  : ELSE scope
                | ELSE if_statement
                | Ɛ


while_statement : WHILE LPAREN expression RPAREN scope
```
