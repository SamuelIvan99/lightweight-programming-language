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
    tokens = { SIGNED_TYPE, UNSIGNED_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE, STRING_TYPE, ABYSS_TYPE,
               INTEGRAL_VALUE, FLOAT_VALUE, BOOL_VALUE, CHAR_VALUE, STRING_VALUE, 
               ID, ASSIGN, END, COMPARATOR, LBRACE, RBRACE, LPAREN, RPAREN, LSBRACKET, RSBRACKET,
               WHILE, MINUS, PLUS, MULTIPLICATION, DIVISION, AND, OR, IF, ELSE,
               COLON, COMMA, INSERTION, EXTRACTION}

    SIGNED_TYPE   = r"i64|i32|i16|i8|isize"
    UNSIGNED_TYPE = r"u64|u32|u16|u8|usize"
    FLOAT_TYPE    = r"f64|f32"
    BOOL_TYPE     = r"bool"
    CHAR_TYPE     = r"char"
    STRING_TYPE   = r"str"
    ABYSS_TYPE    = r"abyss"

    INTEGRAL_VALUE = r"-?\d+"
    FLOAT_VALUE    = r"-?\d+\.\d+"
    BOOL_VALUE     = r"true|false"
    CHAR_VALUE     = r"\'.\'"
    STRING_VALUE   = r"\"[^\"]*\""

    WHILE = r"while"
    IF    = r"if"
    ELSE  = r"else"

    AND            = r"\&\&"
    OR             = r"\|\|"
    MINUS          = r"\-"
    PLUS           = r"\+"
    DIVISION       = r"\/"
    MULTIPLICATION = r"\*"

    ID = r"[a-zA-Z_][a-zA-Z0-9_\-]*"

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

    literals = {}

    ignore = " \t"

    @_(r"\n+")
    def ignore_newline(self, t):
        pass

    ignore_comment = r"#.*"

class BasedParser(Parser):
    tokens = BasedLexer.tokens
    debugfile = "dist/debug"

    def __init__(self):
        globalScope = []
        self.scopesList = [globalScope]

        globalArrayScope = []
        self.arrayScopeList = [globalArrayScope]

    @_("functions")
    def program(self, p):
        return f"{p.functions}"

    @_("ID")
    def var_name(self, p):
        return f"{p.ID}"
    @_("array_name")
    def var_name(self, p):
        return f"{p.array_name}"
    @_("ID LSBRACKET arithmetic_layer RSBRACKET")
    def array_name(self,p):
        return f"{p.ID}{p.LSBRACKET}{p.arithmetic_layer}{p.RSBRACKET}"

    #region functions
    @_("function functions")
    def functions(self, p):
        return f"{p.function}{p.functions}"
    @_("")
    def functions(self, p):
        return ""
    @_("ID LPAREN formal_params RPAREN COLON return_type scope")
    def function(self, p):
        return f"{p.return_type} {p.ID}{p.LPAREN}{p.formal_params}{p.RPAREN}{p.scope}" 
    @_("var_name type multi_formal_params")
    def formal_params(self, p):
        type_name,mapping,min,max,default = p.type
        return f"{mapping} {p.var_name}{p.multi_formal_params}"
    @_("")
    def formal_params(self, p):
        return ""
    @_("COMMA var_name type multi_formal_params")
    def multi_formal_params(self, p):
        type_name,mapping,min,max,default = p.type
        return f"{p.COMMA}{mapping} {p.var_name}{p.multi_formal_params}"
    @_("")
    def multi_formal_params(self, p):
        return ""

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
    @_("expression END")
    def statement(self, p):
        return f"{p.expression}{p.END}"
    @_("declaration END")
    def statement(self, p):
        return f"{p.declaration}{p.END}"
    @_("declaration_init END")
    def statement(self, p):
        return f"{p.declaration_init}{p.END}"
    @_("assignment END")
    def statement(self, p):
        return f"{p.assignment}{p.END}"
    @_("scope")
    def statement(self,p):
        return p.scope
    @_("while_statement")
    def statement(self, p):
        return f"{p.while_statement}"
    @_("if_statement")
    def statement(self, p):
        return f"{p.if_statement}"
    @_("END")
    def statement(self, p):
        return f"{p.END}"
    
    @_("WHILE LPAREN expression RPAREN scope")
    def while_statement(self,p):
        return f"{p.WHILE}{p.LPAREN}{p.expression}{p.RPAREN}{p.scope}"
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
    #endregion

    #region declaration
    @_("var_name COLON type")
    def declaration(self, p):
        if(p.var_name in self.scopesList[-1]):
            print(f"ERROR: redefinition of {p.var_name}")
            exit(1)
        self.scopesList[-1].append(p.var_name)
        type_name, mapping, min, max, default = p.type
        # bindings.bind(p.ID, type_name, default)
        return f"{mapping} {p.var_name}"

    @_("var_name COLON type ASSIGN expression")
    def declaration_init(self, p):
        if(p.var_name in self.scopesList[-1]):
            print(f"ERROR: redefinition of {p.var_name}")
            exit(1)
        self.scopesList[-1].append(p.var_name)
        type_name, mapping, min, max, default = p.type
        value = p.expression
        # if value < min or value > max:
        #     print(f"ERROR: overflow detected in {type_name}{p.var_name}{p.ASSIGN}{value}, assigned value must be in range [{min},{max}]")
        #     exit(1)
        # bindings.bind(p.var_name, type_name, value)
        if type_name == "str":
            return f"{mapping} {p.var_name}[]{p.ASSIGN}{value}"
        else:        
            return f"{mapping} {p.var_name}{p.ASSIGN}{value}"
        
    # Troublesome declaration
    # @_("type ID LSBRACKET term RSBRACKET END")
    # def declaration(self, p):
    #     type_name, mapping, min, max, default = p.type
    #     arr = (p.ID,mapping)
    #     if(arr in self.arrayScopeList[-1] or arr[0] in self.scopesList[-1]):
    #         print(f"ERROR: redefinition of {arr[0]}")
    #         exit(1)
    #     self.arrayScopeList[-1].append(arr)
    #     self.scopesList[-1].append(arr[0])
    #     value = p.term
    #     return f"Array {arr[0]}{p.END} {arr[0]}.size = {value}{p.END} {arr[0]}.value = malloc(sizeof({arr[1]})*{value}){p.END}"
    #endregion

    #region assignment
    @_("ID ASSIGN expression")
    def assignment(self, p):
        var_name = p.ID
        if(var_name not in self.scopesList[-1]):
            print(f"ERROR: variable: {var_name} not found")
            exit(1)
        value = p.expression          
        return f"{var_name}{p.ASSIGN}{value}"
    
    @_("ID LSBRACKET arithmetic_layer RSBRACKET ASSIGN expression")
    def assignment(self, p):
        var_name = p.ID
        flag = 1
        arr = ("","")
        for i in self.arrayScopeList[-1]:
            if(i[0] == var_name):
                flag = 0
                arr = i
                break
        if(flag):
            print(f"ERROR: variable: {var_name} not found")
            exit(1)
        value = p.expression
        return f"(({arr[1]}*)getElement({arr[0]},{p.arithmetic_layer}))[{p.arithmetic_layer}]{p.ASSIGN}{value}"
    #endregion

    #region expressions
    @_("ID LSBRACKET arithmetic_layer RSBRACKET")
    def expression(self, p):
        var_name = p.ID
        flag = 1
        arr = ("","")
        for i in self.arrayScopeList[-1]:
            if(i[0] == var_name):
                flag = 0
                arr = i
                break
        if(flag):
            print(f"ERROR: variable: {var_name} not found")
            exit(1)
        return f"(({arr[1]}*)getElement({arr[0]},{p.arithmetic_layer}))[{p.arithmetic_layer}]"
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

    #region type and return type
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
    @_("STRING_TYPE")
    def type(self, p):
        return (
            p.STRING_TYPE,
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
    
    @_("type")
    def return_type(self, p):
        type_name, mapping, min, max, default = p.type
        return f"{mapping}"

    @_("ABYSS_TYPE")
    def return_type(self, p):
        return "void"

    #endregion

    #region value
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
    @_("STRING_VALUE")
    def value(self, p):
        return p.STRING_VALUE
    #endregion

    #region scope
    @_("LBRACE new_scope statements pop_scope RBRACE")
    def scope(self,p):
        return f"{p.LBRACE}{p.statements}{p.pop_scope}{p.RBRACE}"

    @_('')
    def new_scope(self,p):
        newScope = []
        newArrayScope = []
        self.scopesList.append(newScope)
        self.arrayScopeList.append(newArrayScope)

    @_('')
    def pop_scope(self,p):
        s = f""
        for i in self.arrayScopeList[-1]:
            s += f"free({i[0]}.value);\n"
        self.scopesList.pop()
        self.arrayScopeList.pop()
        return s
    #endregion
    
    
    # @_("STRING_TYPE ID ASSIGN STRING_VALUE END")
    # def declaration_init(self, p):
    #     return f"char {p.ID}[] {p.ASSIGN} {p.STRING_VALUE}{p.END}"

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
        c_file.write(f"#include \"array.h\"\n\n{result}")
    # subprocess.run(["clang-format", "-i", "dist/out.c"])
    # os.system("gcc dist/out.c -o bin/based")
if __name__ == '__main__':
    main()
