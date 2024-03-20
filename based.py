from variables import VariableStack

from sly import Lexer, Parser
import os

class BasedLexer(Lexer):
    tokens = { SIGNED_TYPE, UNSIGNED_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE,
               INTEGRAL_VALUE, FLOAT_VALUE, BOOL_VALUE, CHAR_VALUE, ID,
               ASSIGN, END, COMPARATOR, LBRACE, RBRACE,
               LCURLYBRACE, RCURLYBRACE, LOGICAL_OPERATOR, WHILE_NAME}

    SIGNED_TYPE   = r"i64|i32|i16|i8|isize"
    UNSIGNED_TYPE = r"u64|u32|u16|u8|usize"
    FLOAT_TYPE    = r"f64|f32"
    BOOL_TYPE     = r"bool"
    CHAR_TYPE     = r"char"

    FLOAT_VALUE    = r"-?\d+\.\d+"
    INTEGRAL_VALUE = r"-?\d+"
    BOOL_VALUE     = r"true|false"
    CHAR_VALUE     = r"\'.\'"
    LOGICAL_OPERATOR = r"AND|OR"

    WHILE_NAME = r"while"

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

bindings = VariableStack()

class BasedParser(Parser):
    tokens = BasedLexer.tokens

    @_("statements")
    def program(self, p):
        return f"{p.statements}"

    @_("statement END statements")
    def statements(self, p):
        return f"    {p.statement}{p.END}\n{p.statements}"

    @_("")
    def statements(self, p):
        return ""

    @_("declaration")
    def statement(self, p):
        return p.declaration

    @_("declaration_with_initialization")
    def statement(self, p):
        return p.declaration_with_initialization
    
    @_("var_assignment")
    def statement(self, p):
        return p.var_assignment
    
    @_("WHILE")
    def statement(self,p):
        return p.WHILE
    
    @_("")
    def statement(self, p):
        return ""

    @_("type ID")
    def declaration(self, p):
        type_name, type_mapping = p.type
        bindings.bind(p.ID, type, type_mapping["default"])
        return f"{type_mapping['mapping']} {p.ID}"

    @_("type ID ASSIGN value")
    def declaration_with_initialization(self, p):
        name = p.ID
        type_name, type_mapping = p.type
        value = p.value
        if value < type_mapping["min"] or value > type_mapping["max"]:
            print(f"ERROR: overflow detected in {type_name} {name} {p.ASSIGN} {value}, assigned value must be in range [{type_mapping['min']},{type_mapping['max']}]")
            exit(1)
        bindings.bind(name, type_name, value)
        return f"{type_mapping['mapping']} {name} {p.ASSIGN} {value}"

    @_("SIGNED_TYPE")
    def type(self, p):
        types_mapping = {
            "i64": {"mapping": "long long int", "min": -(2**63 - 1), "max": 2**63 - 1, "default": 0},
            "i32": {"mapping": "long int", "min": -(2**31 - 1), "max": 2**31 - 1, "default": 0},
            "i16": {"mapping": "int", "min": -(2**15 - 1), "max": 2**15 - 1, "default": 0},
            "i8": {"mapping": "char", "min": -(2**7 - 1), "max": 2**7 - 1, "default": 0}
            # "isize": "size_t"
        }
        return (p.SIGNED_TYPE, types_mapping[p.SIGNED_TYPE])

    @_("UNSIGNED_TYPE")
    def type(self, p):
        types_mapping = {
            "u64": {"mapping": "unsigned long long int", "min": 2**64 - 1, "max": 2**64 - 1, "default": 0},
            "u32": {"mapping": "unsigned long int", "min": 2**32 - 1, "max": 2**63 - 1, "default": 0},
            "u16": {"mapping": "unsigned int", "min": 2**16 - 1, "max": 2**16 - 1, "default": 0},
            "u8": {"mapping": "unsigned char", "min": 2**7 - 1, "max": 2**7 - 1, "default": 0},
            # "usize": "size_t"
        }
        return (p.UNSIGNED_TYPE, types_mapping[p.UNSIGNED_TYPE])

    @_("FLOAT_TYPE")
    def type(self, p):
        types_mapping = {
            "f64": "double",
            "f32": "float"
        }
        return (p.FLOAT_TYPE, types_mapping[p.FLOAT_TYPE])

    @_("CHAR_TYPE")
    def type(self, p):
        return (p.CHAR_TYPE, "char")

    @_("BOOL_TYPE")
    def type(self, p):
        return (p.BOOL_TYPE, "char")

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

    @_("ID ASSIGN value")
    def var_assignment(self, p):
        name = p.ID
        value = p.value
        vairable = bindings.lookup(name)
        if value < variable["min"] or value > variable["max"]:
            print(f"overflow detected in {name} {p.ASSIGN} {value}, assigned value must be in range [{type_mapping['min']},{type_mapping['max']}]")
            exit(1)
        return f"{type_mapping['mapping']} {name} {p.ASSIGN} {value}"
        return f"{p.ID}{p.ASSIGN}{p.value}"

    @_("WHILE_NAME LBRACE conditions RBRACE LCURLYBRACE statements RCURLYBRACE")
    def WHILE(self,p):
        return f"{p.WHILE_NAME}{p.LBRACE}{p.conditions}{p.RBRACE}{p.LCURLYBRACE}\n    {p.statements}    {p.RCURLYBRACE}"
    
    @_("single_condition")
    def conditions(self,p):
        return p.single_condition
    
    @_("multiple_condition")
    def conditions(self,p):
        return p.multiple_condition
    
    @_("term")
    def single_condition(self,p):
        return p.term

    @_("term COMPARATOR term logical_operation")
    def multiple_condition(self,p):
        return f"{p.term0}{p.COMPARATOR}{p.term1}{p.logical_operation}"
    
    @_("LOGICAL_OPERATOR term COMPARATOR term logical_operation")
    def logical_operation(self,p):
        if p.LOGICAL_OPERATOR == "AND":
            logical_operator = "&&"
        elif p.LOGICAL_OPERATOR == "OR":
            logical_operator = "||"

        return f"{logical_operator}{p.term0}{p.COMPARATOR}{p.term1}{p.logical_operation}"
    
    @_("")
    def logical_operation(self,p):
        return ""
    
    @_("ID")
    def term(self,p):
        return p.ID
    
    @_("value")
    def term(self,p):
        return p.value

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
