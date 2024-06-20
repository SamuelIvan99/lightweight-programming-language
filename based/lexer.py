from sly import Lexer

class BasedLexer(Lexer):
    tokens = { SIGNED_TYPE, UNSIGNED_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE, STRING_TYPE, ABYSS_TYPE,
               INTEGRAL_VALUE, FLOAT_VALUE, BOOL_VALUE, CHAR_VALUE, STRING_VALUE, 
               ID, ASSIGN, END, COMPARATOR, LBRACE, RBRACE, LPAREN, RPAREN, LSBRACKET, RSBRACKET,
               WHILE, FOR, MINUS, PLUS, MULTIPLICATION, DIVISION, AND, OR, IF, ELSE,
               COLON, COMMA, DECLARE, INSERTION, EXTRACTION, USE, RETURN, SYSTEM_VALUE }

    ignore = " \t"
    ignore_comment = r"\/\/.*"
    ignore_newline = r"\n+"

    SIGNED_TYPE   = r"\bi64\b|\bi32\b|\bi16\b|\bi8\b|\bisize\b"
    UNSIGNED_TYPE = r"\bu64\b|\bu32\b|\bu16\b|\bu8\b|\busize\b"
    FLOAT_TYPE    = r"\bf64\b|\bf32\b"
    BOOL_TYPE     = r"\bbool\b"
    CHAR_TYPE     = r"\bchar\b"
    STRING_TYPE   = r"\bstr\b"
    ABYSS_TYPE    = r"\babyss\b"

    INTEGRAL_VALUE = r"-?\b\d+(?!\.)\b"
    FLOAT_VALUE    = r"-?\b\d+(\.\d+)?\b"
    BOOL_VALUE     = r"\btrue\b|\bfalse\b"
    CHAR_VALUE     = r"\'(.|\\0|\\n)\'"
    STRING_VALUE   = r"\"[^\"]*\""
    SYSTEM_VALUE   = r"<[^\"<>]*>"

    WHILE    = r"\bwhile\b"
    FOR      = r"\bfor\b"
    IF       = r"\bif\b"
    ELSE     = r"\belse\b"
    DECLARE  = r"\blet\b"
    RETURN   = r"\breturn\b"

    USE      = r"\buse\b"

    AND            = r"\&\&"
    OR             = r"\|\|"
    MINUS          = r"\-"
    PLUS           = r"\+"
    DIVISION       = r"\/"
    MULTIPLICATION = r"\*"

    ID = r"\b[a-zA-Z_][a-zA-Z0-9_\-]*\b"

    INSERTION   = r"<<"
    EXTRACTION  = r">>"
    COMPARATOR  = r"==|!=|<=|>=|<|>"
    ASSIGN      = r"="
    END         = r";"
    LPAREN      = r"\("
    RPAREN      = r"\)"
    LSBRACKET   = r"\["
    RSBRACKET   = r"\]"
    LBRACE      = r"\{"
    RBRACE      = r"\}"
    COLON       = r"\:"
    COMMA       = r"\,"
