from sly import Lexer, Parser

class BasedLexer(Lexer):
    tokens = {ITYPE, UTYPE, ASSIGN, NAME, NUMBER, END}

    # Tokens
    ITYPE  = r"i64|i32|i16|i8|isize"
    UTYPE  = r"u64|u32|u16|u8|usize"
    ASSIGN = r"="
    NAME   = f"[a-zA-Z_][a-zA-Z0-9_\-]*"
    NUMBER = r"\d+"
    END    = ";"

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

    @_("ITYPE NAME ASSIGN NUMBER END")
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
            # I don't think size_t is signed
            type = "size_t"
        # else
            # Handle else case

        value = p.NUMBER

        return f"{type} x = {value};"


    @_("UTYPE NAME ASSIGN NUMBER END")
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
        # else
            # Handle else case

        value = p.NUMBER

        return f"{type} x = {value};"

    def __init__(self):
        pass

def main():
    lexer = BasedLexer()
    parser = BasedParser()

    while True:
        try:
            text = input('based > ')
            tokens = lexer.tokenize(text)
            # for token in tokens:
            #     print(token)
            result = parser.parse(tokens)
            print(result)
        except EOFError:
            break


if __name__ == '__main__':
    main()
