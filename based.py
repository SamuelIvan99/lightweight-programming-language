from sly import Lexer, Parser

import os
import subprocess
import argparse

class Bindings:
    def __init__(self):
        self._stack = []

    def bind(self, name, mapping):
        self._stack.insert(0, (name, mapping))

    def lookup(self, name_to_find):
        scope_depth = []
        for result in self._stack:
            if result == "#":
                scope_depth.append(True)
            else:
                name, mapping = result
                if name == name_to_find:
                    return name, mapping

                if len(scope_depth) == self._stack.count("#"):
                    break
        return None

    def enter(self):
        self._stack.insert(0, "#")

    def exit(self):
        popped = []
        while len(self._stack) > 0 and self._stack[0] != "#":
            variable = self._stack.pop(0)
            popped.append(variable)
        if self._stack:
            self._stack.pop(0)
        return popped


class BasedLexer(Lexer):
    tokens = { SIGNED_TYPE, UNSIGNED_TYPE, FLOAT_TYPE, BOOL_TYPE, CHAR_TYPE, STRING_TYPE, ABYSS_TYPE,
               INTEGRAL_VALUE, FLOAT_VALUE, BOOL_VALUE, CHAR_VALUE, STRING_VALUE, 
               ID, ASSIGN, END, COMPARATOR, LBRACE, RBRACE, LPAREN, RPAREN, LSBRACKET, RSBRACKET,
               WHILE, FOR, MINUS, PLUS, MULTIPLICATION, DIVISION, AND, OR, IF, ELSE,
               COLON, COMMA, DECLARE, INSERTION, EXTRACTION, INCLUDE, USE, RETURN, SYSTEM_VALUE }

    literals = {}

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
    CHAR_VALUE     = r"\'.\'"
    STRING_VALUE   = r"\"[^\"]*\""
    SYSTEM_VALUE   = r"<[^\"]*>"

    WHILE    = r"\bwhile\b"
    FOR      = r"\bfor\b"
    IF       = r"\bif\b"
    ELSE     = r"\belse\b"
    DECLARE  = r"\blet\b"
    RETURN   = r"\breturn\b"

    INCLUDE  = r"\binclude\b"
    USE      = r"\buse\b"

    AND            = r"\&\&"
    OR             = r"\|\|"
    MINUS          = r"\-"
    PLUS           = r"\+"
    DIVISION       = r"\/"
    MULTIPLICATION = r"\*"

    ID             = r"\b[a-zA-Z_][a-zA-Z0-9_\-]*\b"

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

class BasedParser(Parser):
    tokens = BasedLexer.tokens
    debugfile = "dist/debug"

    def __init__(self):
        self.scalar_bindings = Bindings()
        self.array_bindings = Bindings()


        self.based_includes = set()

    #region program
    @_("globals")
    def program(self, p): 
        return f"{p.globals}"
    #endregion

    #region globals
    @_("globall globals")
    def globals(self, p):
        return f"{p.globall}{p.globals}"
    @_("")
    def globals(self, p):
        return ""
    @_("function")
    def globall(self, p):
        return f"{p.function}"
    @_("include")
    def globall(self, p):
        return f"{p.include}"
    @_("scalar_declaration_init END")
    def globall(self, p):
        return f"{p.scalar_declaration_init};"
    #endregion

    #region includes
    @_("INCLUDE STRING_VALUE")
    def include(self, p):
        return f"#include {p.STRING_VALUE}\n"
    @_("INCLUDE SYSTEM_VALUE")
    def include(self, p):
        return f"#include {p.SYSTEM_VALUE}\n"
    @_("USE STRING_VALUE")
    def include(self, p):
        based_file_name = p.STRING_VALUE.replace("\"", "")
        self.based_includes.add(based_file_name)
        based_file_name = based_file_name.replace(".based", ".c")
        return f"#include \"{based_file_name}\"\n"
    #endregion

    #region function
    @_("ID LPAREN new_scope formal_params RPAREN COLON type LBRACE statements pop_scope RBRACE")
    def function(self, p):
        _, mapping, _, _, _ = p.type
        return f"{mapping} {p.ID}({p.formal_params}){{{p.statements}{p.pop_scope}}}"
    @_("ID COLON type multi_formal_params")
    def formal_params(self, p):
        _, mapping, _, _, _ = p.type
        self.scalar_bindings.bind(p.ID, mapping)

        return f"{mapping} {p.ID}{p.multi_formal_params}"
    @_("ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params")
    def formal_params(self, p):
        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)

        return f"Array {p.ID}{p.multi_formal_params}"
    @_("ID LSBRACKET RSBRACKET COLON type multi_formal_params")
    def formal_params(self, p):
        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)

        return f"Array {p.ID}{p.multi_formal_params}"
    @_("")
    def formal_params(self, p):
        return ""
    @_("COMMA ID COLON type multi_formal_params")
    def multi_formal_params(self, p):
        _, mapping, _, _, _ = p.type
        self.scalar_bindings.bind(p.ID, mapping)
        return f", {mapping} {p.ID}{p.multi_formal_params}"
    @_("COMMA ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type multi_formal_params")
    def multi_formal_params(self, p):
        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)
        return f", Array {p.ID}{p.multi_formal_params}"
    @_("COMMA ID LSBRACKET RSBRACKET COLON type multi_formal_params")
    def multi_formal_params(self, p):
        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)
        return f", Array {p.ID}{p.multi_formal_params}"
    @_("")
    def multi_formal_params(self, p):
        return ""
    @_("ID LPAREN actual_params RPAREN")
    def function_call(self, p):
        return f"{p.ID}({p.actual_params})"
    @_("expression multi_actual_params")
    def actual_params(self, p):
        return f"{p.expression}{p.multi_actual_params}"
    @_("")
    def actual_params(self, p):
        return ""
    @_("COMMA expression multi_actual_params")
    def multi_actual_params(self, p):
        return f", {p.expression}{p.multi_actual_params}"
    @_("")
    def multi_actual_params(self, p):
        return ""
    #endregion

    #region scope
    @_("LBRACE new_scope statements pop_scope RBRACE")
    def scope(self, p):
        return f"{{{p.statements}{p.pop_scope}}}"
    @_("")
    def new_scope(self, p):
        self.scalar_bindings.enter()
        self.array_bindings.enter()
    @_("")
    def pop_scope(self, p):
        self.scalar_bindings.exit()
        popped = self.array_bindings.exit()
        return "".join([f"free({name}.value);" for name, _ in popped])
    #endregion

    #region statements
    @_("statement statements")
    def statements(self, p):
        return f"{p.statement}{p.statements}"
    @_("")
    def statements(self, p):
        return ""
    #endregion

    #region statement
    @_("expression END")
    def statement(self, p):
        return f"{p.expression};"
    @_("scalar_declaration END")
    def statement(self, p):
        return f"{p.scalar_declaration};"
    @_("array_declaration END")
    def statement(self, p):
        return f"{p.array_declaration};"
    @_("scalar_declaration_init END")
    def statement(self, p):
        return f"{p.scalar_declaration_init};"
    @_("array_declaration_init END")
    def statement(self, p):
        return f"{p.array_declaration_init};"
    @_("scalar_assignment END")
    def statement(self, p):
        return f"{p.scalar_assignment};"
    @_("array_assignment END")
    def statement(self, p):
        return f"{p.array_assignment};"
    @_("scope")
    def statement(self, p):
        return f"{p.scope}"
    @_("while_statement")
    def statement(self, p):
        return f"{p.while_statement}"
    @_("for_statement")
    def statement(self, p):
        return f"{p.for_statement}"
    @_("if_statement")
    def statement(self, p):
        return f"{p.if_statement}"
    @_("return_statement END")
    def statement(self, p):
        return f"{p.return_statement};"
    @_("insertion_statement END")
    def statement(self, p):
        return f"{p.insertion_statement}"
    @_("extraction_statement END")
    def statement(self, p):
        return f"{p.extraction_statement}"
    @_("END")
    def statement(self, p):
        return ";"
    #endregion

    #region forstatement
    @_("scalar_declaration_init")
    def for_init(self, p):
        return f"{p.scalar_declaration_init}"
    @_("scalar_assignment")
    def for_init(self, p):
        return f"{p.scalar_assignment}"
    @_("array_declaration_init")
    def for_init(self, p):
        return f"{p.array_declaration_init}"
    @_("array_assignment")
    def for_init(self, p):
        return f"{p.array_assignment}"
    @_("expression")
    def for_init(self, p):
        return f"{p.expression}"
    @_("")
    def for_init(self, p):
        return ""
    @_("expression")
    def for_condition(self, p):
        return f"{p.expression}"
    @_("")
    def for_condition(self, p):
        return ""
    @_("scalar_assignment")
    def for_increment(self, p):
        return f"{p.scalar_assignment}"
    @_("array_assignment")
    def for_increment(self, p):
        return f"{p.array_assignment}"
    @_("expression")
    def for_increment(self, p):
        return f"{p.expression}"
    @_("")
    def for_increment(self, p):
        return ""
    @_("FOR LPAREN new_scope for_init END for_condition END for_increment RPAREN LBRACE statements pop_scope RBRACE")
    def for_statement(self,p):
        return f"for({p.for_init};{p.for_condition};{p.for_increment}){{{p.statements}{p.pop_scope}}}"
    #endregion

    #region whilestatement    
    @_("WHILE LPAREN expression RPAREN scope")
    def while_statement(self, p):
        return f"while({p.expression}){p.scope}"
    #endregion

    #region ifstatement
    @_("IF LPAREN expression RPAREN scope else_statement")
    def if_statement(self, p):
        return f"if({p.expression}){p.scope}{p.else_statement}"
    @_("ELSE scope")
    def else_statement(self, p):
        return f"else{p.scope}" 
    @_("ELSE if_statement")
    def else_statement(self, p):
        return f"else {p.if_statement}"
    @_("")
    def else_statement(self, p):
        return ""
    #endregion

    #region returnstatement
    @_("RETURN expression")
    def return_statement(self, p):
        return f"return {p.expression}"
    #endregion

    #region declaration
    @_("DECLARE ID COLON type")
    def scalar_declaration(self, p):
        if self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID):
            print(f"ERROR: variable '{p.ID}' already defined in scope")
            exit(1)

        _, mapping, _, _, _ = p.type
        self.scalar_bindings.bind(p.ID, mapping)
        return f"{mapping} {p.ID}"
    @_("DECLARE ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type")
    def array_declaration(self, p):
        if self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID):
            print(f"ERROR: variable '{p.ID}' already defined in scope")
            exit(1)

        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)

        return f"Array {p.ID};{p.ID}.size={p.INTEGRAL_VALUE};{p.ID}.value=calloc({p.ID}.size ,sizeof({mapping}))"
    #endregion

    #region declaration_init
    @_("DECLARE ID COLON type ASSIGN expression")
    def scalar_declaration_init(self, p):
        if self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID):
            print(f"ERROR: variable '{p.ID}' already defined in scope")
            exit(1)

        type_name, mapping, _, _, _ = p.type
        self.scalar_bindings.bind(p.ID, mapping)
        if type_name == "str":
            return f"{mapping} {p.ID}[]={p.expression}"
        else:
            return f"{mapping} {p.ID}={p.expression}"
    @_("DECLARE ID LSBRACKET INTEGRAL_VALUE RSBRACKET COLON type ASSIGN array_init")
    def array_declaration_init(self, p):
        if self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID):
            print(f"ERROR: variable '{p.ID}' already defined in scope")
            exit(1)

        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)

        values = p.array_init

        array_declaration = f"""
            Array {p.ID} = 
            {{
                .value = calloc({p.ID}.size ,sizeof({mapping})),
                .size = {p.INTEGRAL_VALUE}
            }};
        """
        array_init = ";".join([
            f"(({mapping}*)getElement({p.ID},{i}))[{i}]={values[i]}"
            for i in range(len(values))
        ])

        return f"{array_declaration}{array_init}"
    @_("DECLARE ID LSBRACKET RSBRACKET COLON type ASSIGN array_init")
    def array_declaration_init(self, p):
        if self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID):
            print(f"ERROR: variable '{p.ID}' already defined in scope")
            exit(1)

        _, mapping, _, _, _ = p.type
        self.array_bindings.bind(p.ID, mapping)

        values = p.array_init

        array_declaration = f"""
            Array {p.ID} = 
            {{
                .value = calloc({p.ID}.size ,sizeof({mapping})),
                .size = {len(values)}
            }};
        """
        array_init = ";".join([
            f"(({mapping}*)getElement({p.ID},{i}))[{i}]={values[i]}"
            for i in range(len(values))
        ])

        return f"{array_declaration}{array_init}"
    @_("STRING_VALUE")
    def array_init(self, p):
        result = p.STRING_VALUE.replace("\"", "")
        result = [f"'{char}'" for char in result]
        return list(result)
    @_("LBRACE value multi_array_init RBRACE")
    def array_init(self, p):
        return [p.value] + p.multi_array_init
    @_("COMMA value multi_array_init")
    def multi_array_init(self, p):
        return [p.value] + p.multi_array_init
    @_("")
    def multi_array_init(self, p):
        return []
    #endregion

    #region assignment
    @_("ID ASSIGN expression")
    def scalar_assignment(self, p):
        result = self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID)
        if not result:
            print(f"ERROR: variable '{p.ID}' not in scope")
            exit(1)
        return f"{p.ID}={p.expression}"
    @_("ID LSBRACKET arithmetic_layer RSBRACKET ASSIGN expression")
    def array_assignment(self, p):
        result = self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID)
        if not result:
            print(f"ERROR: variable '{p.ID}' not in scope")
            exit(1)

        _, mapping = result
        return f"(({mapping}*)getElement({p.ID},{p.arithmetic_layer}))[{p.arithmetic_layer}]={p.expression}"
    #endregion

    #region insertion
    @_("expression INSERTION expression multi_insertion")
    def insertion_statement(self, p):
        return self.handle_insertions(p.expression0, p.expression1, p.multi_insertion)
    @_("INSERTION expression multi_insertion")
    def multi_insertion(self, p):
        return (p.expression, p.multi_insertion)
    @_("")
    def multi_insertion(self, p):
        return ()
    def handle_insertions(self, initial, current, remaining):
        code = f"{initial}.write({initial}.writer, {current});"
        if remaining:
            next_expression, next_remaining = remaining
            code += self.handle_insertions(initial, next_expression, next_remaining)
        return code
    #endregion

    #region extraction
    @_("expression EXTRACTION expression multi_extraction")
    def extraction_statement(self, p):
        return self.handle_extraction(p.expression0, p.expression1, p.multi_extraction)
    @_("EXTRACTION expression multi_extraction")
    def multi_extraction(self, p):
        return (p.expression, p.multi_extraction)
    @_("")
    def multi_extraction(self, p):
        return ()
    def handle_extraction(self, initial, current, remaining):
        code = f"{initial}.write({initial}.writer, {current});"
        if remaining:
            next_expression, next_remaining = remaining
            code += self.handle_extraction(initial, next_expression, next_remaining)
        return code
    #endregion

    #region expression
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
        return f"{p.arithmetic_layer}+{p.term}"
    @_("arithmetic_layer MINUS term")
    def arithmetic_layer(self, p):
        return f"{p.arithmetic_layer}-{p.term}"
    @_("term")
    def arithmetic_layer(self, p):
        return f"{p.term}"
    @_("term MULTIPLICATION factor")
    def term(self, p):
        return f"{p.term}*{p.factor}"    
    @_("term DIVISION factor")
    def term(self, p):
        return f"{p.term}/{p.factor}" 
    @_("factor")
    def term(self, p):
        return f"{p.factor}"
    @_("function_call")
    def factor(self, p):
        return f"{p.function_call}"
    @_("LPAREN expression RPAREN")
    def factor(self, p):
        return f"({p.expression})"
    @_("value")
    def factor( self,p):
        return f"{p.value}"
    @_("ID LSBRACKET arithmetic_layer RSBRACKET")
    def factor(self, p):
        result = self.scalar_bindings.lookup(p.ID) or \
            self.array_bindings.lookup(p.ID)
        if not result:
            print(f"ERROR: variable '{p.ID}' not in scope")
            exit(1)

        _, mapping = result
        return f"(({mapping}*)getElement({p.ID},{p.arithmetic_layer}))[{p.arithmetic_layer}]"
    @_("ID")
    def factor(self, p):
        scalar_result = self.scalar_bindings.lookup(p.ID)
        array_result = self.array_bindings.lookup(p.ID)
        result = scalar_result or array_result
        if not result:
            print(f"ERROR: variable '{p.ID}' not in scope")
            exit(1)

        if scalar_result:
            return f"{p.ID}"
        elif array_result:
            return f"{p.ID}.value"
    #endregion

    #region type
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
    @_("ABYSS_TYPE")
    def type(self, p):
        return (
            p.ABYSS_TYPE,
            "void",
            "0",
            "0",
            "0"
        )
    @_("ID")
    def type(self, p):
        return (
            p.ID,
            p.ID,
            "0",
            "0",
            "0"
        )
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
        return f"{p.CHAR_VALUE}"
    @_("STRING_VALUE")
    def value(self, p):
        return f"{p.STRING_VALUE}"
    #endregion

def compile_based(based_file_name, lexer, parser):
    with open(based_file_name) as based_file:
        program = based_file.read()
        tokens = lexer.tokenize(program)
        result = parser.parse(tokens)

    c_file_name = based_file_name.replace(".based", ".c")
    c_file_name = f"dist/{c_file_name}"
    if os.path.exists(c_file_name):
        os.remove(c_file_name)

    with open(c_file_name, "a") as c_file:
        c_file.write(result)

    subprocess.run(["clang-format", "-i", c_file_name])

    if (len(parser.based_includes) > 0):
        based_include_name = parser.based_includes.pop()
        compile_based(based_include_name, lexer, parser)
    return c_file_name

def parse_args():
    parser = argparse.ArgumentParser(prog="BasedCompiler",
        description="Compile your based source code into native machine code", epilog="") 
    parser.add_argument("-b", "--based-source", required=True, nargs="+", help="Based source files to compile")
    parser.add_argument("-c", "--c-source", nargs="+", help="C source files to compile")
    parser.add_argument("-I", "--include", help="C header files to include")
    parser.add_argument("-o", "--output", required=True, help="Output executable")
    return parser.parse_args()

def main():
    args = parse_args()
    # For compiled machine code
    if not os.path.exists("bin"):
        os.mkdir("bin")

    # For transpiled C code        
    if not os.path.exists("dist"):
        os.mkdir("dist")

    lexer = BasedLexer()
    parser = BasedParser()

    based_compiled_names = [
        compile_based(based_file_name, lexer, parser) 
        for based_file_name in args.based_source
    ]
    based_compiled_names = " ".join(based_compiled_names)

    c_source_names = ""
    if args.c_source:
        c_source_names = " ".join(args.c_source)

    c_include_names = ""
    if args.include:
        c_include_names = f"-I{args.include}"

    os.system(f"gcc {based_compiled_names} {c_source_names} -o {args.output} {c_include_names}")

if __name__ == "__main__":
    main()
