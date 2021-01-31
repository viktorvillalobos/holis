# -*- coding: utf-8 -*-
import argparse
import ast
import platform
import sys
import traceback


class PrintVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.print_visited = False

    def found_print_statement(self, lineno, col_offset, is_function):
        self.print_visited = True
        statement = "print" if is_function else "print (legacy)"
        print(
            "{}:{}:{} found {} call".format(
                self.filename, lineno, col_offset, statement
            )
        )

    def visit_Print(self, node):
        self.found_print_statement(node.lineno, node.col_offset, False)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.found_print_statement(node.lineno, node.col_offset, True)
        self.generic_visit(node)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, "rb") as f:
                visitor = PrintVisitor(filename)
                visitor.visit(ast.parse(f.read(), filename=filename))
                if visitor.print_visited:
                    retval = 1
        except SyntaxError:
            print(
                "{}: failed parsing with {} {}:".format(
                    filename,
                    platform.python_implementation(),
                    sys.version.partition(" ")[0],
                )
            )
            print(
                "\n{}".format("    " + traceback.format_exc().replace("\n", "\n    "))
            )
            retval = 1
    return retval


if __name__ == "__main__":
    exit(main())
