class Node(object):
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        super().__init__(self.__class__, [left, right], operator)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class UnaryExpression(Node):
    def __init__(self, operator, operand, left=True):
        super().__init__(self.__class__, [operand], operator)
        self.operator = operator
        self.operand = operand
        self.left = left

    def __repr__(self):
        order = [self.operator, self.operand] if self.left else [self.operand, self.operator]
        return '{}{}'.format(*order)


class Negation(UnaryExpression):
    def __init__(self, operand):
        super().__init__('-', operand)


class Transposition(UnaryExpression):
    def __init__(self, operand):
        super().__init__('\'', operand, False)


class Assignment(BinaryExpression):
    pass


class Function(Node):
    def __init__(self, name, argument):
        super().__init__(self.__class__, [argument], name)
        self.name = name
        self.argument = argument

    def __repr__(self):
        return "{}({})".format(self.name, self.argument)


class Variable(Node):
    def __init__(self, name):
        super().__init__(self.__class__, [], name)
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class If(Node):
    def __init__(self, condition, expression, else_expression=None):
        super().__init__(self.__class__, [condition, expression, else_expression], ["IF", "THEN", "ELSE"])
        self.condition = condition
        self.expression = expression
        self.else_expression = else_expression
        if else_expression == None:
            self.children = self.children[:-1]
            self.leaf = self.leaf[:-1]

    def __repr__(self):
        representation = 'IF {} THEN {}'.format(self.condition, self.expression)
        result = representation + ' ELSE {}'.format(self.else_expression) \
            if self.else_expression else representation
        return result


class While(Node):
    def __init__(self, condition, body):
        super().__init__(self.__class__, [condition, body], "WHILE")
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class Range(Node):
    def __init__(self, start, end, step=1):
        super().__init__(self.__class__, [start, end, step], "RANGE")
        if step == 1: self.children = self.children[:-1]
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return '{}:{}:{}'.format(self.start, self.end, self.step)


class For(Node):
    def __init__(self, id, range, body):
        super().__init__(self.__class__, [id, range, body], "FOR")
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class Break(Node):
    def __init__(self):
        super().__init__(self.__class__, [], "BREAK")

    def __repr__(self):
        return 'BREAK'


class Continue(Node):
    def __init__(self):
        super().__init__(self.__class__, [], "CONTINUE")

    def __repr__(self):
        return 'CONTINUE'


class Return(Node):
    def __init__(self, result):
        super().__init__(self.__class__, [result], "RETURN")
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print(Node):
    def __init__(self, expression):
        super().__init__(self.__class__, [expression], "PRINT")
        self.expression = expression

    def __repr__(self):
        return 'PRINT( {} )'.format(self.expression)


class Access(Node):
    def __init__(self, variable, key):
        super().__init__(self.__class__, [variable, key], "REF")
        self.variable = variable
        self.key = key

    def __repr__(self):
        return '{}[{}]'.format(self.variable, self.key)


class Error(Node):
    pass


class Block(Node):
    def __init__(self, instruction):
        super().__init__(self.__class__, [instruction])
        self.instructions = self.children

    def __repr__(self):
        return "{\n" + "\n".join(map(str, self.instructions)) + "\n}"


class Program(Node):
    def __init__(self, program):
        super().__init__(self.__class__, [program])
        self.program = program

    def __repr__(self):
        return str(self.program)


class Instruction(Node):
    def __init__(self, line):
        super().__init__(self.__class__, [line])
        self.line = line

    def __repr__(self):
        return str(self.line)


class Matrix(Node):
    def __init__(self, rows):
        super().__init__(self.__class__, [rows], "MATRIX")
        self.dims = len(rows), len(rows[0])
        self.rows = rows

    def __repr__(self):
        return str(self.rows)

    def has_correct_dims(self):
        sizes = list(map(len, self.rows))
        return not sizes or sizes.count(sizes[0]) == len(sizes)

    def dims_compatible(self, other):
        if type(other) is not Matrix:
            return False
        return self.dims == other.dims


class Value(Node):
    def __init__(self, primitive):
        super().__init__(self.__class__, [], primitive)
        self.primitive = primitive

    def __repr__(self):
        return "{}({})".format(type(self.primitive).__name__, self.primitive)


class Rows(Node):
    def __init__(self, sequence):
        super().__init__(self.__class__, [sequence])
        self.row_list = self.children

    def __repr__(self):
        return "[" + ", ".join(map(str, self.row_list)) + "]"

    def __len__(self):
        return len(self.row_list)

    def __getitem__(self, item):
        return self.row_list[item]


class Sequence(Node):
    def __init__(self, expression):
        super().__init__(self.__class__, [expression], "SEQ")
        self.expressions = self.children

    def __repr__(self):
        return "{}".format(self.expressions)

    def __len__(self):
        return len(self.expressions)

    def __getitem__(self, item):
        return self.expressions[item]
