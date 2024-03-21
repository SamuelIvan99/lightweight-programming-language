from sly import Lexer, Parser
import os

class BasedLexer(Lexer):
    tokens = { INTEGRAL_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE,
               INTEGRAL_VALUE, FLOAT_VALUE, BOOL_VALUE, CHAR_VALUE, ID,
               ASSIGN, END, LBRACE, RBRACE, LCURLYBRACE, RCURLYBRACE,
               COMPARATOR, LOGICAL_OPERATOR, WHILE_NAME, IF_NAME, ELSE_NAME,
               AND, OR, MINUS, PLUS, DIVISION, MULTIPLICATION }

    INTEGRAL_TYPE   = r"i64|i32|i16|i8|isize|u64|u32|u16|u8|usize"
    FLOAT_TYPE    = r"f64|f32"
    BOOL_TYPE     = r"bool"
    CHAR_TYPE     = r"char"

    FLOAT_VALUE    = r"-?\d+\.\d+"
    INTEGRAL_VALUE = r"-?\d+"
    BOOL_VALUE     = r"true|false"
    CHAR_VALUE     = r"\'.\'"

    # LOGICAL_OPERATOR = r"AND|OR|NEGATION"
    LOGICAL_OPERATOR = r"AND|OR"

    WHILE_NAME = r"while"
    IF_NAME    = r"if"
    ELSE_NAME  = r"else"

    AND            = r"\&\&"
    OR             = r"\|\|"
    MINUS          = r"\-"
    PLUS           = r"\+"
    DIVISION       = r"\/"
    MULTIPLICATION = r"\*"

    ID = r"[a-zA-Z_][a-zA-Z0-9_\-]*"

    COMPARATOR  = r"==|!=|<=|>=|<|>"
    ASSIGN      = r"="
    END         = r";"
    LBRACE      = r"\("
    RBRACE      = r"\)"
    LCURLYBRACE = r"\{"
    RCURLYBRACE = r"\}"

    literals = {}

    ignore = " \t"

    @_(r"\n+")
    def ignore_newline(self, t):
        pass

    ignore_comment = r"#.*"

class BasedParser(Parser):
    tokens = BasedLexer.tokens
    debugfile = "dist/parser.out"
    
    # precedence = (
    #     ("left", COMPARATOR),
    #     ("left", LOGICAL_OPERATOR),
    #     ("left", PLUS, MINUS),
    #     ("left", DIVISION, MULTIPLICATION),
    # )
    # Example -> go through the operation order in your head
    # 3 + 4 AND x * z >= 10
    
    # highest (done first) to lowest(done last):
    #  - MULTIPLICATION/DIVISION
    #  - PLUS/MINUS
    #  - LOGICAL_OPERATOR
    #  - COMPARATOR
    
    @_("statements")
    def program(self, p):
        return f"{p.statements}"

    @_("statement END statements")
    def statements(self, p):
        return f"    {p.statement}{p.END}\n{p.statements}"

    @_("")
    def statements(self, p):
        return ""
    
    @_("var_declaration")
    def statement(self, p):
        return p.var_declaration
    
    @_("var_assignment")
    def statement(self, p):
        return p.var_assignment
    
    # @_("WHILE")
    # def statement(self,p):
    #     return p.WHILE
    
    # @_("IF")
    # def statement(self,p):
    #     return p.IF
    
    # @_("ELSE")
    # def statement(self,p):
    #     return p.ELSE
    
    @_("")
    def statement(self, p):
        return ""

    @_("type ID initializer")
    def var_declaration(self, p):
        return f"{p.type} {p.ID} {p.initializer}"

    @_("ASSIGN value")
    def initializer(self, p):
        return f"{p.ASSIGN} {p.value}"
    
    @_("")
    def initializer(self, p):
        return ""

    @_("INTEGRAL_TYPE")
    def type(self, p):
        if p.INTEGRAL_TYPE == "i64":
            type = "long long int"
        elif p.INTEGRAL_TYPE == "i32":
            type = "long int"
        elif p.INTEGRAL_TYPE == "i16":
            type = "int"
        elif p.INTEGRAL_TYPE == "i8":
            type = "char"
        elif p.INTEGRAL_TYPE == "isize": 
            type = "size_t" # I don't think size_t is signed
        elif p.INTEGRAL_TYPE == "u64":
            type = "unsigned long long int"
        elif p.INTEGRAL_TYPE == "u32":
            type = "unsigned long int"
        elif p.INTEGRAL_TYPE == "u16":
            type = "unsigned int"
        elif p.INTEGRAL_TYPE == "u8":
            type = "unsigned char"
        elif p.INTEGRAL_TYPE == "usize":
            type = "size_t"
        return type
        
    @_("FLOAT_TYPE")
    def type(self, p):
        if p.FLOAT_TYPE == "f64":
            type = "double"
        elif p.FLOAT_TYPE == "f32":
            type = "float"
        return type

    @_("BOOL_TYPE")
    def type(self, p):
        return "char"
    
    @_("CHAR_TYPE")
    def type(self, p):
        return "char"

    @_("INTEGRAL_VALUE")
    def value(self, p):
        return p.INTEGRAL_VALUE
    
    @_("FLOAT_VALUE")
    def value(self, p):
        return p.FLOAT.VALUE
    
    # Do we still want to have Bools this way?
    @_("BOOL_VALUE")
    def value(self, p):
        if p.BOOL_VALUE == "true":
            value = "0x01"
        elif p.BOOL_VALUE == "false":
            value = "0x00"
        return value
    
    @_("CHAR_VALUE")
    def value(self, p):
        return p.CHAR_VALUE

    @_("ID ASSIGN value")
    def var_assignment(self,p):
        return f"{p.ID}{p.ASSIGN}{p.value}"
    
    #  expressions begin here
    @_("expression AND comparison_layer")
    def expression(self, p):
        return f"{p.expression}{p.AND}{p.comparison_layer}"
    
    @_("expression OR comparison_layer")
    def expression(self, p):
        return f"{p.expression}{p.OR}{p.comparison_layer}"
    
    @_("comparison_layer")
    def expression(self, p):
        return f"{p.comparison_layer}"
    
    @_("comparison_layer COMPARATOR arithmetic_layer")
    def comparison_layer(self, p):
        return f"{p.comparison_layer}{p.COMPARATOR}{p.arithmetic_layer}"

    @_("arithmetic_layer")
    def comparison_layer(self, p):
        return f"{p.arithmetic_layer}"
    
    @_("arithmetic_layer PLUS term")
    def arithmetic_layer(self,p):
        return f"{p.arithmetic_layer}{p.PLUS}{p.term}"
    
    @_("arithmetic_layer MINUS term")
    def arithmetic_layer(self,p):
        return f"{p.arithmetic_layer}{p.MINUS}{p.term}"
    
    @_("arithmetic_layer")
    def arithmetic_layer(self, p):
        return f"{p.term}"
    
    # @_("expression logical_operator_or_comparator expression")
    # def expression(self,p):
    #     return f"{p.expression0}{p.logical_operator_or_comparator}{p.expression1}"
    
    # @_("LOGICAL_OPERATOR")
    # def logical_operator_or_comparator(self,p):
    #     if p.LOGICAL_OPERATOR == "AND":
    #         logical_operator = "&&"
    #     elif p.LOGICAL_OPERATOR == "OR":
    #         logical_operator = "||"
    #     elif p.LOGICAL_OPERATOR == "NOT":
    #         logical_operator = "!"
    #     return logical_operator
    
    # @_("COMPARATOR")
    # def logical_operator_or_comparator(self,p):
    #     return p.COMPARATOR
    
    @_("term MULTIPLICATION factor")
    def term(self,p):
        return f"{p.term}{p.MULTIPLICATION}{p.FACTOR}"
    
    @_("term DIVISION factor")
    def term(self,p):
        return f"{p.term}{p.DIVISION}{p.FACTOR}"
    
    @_("factor")
    def term(self,p):
        return p.factor
    
    @_("value")
    def factor(self,p):
        return p.value
    
    @_("ID")
    def factor(self,p):
        return p.ID
    
    @_("LBRACE expression RBRACE")
    def factor(self,p):
        return f"{p.LBRACE}{p.expression}{p.RBRACE}"
    
    #  expressions end here

    # @_("WHILE_NAME LBRACE expression RBRACE LCURLYBRACE statements RCURLYBRACE")
    # def WHILE(self,p):
    #     return f"{p.WHILE_NAME}{p.LBRACE}{p.expression}{p.RBRACE}{p.LCURLYBRACE}\n    {p.statements}    {p.RCURLYBRACE}"
    
    # @_("IF_NAME LBRACE expression RBRACE LCURLYBRACE statements RCURLYBRACE ELSE")
    # def IF(self,p):
    #     return f"{p.IF_NAME}{p.LBRACE}{p.expression}{p.RBRACE}{p.LCURLYBRACE}{p.statements}{p.RCURLYBRACE}{p.ELSE}"
    
    # @_("ELSE_NAME LCURLYBRACE statements RCURLYBRACE")
    # def ELSE(self,p):
    #     return f"{p.ELSE_NAME}{p.LCURLYBRACE}{p.statements}{p.RCURLYBRACE}"
    
    # @_("ELSE_NAME IF")
    # def ELSE(self,p):
    #     return f"{p.ELSE_NAME}{p.IF}"
    
    

def main():
# For transpiled C code
    if not os.path.exists("dist"):
        os.mkdir("dist")
    if os.path.exists("dist/out.c"):
        os.remove("dist/out.c")
    # For compiled machine code
    if not os.path.exists("bin"):
        os.mkdir("bin")

    lexer = BasedLexer()
    parser = BasedParser()

    with open("test.based") as based_file:
        program = based_file.read()
        tokens = lexer.tokenize(program)
        result = parser.parse(tokens)

    with open("dist/out.c", "a") as c_file:
        c_file.write(
f"""int main()
{{
{result}
    return 0;
}}
""")
    os.system("gcc dist/out.c -o bin/based")
if __name__ == '__main__':
    main()