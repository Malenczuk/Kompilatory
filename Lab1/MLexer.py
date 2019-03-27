#!/usr/bin/python

import ply.lex as lex


class MLexer:

    newlines = [0]

    def __init__(self):
        self.lexer = lex.lex(object=self)
        self.result = []

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    def run(self, s):
        self.lexer.input(s)
        for token in self.lexer:
            self.result.append(token)

    def print_result(self):
        print(self.show_result())

    def show_result(self):
        result = ""
        for token in self.result:
            result += self.show_token(token) + "\n"
        return result

    def show_token(self, token):
        return "(%d, %d): %s(%s)" % (
            token.lineno,
            MLexer.get_column(token),
            token.type,
            token.value
        )

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

    tokens = [
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'DOTPLUS',
                 'DOTMINUS',
                 'DOTTIMES',
                 'DOTDIVIDE',
                 'ASSIGN',
                 'PLUSASSIGN',
                 'MINUSASSIGN',
                 'TIMESASSIGN',
                 'DIVIDEASSIGN',
                 'LESS',
                 'MORE',
                 'LESSEQUAL',
                 'MOREEQUAL',
                 'INEQUAL',
                 'EQUAL',
                 'LPAREN',
                 'RPAREN',
                 'LBRACKET',
                 'RBRACKET',
                 'LCURLY',
                 'RCURLY',
                 'COLON',
                 'TRANSPOSE',
                 'COMMA',
                 'SEMICOLON',
                 'ID',
                 'INT',
                 'FLOAT',
                 'STRING'
             ] + list(reserved.values())

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_DOTPLUS = r'\.\+'
    t_DOTMINUS = r'\.-'
    t_DOTTIMES = r'\.\*'
    t_DOTDIVIDE = r'\./'
    t_ASSIGN = r'='
    t_PLUSASSIGN = r'\+='
    t_MINUSASSIGN = r'-='
    t_TIMESASSIGN = r'\*='
    t_DIVIDEASSIGN = r'/='
    t_LESS = r'<'
    t_MORE = r'>'
    t_LESSEQUAL = r'<='
    t_MOREEQUAL = r'>='
    t_INEQUAL = r'!='
    t_EQUAL = r'=='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_COLON = r':'
    t_TRANSPOSE = r'\''
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_STRING = r'"([^\\\n]|(\\.))*?"'

    t_ignore = ' \t'
    t_ignore_COMMENT = r'\#.*'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_FLOAT(self, t):
        r"([0-9]+)(\.)([0-9]+)?|(\.)([0-9]+)"
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        MLexer.add_newline(t)

    def t_error(self, t):
        print("illegal character '%s' at (%d, %d)" %
              (t.value[0], t.lineno, self.get_column(t)))
        t.lexer.skip(1)

    @staticmethod
    def get_column(t):
        # Lines start at 1 not 0
        return (t.lexpos - MLexer.newlines[t.lineno - 1]) + 1

    @staticmethod
    def get_position(t):
        return t.lineno, MLexer.get_column(t)

    @staticmethod
    def add_newline(t):
        for i in range(len(t.value)):
            MLexer.newlines.append(t.lexpos + i)
