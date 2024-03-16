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
               ASS, END, SPACE }

    ITYPE = r"i64|i32|i16|i8|isize"
    UTYPE = r"u64|u32|u16|u8|usize"
    FTYPE = r"f32|f64"
    BTYPE = r"bool"
    CTYPE = r"char"


    IPRIM = r"-?\d+"
    FPRIM = r"-?\d+(\.\d+)?"
    BPRIM = r"true|false"
    CPRIM = r"\".\""

    ID = r"[a-zA-Z_][a-zA-Z0-9_\-]*"

    ASS = r"="
    END = r";"
    SPACE = r"\s"

    literals = {}

    ignore = " \t"
    ignore_newline = r"\n+"
    # ignore_comment = r""

class BasedParser(Parser):
    tokens = BasedLexer.tokens

    # @_("type SPACE ID blank ASS blank prim END")
    @_("type ID ASS prim END")
    def declaration(self, p):
        print(p.type)
        print(p.SPACE)
        print(p.ID)
        print(p.blank)
        print(p.ASS)
        print(p.blank)
        print(p.prim)
        print(p.END)

    @_("IPRIM")
    def prim(self, p):
        return p.IPRIM
    @_("FPRIM")
    def prim(self, p):
        return p.FPRIM
    @_("BPRIM")
    def prim(self, p):
        return p.BPRIM
    @_("CPRIM")
    def prim(self, p):
        return p.CPRIM

    @_("ITYPE")
    def type(self, p):
        return p.ITYPE
    @_("UTYPE")
    def type(self, p):
        return p.UTYPE
    @_("FTYPE")
    def type(self, p):
        return p.FTYPE
    @_("BTYPE")
    def type(self, p):
        return p.BTYPE
    @_("CTYPE")
    def type(self, p):
        return p.CTYPE

    # @_("SPACE")
    # def blank(self, p):
    #     return p.SPACE
    # @_("epsilon")
    # def blank(self, p):
    #     return p.epsilon

    # @_("")
    # def epsilon(self, p):
    #     pass

    # @_('ITYPE Id ASSER END')
    # def declaration(self, p):
    #     if p.ITYPE == "i64":
    #         type = "long long int"
    #     elif p.ITYPE == "i32":
    #         type = "long int"
    #     elif p.ITYPE == "i16":
    #         type = "int"
    #     elif p.ITYPE == "i8":
    #         type = "char"
    #     elif p.ITYPE == "isize": 
    #         type = "size_t" # I don't think size_t is signed

    #     if stack.lookup(p.Id):
    #         print()
    #     stack.bind(p.Id, type, p.NUMBER)

    #     return f"{type} {p.Id} = {p.NUMBER};"


    # @_('UTYPE Id ASSER END')
    # def declaration(self, p):
    #     if p.UTYPE == "u64":
    #         type = "unsigned long long int"
    #     elif p.UTYPE == "u32":
    #         type = "unsigned long int"
    #     elif p.UTYPE == "u16":
    #         type = "unsigned int"
    #     elif p.UTYPE == "u8":
    #         type = "unsigned char"
    #     elif p.UTYPE == "usize":
    #         type = "size_t"

    #     if stack.lookup(p.Id):
    #         print()
    #     stack.bind(p.Id, type, p.NUMBER)

    #     return f"{type} {p.Id} = {p.NUMBER};"

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

    while True:
        line = program.readline()
        # print(line)
        if not line:
            break

        tokens = lexer.tokenize(line)
        result = parser.parse(tokens)
        print(result)
        # compiled.write("\t" + result + "\n")

    compiled.write("\treturn 0;\n")
    compiled.write("}\n")
    compiled.close()

if __name__ == '__main__':
    main()
