from sly import Lexer, Parser
import os

class SymbolStack():
    def __init__(self):
        self._stack = []

    def empty(self):
        pass

    def bind(self, name, type, value):
        self._stack.append(
            (name, type, value)
        )

    def lookup(self, name):
        for n, type, value in self._stack:
            if n == name:
                return True
        return False

    def enter(self):
        self._stack.append("#")

    def exit(self):
        for item in self._stack:
            if item == "#":
                self._stack.pop(len(self._stack) - 1)
                break
            self._stack.pop(len(self._stack) - 1)

stack = SymbolStack()

class BasedLexer(Lexer):
    # Tokens
    tokens = { ITYPE, UTYPE, FTYPE, BTYPE, CTYPE,
               IPRIM, FPRIM, BPRIM, CPRIM, ID,
               ASS, END }

    ITYPE = r"i64|i32|i16|i8|isize"
    UTYPE = r"u64|u32|u16|u8|usize"
    FTYPE = r"f64|f32"
    BTYPE = r"bool"
    CTYPE = r"char"

    IPRIM = r"-?\d+"
    FPRIM = r"-?\d+(\.\d+)?"
    BPRIM = r"true|false"
    CPRIM = r'".*"'

    ID = r"[a-zA-Z_][a-zA-Z0-9_\-]*"

    ASS = r"="
    END = r";"

    literals = {}

    ignore = " \t"
    ignore_newline = r"\n+"
    ignore_comment = r"#.*"

class BasedParser(Parser):
    tokens = BasedLexer.tokens

    @_("statements")
    def program(self, p):
        return p.statements
    @_("statements END statement")
    def statements(self, p):
        return f"{p.statement}{p.END}{p.statements}"
    @_("statement END")
    def statements(self, p):
        return f"{p.statement}{p.END}"
    @_("type ID ASS prim")
    def statement(self, p):
        return f"{p.type} {p.ID} {p.ASS} {p.prim}"
    @_("")
    def statement(self, p):
        return ""

    @_("ITYPE")
    def type(self, p):
        if p.ITYPE == "i64":
            type = "long long int"
        elif p.ITYPE == "i32":
            type = "long int"
        elif p.ITYPE == "i16":
            type = "int"
        elif p.ITYPE == "i8":
            type = "char"
        elif p.ITYPE == "isize": 
            type = "size_t" # I don't think size_t is signed
        return type
    @_("UTYPE")
    def type(self, p):
        if p.UTYPE == "u64":
            type = "unsigned long long int"
        elif p.UTYPE == "u32":
            type = "unsigned long int"
        elif p.UTYPE == "u16":
            type = "unsigned int"
        elif p.UTYPE == "u8":
            type = "unsigned char"
        elif p.UTYPE == "usize":
            type = "size_t"
        return type
    @_("FTYPE")
    def type(self, p):
        if p.FTYPE == "f64":
            type = "double"
        elif p.FTYPE == "f32":
            type = "float"
        return type
    @_("BTYPE")
    def type(self, p):
        return "char"
    @_("CTYPE")
    def type(self, p):
        return "char"

    @_("IPRIM")
    def prim(self, p):
        return p.IPRIM
    @_("FPRIM")
    def prim(self, p):
        return p.FPRIM
    @_("BPRIM")
    def prim(self, p):
        if p.BPRIM == "true":
            value = "0x01"
        elif p.BPRIM == "false":
            value = "0x00"
        return value
    @_("CPRIM")
    def prim(self, p):
        return p.CPRIM

    # @_("SPACES")
    # def blank(self, p):
    #     return p.SPACES
    # @_("")
    # def blank(self, p):
    #     return ""

def main():
    if not os.path.exists("dist"):
        os.mkdir("dist")
    if os.path.exists("dist/out.c"):
        os.remove("dist/out.c")
    program = open("src.based", "r")
    compiled = open("dist/out.c", "a")

    lexer = BasedLexer()
    parser = BasedParser()

    compiled.write("int main() {\n")

    with open("src.based") as f:
        program = f.read()
        tokens = lexer.tokenize(program)
        result = parser.parse(tokens)
        print(result)


    # while True:
    #     try:
    #         line = program.readline()
    #     except EOFError:
    #         break
    #     tokens = lexer.tokenize(line)
    #     # compiled.write("\t" + result + "\n")

    compiled.write("\treturn 0;\n")
    compiled.write("}\n")
    compiled.close()

if __name__ == '__main__':
    main()
