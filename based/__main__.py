from lexer import BasedLexer
from parser import BasedParser

import os
import argparse
import subprocess
import sys


def remove_dir_contents(dir):
    for file in os.listdir(dir):
        os.remove(os.path.join(dir, file))


def check_files_exist(files):
    for file in files:
        if not os.path.exists(file):
            print(f"Error: File '{file}' does not exist.")
            sys.exit(1)


def compile_library():
    stdlib_dir = "stdlib_implementation"
    lib_dir = "lib"
    include_dir = "include"

    if not os.path.exists(stdlib_dir):
        print(f"Error: Directory '{stdlib_dir}' does not exist. Put your C and Headers there.")
        sys.exit(1)

    if os.path.exists(include_dir):
        remove_dir_contents(include_dir)
    else:
        os.mkdir(include_dir)

    if os.path.exists(lib_dir):
        remove_dir_contents(lib_dir)
    else:
        os.mkdir(lib_dir)

    for file in os.listdir(stdlib_dir):
        if file.endswith(".c"):
            c_path = os.path.join(stdlib_dir, file)
            o_path = c_path.replace(".c", ".o")
            os.system(f"gcc -c {c_path} -o {o_path}")
        elif file.endswith(".h"):
            h_path = os.path.join(stdlib_dir, file)
            os.system(f"cp {h_path} {include_dir}")

    lib_path = os.path.join(lib_dir, "libbased.a")
    os.system(f"ar rcs {lib_path} {stdlib_dir}/*.o")

    for file in os.listdir(stdlib_dir):
        if file.endswith(".o"):
            o_path = os.path.join(stdlib_dir, file)
            os.remove(o_path)


def transpile_based(based_path, lexer, parser):
    with open(based_path) as file:
        program = file.read()
        tokens = lexer.tokenize(program)
        result = parser.parse(tokens)

    c_path = based_path.replace(".based", ".c")
    c_path = os.path.basename(c_path)
    c_path = os.path.join("dist", c_path)
    if os.path.exists(c_path):
        os.remove(c_path)

    with open(c_path, "a") as file:
        if parser.using_arrays:
            result = f"#include <array.h>\n#include <stdlib.h>\n{result}"

        file.write(result)

    subprocess.run(["clang-format", "-i", c_path])

    for include in parser.c_includes:
        include_dir = os.path.join(os.path.dirname(based_path), include)
        include_basename = os.path.basename(include)
        dist_path = os.path.join("dist", include_basename)
        if os.path.exists(dist_path):
            os.remove(dist_path)
        os.system(f"cp {include_dir} {dist_path}")

    if len(parser.based_includes) > 0:
        include = parser.based_includes.pop()
        transpile_based(include, lexer, parser)

    return c_path


def parse_args():
    parser = argparse.ArgumentParser(prog="BasedCompiler", description="compile based source code into native machine code", epilog="")
    parser.add_argument("based_sources", metavar="BASED_SOURCE", nargs="+", help="based source files to compile")
    parser.add_argument("-o", "--output", required=True, help="output executable")
    return parser.parse_args()


def main():
    args = parse_args()

    check_files_exist(args.based_sources)

    if not os.path.exists("dist"):
        os.mkdir("dist")

    lexer = BasedLexer()
    parser = BasedParser()

    c_paths = [
        transpile_based(based_path, lexer, parser)
        for based_path in args.based_sources
    ]
    c_paths = " ".join(c_paths)

    compile_library()

    os.system(f"gcc {c_paths} -o {args.output} -Iinclude -Llib -lbased")


if __name__ == "__main__":
    main()
