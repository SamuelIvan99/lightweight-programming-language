from sly import Lexer, Parser
import os

class BasedLexer(Lexer):
    tokens = { INT_TYPE, UNSIGNED_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE,
               INT, FLOAT, BOOL, CHAR, ID,
               ASSIGN, END }

    INT_TYPE      = r"i64|i32|i16|i8|isize"
    UNSIGNED_TYPE = r"u64|u32|u16|u8|usize"
    FLOAT_TYPE    = r"f64|f32"
    BOOL_TYPE     = r"bool"
    CHAR_TYPE     = r"char"

    FLOAT = r"-?\d+(\.\d+)?"
    INT   = r"-?\d+"
    BOOL  = r"true|false"
    CHAR  = r'"."'

    ID = r"[a-zA-Z_][a-zA-Z0-9_\-]*"

    ASSIGN = r"="
    END    = r";"

    literals = {}

    ignore = " \t"
    @_(r"\n+")
    def ignore_newline(self, t):
        pass

    ignore_comment = r"#.*"

class BasedParser(Parser):
    tokens = BasedLexer.tokens

    @_("statements")
    def program(self, p):
        return p.statements

    @_("statement END statements")
    def statements(self, p):
        return f"{p.statement}{p.END}{p.statements}"
    @_("")
    def statements(self, p):
        return ""

    @_("declaration")
    def statement(self, p):
        return p.declaration
    @_("")
    def statement(self, p):
        return ""

    @_("type ID initializer")
    def declaration(self, p):
        return f"{p.type} {p.ID} {p.initializer}"

    @_("ASSIGN primitive")
    def initializer(self, p):
        return f"{p.ASSIGN} {p.primitive}"
    @_("")
    def initializer(self, p):
        return ""

    @_("INT_TYPE")
    def type(self, p):
        if p.INT_TYPE == "i64":
            type = "long long int"
        elif p.INT_TYPE == "i32":
            type = "long int"
        elif p.INT_TYPE == "i16":
            type = "int"
        elif p.INT_TYPE == "i8":
            type = "char"
        elif p.INT_TYPE == "isize": 
            type = "size_t" # I don't think size_t is signed
        return type
    @_("UNSIGNED_TYPE")
    def type(self, p):
        if p.UNSIGNED_TYPE == "u64":
            type = "unsigned long long int"
        elif p.UNSIGNED_TYPE == "u32":
            type = "unsigned long int"
        elif p.UNSIGNED_TYPE == "u16":
            type = "unsigned int"
        elif p.UNSIGNED_TYPE == "u8":
            type = "unsigned char"
        elif p.UNSIGNED_TYPE == "usize":
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

    @_("INT")
    def primitive(self, p):
        return p.INT
    @_("FLOAT")
    def primitive(self, p):
        return p.FLOAT
    @_("BOOL")
    def primitive(self, p):
        if p.BOOL == "true":
            value = "0x01"
        elif p.BOOL == "false":
            value = "0x00"
        return value
    @_("CHAR")
    def primitive(self, p):
        return p.CHAR

def main():
    if not os.path.exists("dist"):
        os.mkdir("dist")
    if os.path.exists("dist/out.c"):
        os.remove("dist/out.c")

    lexer = BasedLexer()
    parser = BasedParser()

    with open("src.based") as based_file:
        program = based_file.read()
        tokens = lexer.tokenize(program)
        result = parser.parse(tokens)

    with open("dist/out.c", "a") as c_file:
        c_file.write(f"int main(){{{result}return 0;}}")

if __name__ == '__main__':
    main()
