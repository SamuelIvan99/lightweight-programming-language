from sly import Lexer, Parser
import os
import subprocess

class Bindings:
    def __init__(self):
        self._stack = []

    def bind(self, name, type, value):
        self._stack.insert(0, (name, type, value))

    def lookup(self, name_to_find):
        for name, type in self._stack:
            if name == name_to_find:
                return name
        return None

    def enter(self):
        self._stack.insert(0, "#")

    def exit(self):
        variable = self._stack.pop(0)
        while len(self.stack) > 0 and variable != "#":
            variable = self._stack.pop(0)

bindings = Bindings()

class BasedLexer(Lexer):
    tokens = { SIGNED_TYPE, UNSIGNED_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE,
               INTEGRAL_VALUE, FLOAT_VALUE, BOOL_VALUE, CHAR_VALUE, ID, ASSIGN,
               END, COMPARATOR, LBRACE, RBRACE, LPAREN, RPAREN,
               WHILE, FOR, MINUS, PLUS, MULTIPLICATION, DIVISION, AND, OR, IF, ELSE,
               COLON, COMMA, ABYSS_TYPE }

    SIGNED_TYPE   = r"i64|i32|i16|i8|isize"
    UNSIGNED_TYPE = r"u64|u32|u16|u8|usize"
    FLOAT_TYPE    = r"f64|f32"
    BOOL_TYPE     = r"bool"
    CHAR_TYPE     = r"char"
    ABYSS_TYPE    = r"abyss"

    FLOAT_VALUE    = r"-?\d+\.\d+"
    INTEGRAL_VALUE = r"-?\d+"
    BOOL_VALUE     = r"true|false"
    CHAR_VALUE     = r"\'.\'"

    WHILE = r"while"
    FOR   = r"for"
    IF    = r"if"
    ELSE  = r"else"

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
    LPAREN      = r"\("
    RPAREN      = r"\)"
    LBRACE      = r"\{"
    RBRACE      = r"\}"
    COLON       = r"\:"
    COMMA       = r"\,"

    literals = {}

    ignore = " \t"

    @_(r"\n+")
    def ignore_newline(self, t):
        pass

    ignore_comment = r"#.*"

class BasedParser(Parser):
    tokens = BasedLexer.tokens
    debugfile = "dist/debug"

    @_("functions")
    def program(self, p):
        return f"{p.functions}"

    #region functions
    @_("function functions")
    def functions(self, p):
        return f"{p.function}{p.functions}"
    @_("")
    def functions(self, p):
        return ""
    @_("ID LPAREN params RPAREN COLON return_type scope")
    def function(self, p):
        return f"{p.return_type} {p.ID}{p.LPAREN}{p.params}{p.RPAREN}{p.scope}"
    @_("type")
    def return_type(self, p):
        type_name, mapping, min, max, default = p.type
        return f"{mapping}"
    @_("ABYSS_TYPE")
    def return_type(self, p):
        return f"{p.ABYSS_TYPE}"
    @_("param_declaration multi_params")
    def params(self, p):
        return f"{p.param_declaration}{p.multi_params}"
    @_("")
    def params(self, p):
        return ""
    @_("COMMA param_declaration multi_params")
    def multi_params(self, p):
        return f"{p.COMMA}{p.param_declaration}{p.multi_params}"
    @_("")
    def multi_params(self, p):
        return ""
    @_("type ID")
    def param_declaration(self, p):
        type_name, mapping, min, max, default = p.type
        return f"{mapping} {p.ID}"
    @_("ID LPAREN actual_params RPAREN")
    def function_call(self, p):
        return f"{p.ID}{p.LPAREN}{p.actual_params}{p.RPAREN}"
    @_("expression multi_actual_params")
    def actual_params(self, p):
        return f"{p.expression}{p.multi_actual_params}"
    @_("")
    def actual_params(self, p):
        return ""
    @_("COMMA expression multi_actual_params")
    def multi_actual_params(self, p):
        return f"{p.COMMA}{p.expression}{p.multi_actual_params}"
    @_("")
    def multi_actual_params(self, p):
        return ""
    #endregion

    #region statements
    @_("statement statements")
    def statements(self, p):
        return f"{p.statement}{p.statements}"
    @_("")
    def statements(self, p):
        return f""
    @_("expression_statement")
    def statement(self, p):
        return f"{p.expression_statement}"
    @_("declaration")
    def statement(self, p):
        return f"{p.declaration}"
    @_("declaration_init")
    def statement(self, p):
        return f"{p.declaration_init}"
    @_("scope")
    def statement(self,p):
        return p.scope
    @_("while_statement")
    def statement(self, p):
        return f"{p.while_statement}"
    @_("for_statement")
    def statement(self, p):
        return f"{p.for_statement}"
    @_("if_statement")
    def statement(self, p):
        return f"{p.if_statement}"
    @_("END")
    def statement(self, p):
        return f"{p.END}"
    #endregion


    @_("type ID END")
    def declaration(self, p):
        type_name, mapping, min, max, default = p.type
        # bindings.bind(p.ID, type_name, default)
        return f"{mapping} {p.ID}{p.END}"
    @_("type ID ASSIGN expression END")
    def declaration_init(self, p):
        var_name = p.ID
        type_name, mapping, min, max, default = p.type
        value = p.expression
        # if value < min or value > max:
        #     print(f"ERROR: overflow detected in {type_name}{var_name}{p.ASSIGN}{value}, assigned value must be in range [{min},{max}]")
        #     exit(1)
        # bindings.bind(var_name, type_name, value)            
        return f"{mapping} {p.ID}{p.ASSIGN}{value}{p.END}"

    #region expressions
    @_("expression END")
    def expression_statement(self, p):
        return f"{p.expression}{p.END}"
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
    def arithmetic_layer(self, p):
        return f"{p.arithmetic_layer}{p.PLUS}{p.term}"
    @_("arithmetic_layer MINUS term")
    def arithmetic_layer(self, p):
        return f"{p.arithmetic_layer}{p.MINUS}{p.term}"
    @_("term")
    def arithmetic_layer(self, p):
        return f"{p.term}"
    @_("term MULTIPLICATION factor")
    def term(self,p):
        return f"{p.term}{p.MULTIPLICATION}{p.factor}"    
    @_("term DIVISION factor")
    def term(self,p):
        return f"{p.term}{p.DIVISION}{p.factor}" 
    @_("factor")
    def term(self,p):
        return f"{p.factor}"
    @_("function_call")
    def factor(self, p):
        return f"{p.function_call}"
    @_("LPAREN expression RPAREN")
    def factor(self,p):
        return f"{p.LPAREN}{p.expression}{p.RPAREN}"
    @_("value")
    def factor(self,p):
        return f"{p.value}"
    @_("ID")
    def factor(self,p):
        return f"{p.ID}"
    #endregion

 
    @_("SIGNED_TYPE")
    def type(self, p):
        types_mapping = {
            "i64": {"mapping": "long long int", "min": -(2**63 - 1), "max": 2**63 - 1, "default": 0},
            "i32": {"mapping": "long int", "min": -(2**31 - 1), "max": 2**31 - 1, "default": 0},
            "i16": {"mapping": "int", "min": -(2**15 - 1), "max": 2**15 - 1, "default": 0},
            "i8": {"mapping": "char", "min": -(2**7 - 1), "max": 2**7 - 1, "default": 0}
            # "isize": "size_t"
        }
        return (
            p.SIGNED_TYPE,
            types_mapping[p.SIGNED_TYPE]["mapping"],
            types_mapping[p.SIGNED_TYPE]["min"],
            types_mapping[p.SIGNED_TYPE]["max"],
            types_mapping[p.SIGNED_TYPE]["default"]
        )
    @_("UNSIGNED_TYPE")
    def type(self, p):
        types_mapping = {
            "u64": {"mapping": "unsigned long long int", "min": 2**64 - 1, "max": 2**64 - 1, "default": 0},
            "u32": {"mapping": "unsigned long int", "min": 2**32 - 1, "max": 2**63 - 1, "default": 0},
            "u16": {"mapping": "unsigned int", "min": 2**16 - 1, "max": 2**16 - 1, "default": 0},
            "u8": {"mapping": "unsigned char", "min": 2**7 - 1, "max": 2**7 - 1, "default": 0},
            # "usize": "size_t"
        }
        return (
            p.UNSIGNED_TYPE,
            types_mapping[p.UNSIGNED_TYPE]["mapping"],
            types_mapping[p.UNSIGNED_TYPE]["min"],
            types_mapping[p.UNSIGNED_TYPE]["max"],
            types_mapping[p.UNSIGNED_TYPE]["default"]
        )
    @_("FLOAT_TYPE")
    def type(self, p):
        types_mapping = {
            "f64": {"mapping": "double", "min": 2.22507385 * 10**(-308), "max": 1.7976931 * 10**308, "default": 0},
            "f32": {"mapping": "float", "min": 1.175494351 * 10**(-38), "max": 3.4028235 * 10**38, "default": 0}
        }
        return (
            p.FLOAT_TYPE,
            types_mapping[p.FLOAT_TYPE]["mapping"],
            types_mapping[p.FLOAT_TYPE]["min"],
            types_mapping[p.FLOAT_TYPE]["max"],
            types_mapping[p.FLOAT_TYPE]["default"]
        )
    @_("CHAR_TYPE")
    def type(self, p):
        return (
            p.CHAR_TYPE,
            "char",
            "a",
            "Z",
            "0"
        )
    @_("BOOL_TYPE")
    def type(self, p):
        return (
            p.BOOL_TYPE,
            "char",
            "a",
            "Z",
            "0"
        )


    @_("INTEGRAL_VALUE")
    def value(self, p):
        return int(p.INTEGRAL_VALUE)
    @_("FLOAT_VALUE")
    def value(self, p):
        return float(p.FLOAT_VALUE)
    @_("BOOL_VALUE")
    def value(self, p):
        if p.BOOL_VALUE == "true":
            value = 1
        elif p.BOOL_VALUE == "false":
            value = 0
        return value
    @_("CHAR_VALUE")
    def value(self, p):
        return p.CHAR_VALUE


    @_("LBRACE statements RBRACE")
    def scope(self,p):
        return f"{p.LBRACE}{p.statements}{p.RBRACE}"

    @_("WHILE LPAREN expression RPAREN scope")
    def while_statement(self,p):
        return f"{p.WHILE}{p.LPAREN}{p.expression}{p.RPAREN}{p.scope}"

    @_("FOR LPAREN declaration_init expression END expression RPAREN scope")
    def for_statement(self,p):
        return f"{p.FOR}{p.LPAREN}{p.declaration_init}{p.expression0}{p.END}{p.expression1}{p.RPAREN}{p.scope}"

    @_("IF LPAREN expression RPAREN scope else_statement")
    def if_statement(self,p):
        return f"{p.IF}{p.LPAREN}{p.expression}{p.RPAREN}{p.scope}{p.else_statement}"
    @_("ELSE scope")
    def else_statement(self,p):
        return f"{p.ELSE}{p.scope}" 
    @_("ELSE if_statement")
    def else_statement(self,p):
        return f"{p.ELSE} {p.if_statement}"
    @_("")
    def else_statement(self,p):
        return f""

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
        # c_file.write(f"int main(){{{result}return 0;}}")
        c_file.write(f"{result}")
    subprocess.run(["clang-format", "-i", "dist/out.c"])
    os.system("gcc dist/out.c -o bin/based")
if __name__ == '__main__':
    main()
