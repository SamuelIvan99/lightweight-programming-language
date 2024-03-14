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
    tokens = {ITYPE, UTYPE, CHARTYPE, NAME, NUMBER, LBRACE, RBRACE, ASSIGN, END}

    # Ints
    ITYPE  = r"i64|i32|i16|i8|isize"
    UTYPE  = r"u64|u32|u16|u8|usize"
    # Chars
    CHARTYPE = "char"
    # Floats
    # Int Constants
    NUMBER = r"\d+"
    # Variable Identifier
    ID     = f"[a-zA-Z_][a-zA-Z0-9_\-]*"
    # Punctuators
    LBRACE = "{"
    RBRACE = "}"
    # Arithmetics
    # Assignment
    ASSIGN = "="
    # Terminator
    END    = ";"

    # literals
    literals = {}

    # Ignoring whitespace
    ignore = " \t"

    # Ignoring comments
    # ignore_comment = r""

    # Ignoring newline
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print("Line %d: Bad character %r" % (self.lineno, t.value[0]))
        self.index += 1

class BasedParser(Parser):
    tokens = BasedLexer.tokens

    @_("declaration")
    def stat(self, p):

    @_("")
    def statements(self, p):

    @_("LBRACE new_scope statements RBRACE")
    def statements(self, p):
        stack.exit()

    @_("")
    def new_scope(self, p):
        stack.enter()

    @_('ITYPE NAME ASSIGN NUMBER END')
    def declaration(self, p):
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

        if stack.lookup(p.NAME):
            print()
        stack.bind(p.NAME, type, p.NUMBER)

        return f"{type} {p.NAME} = {p.NUMBER};"


    @_('UTYPE NAME ASSIGN NUMBER END')
    def declaration(self, p):
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

        if stack.lookup(p.NAME):
            print()
        stack.bind(p.NAME, type, p.NUMBER)

        return f"{type} {p.NAME} = {p.NUMBER};"

    def __init__(self):
        pass

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
        if not line:
            break
        tokens = lexer.tokenize(line)
        result = parser.parse(tokens)
        compiled.write("\t" + result + "\n")

    compiled.write("\treturn 0;\n")
    compiled.write("}\n")
    compiled.close()

if __name__ == '__main__':
    main()
