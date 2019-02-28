#!/usr/bin/python

import ply.lex as lex
import ply.yacc as yacc

symtab = {}

literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '=', '<', '>', ':', '\'', ',', ';']

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT',
}

tokens = ["REAL_NUMBER", "NUMBER", 'ID', 'STRING',
          "DOTADD", "DOTSUB", "DOTMUL", "DOTDIV",
          "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN",
          "LEQ", "GEQ", "NEQ", "EQ",
          ] + list(reserved.values())

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    #    line = t.value.lstrip()
    #    i = line.find("\n")
    #    line = line if i == -1 else line[:i]
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


def t_COMMENT(t):
    r'\#.*'
    pass

def t_STRING(t):
    r"\"([^\\']+|\\'|\\\\)*\""
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_REAL_NUMBER(t):
    r"([0-9]+)(\.)([0-9]+)?|(\.)([0-9]+)"
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
