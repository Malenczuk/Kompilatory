#!/usr/bin/python

import ply.yacc as yacc
import Lab2.Ast as ast
from Lab2.MLexer import MLexer


class MParser:
    tokens = MLexer.tokens

    def __init__(self):
        self.parser = None
        self.matrix_lexer = MLexer()
        self.symtab = {}
        self.error = False

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self)

    def run(self, s, **kwargs):
        self.build(**kwargs)
        return self.parser.parse(s, lexer=self.matrix_lexer.lexer)

    precedence = (
        ('nonassoc', 'IF'),
        ('nonassoc', 'LESS', 'MORE', 'EQUAL', 'INEQUAL', 'LESSEQUAL', 'MOREEQUAL', 'ELSE'),
        ('left', 'PLUS', 'MINUS', 'DOTPLUS', 'DOTMINUS'),
        ('left', 'TIMES', 'DIVIDE', 'DOTTIMES', 'DOTDIVIDE'),
        ('left', 'UMINUS'),
        ('nonassoc', 'TRANSPOSE')
    )

    def p_program(self, p):
        """program : block"""
        p[0] = ast.Program(p[1])

    def p_block_curly(self, p):
        """
        block : block LCURLY block RCURLY
              | LCURLY block RCURLY
        """
        if len(p) == 5:
            p[1].instructions.append(p[3])
            p[0] = p[1]
        else:
            p[0] = ast.Block(p[2])

    def p_block(self, p):
        """
        block : block instruction
              | instruction
        """
        if len(p) == 3:
            p[1].instructions.append(p[2])
            p[0] = p[1]
        else:
            p[0] = ast.Block(p[1])

    def p_instruction(self, p):
        """
        instruction : statement SEMICOLON
                    | if_statement
                    | while_statement
                    | for_statement
        """
        p[0] = p[1]

    def p_statement(self, p):
        """
        statement : assignment
                  | keyword
        """
        p[0] = ast.Instruction(p[1])

    def p_assignment(self, p):
        """
        assignment : variable assignment_operator expression
        """
        p[0] = ast.Assignment(p[1], p[2], p[3])

    def p_variable(self, p):
        """
        variable : ID
                 | access
        """
        p[0] = ast.Variable(p[1])

    def p_access(self, p):
        """
        access : ID LBRACKET sequence RBRACKET
        """
        p[0] = ast.Access(p[1], p[3])

    def p_sequence(self, p):
        """
        sequence : sequence COMMA expression
                 | expression
        """
        if len(p) == 4:
            p[1].expressions.append(p[3])
            p[0] = p[1]
        else:
            p[0] = ast.Sequence(p[1])

    def p_value(self, p):
        """
        value : FLOAT
              | INT
              | STRING
              | matrix
              | access
        """

        p[0] = ast.Value(p[1])

    def p_matrix(self, p):
        """
        matrix : LBRACKET rows RBRACKET
        """
        p[0] = ast.Matrix(p[2])

    def p_rows(self, p):
        """
        rows : rows SEMICOLON sequence
        """
        p[1].row_list.append(p[3])
        p[0] = p[1]

    def p_row(self, p):
        """
        rows : sequence
        """
        p[0] = ast.Rows(p[1])

    def p_expression_value(self, p):
        """
        expression : value
        """
        p[0] = p[1]

    def p_expression_id(self, p):
        """expression : ID"""
        p[0] = ast.Variable(p[1])

    def p_expression_minus(self, p):
        """
        expression : MINUS expression %prec UMINUS
        """
        p[0] = ast.Negation(p[2])

    def p_id_transpose(self, p):
        """
        expression : ID TRANSPOSE
        """
        p[0] = ast.Transposition(ast.Variable(p[1]))

    def p_expression_transpose(self, p):
        """
        expression : LPAREN expression RPAREN TRANSPOSE
        """
        p[0] = ast.Transposition(p[2])

    def p_expression_paren(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        p[0] = p[2]

    def p_expression_math(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression DOTPLUS expression
                   | expression DOTMINUS expression
                   | expression DOTTIMES expression
                   | expression DOTDIVIDE expression
        """
        p[0] = ast.BinaryExpression(p[1], p[2], p[3])

    def p_expression_fun(self, p):
        """
        expression : function LPAREN expression RPAREN
                   | function LPAREN sequence RPAREN
        """
        p[0] = ast.Function(p[1], p[3])

    def p_keyword_print(self, p):
        """
        keyword : PRINT sequence
        """
        p[0] = ast.Print(p[2])

    def p_keyword_break(self, p):
        """
        keyword : BREAK
        """
        p[0] = ast.Break()

    def p_keyword_continue(self, p):
        """
        keyword : CONTINUE
        """
        p[0] = ast.Continue()

    def p_keyword_return(self, p):
        """
        keyword : RETURN expression
        """
        p[0] = ast.Return(p[2])

    def p_relation(self, p):
        """relation : expression comparison_operator expression"""
        p[0] = ast.BinaryExpression(p[1], p[2], p[3])

    def p_body(self, p):
        """body : instruction"""
        p[0] = ast.Instruction(p[1])

    def p_body_curly(self, p):
        """body : LCURLY block RCURLY"""
        p[0] = ast.Instruction(p[2])

    def p_if_statement(self, p):
        """
        if_statement : IF LPAREN relation RPAREN body %prec IF
        """
        p[0] = ast.If(p[3], p[5])

    def p_if_else_statement(self, p):
        """
        if_statement : IF LPAREN relation RPAREN body ELSE body
        """
        p[0] = ast.If(p[3], p[5], p[7])

    def p_while_statement(self, p):
        """while_statement : WHILE LPAREN relation RPAREN body"""
        p[0] = ast.While(p[3], p[5])

    def p_for_statement(self, p):
        """for_statement : FOR ID ASSIGN range body"""
        p[0] = ast.For(p[2], p[4], p[5])

    def p_range(self, p):
        """range : expression COLON expression"""
        p[0] = ast.Range(p[1], p[3])

    def p_range_step(self, p):
        """
         range : expression COLON expression COLON expression
        """
        p[0] = ast.Range(p[1], p[3], p[5])

    def p_assignment_operator(self, p):
        """
        assignment_operator : ASSIGN
                            | PLUSASSIGN
                            | MINUSASSIGN
                            | TIMESASSIGN
                            | DIVIDEASSIGN
        """
        p[0] = p[1]

    def p_comparision_operator(self, p):
        """
        comparison_operator : LESS
                             | MORE
                             | EQUAL
                             | INEQUAL
                             | LESSEQUAL
                             | MOREEQUAL
        """
        p[0] = p[1]

    def p_function(self, p):
        """
        function : EYE
                 | ZEROS
                 | ONES
        """
        p[0] = p[1]

    def p_error(self, p):
        self.error = True
        if p:
            line = p.lexer.lineno if hasattr(p.lexer, 'lineno') else p.lexer.lexer.lineno
            value = p.value
        else:
            line = 'last'
            value = ''
        print('/' * 40 + '\nERROR\nIllegal symbol {} at line {}\n'.format(value, line) + '/' * 40)
