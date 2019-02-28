#!/usr/bin/python

import Lab1.scanner as scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    # to fill ...
    ("left", '+', '-'),
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


# to finish the grammar
# ....


parser = yacc.yacc()
