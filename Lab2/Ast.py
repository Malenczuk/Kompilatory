class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.operator, self.right)


class UnaryExpression:
    def __init__(self, operator, operand, left=True):
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


class Function:
    def __init__(self, name, argument, ):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return "{}({})".format(self.name, self.argument)


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class If:
    def __init__(self, condition, expression, else_expression=None):
        self.condition = condition
        self.expression = expression
        self.else_expression = else_expression

    def __repr__(self):
        representation = 'IF {} THEN {}'.format(self.condition, self.expression)
        result = representation + ' ELSE {}'.format(self.else_expression) \
            if self.else_expression else representation
        return result


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.condition, self.body)


class Range:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return '{}:{}:{}'.format(self.start, self.end, self.step)


class For:
    def __init__(self, id, range, body):
        self.id = id
        self.range = range
        self.body = body

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.id, self.range, self.body)


class Break:
    def __repr__(self):
        return 'BREAK'


class Continue:
    def __repr__(self):
        return 'CONTINUE'


class Return:
    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return 'RETURN( {} )'.format(self.result)


class Print:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return 'PRINT( {} )'.format(self.expression)


class Access:
    def __init__(self, variable, key):
        self.variable = variable
        self.key = key

    def __repr__(self):
        return '{}[{}]'.format(self.variable, self.key)


class Error:
    pass


class Block:
    def __init__(self, instruction):
        self.instructions = [instruction]

    def __repr__(self):
        return "{\n" + "\n".join(map(str, self.instructions)) + "\n}"


class Program:
    def __init__(self, program):
        self.program = program

    def __repr__(self):
        return str(self.program)


class Instruction:
    def __init__(self, line):
        self.line = line

    def __repr__(self):
        return str(self.line)


class Matrix:
    def __init__(self, rows):
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


class Value:
    def __init__(self, primitive):
        self.primitive = primitive

    def __repr__(self):
        return "{}({})".format(type(self.primitive).__name__, self.primitive)


class Rows:
    def __init__(self, sequence):
        self.row_list = [sequence]

    def __repr__(self):
        return "[" + ", ".join(map(str, self.row_list)) + "]"

    def __len__(self):
        return len(self.row_list)

    def __getitem__(self, item):
        return self.row_list[item]


class Sequence:
    def __init__(self, expression):
        self.expressions = [expression]

    def __repr__(self):
        return "{}".format(self.expressions)

    def __len__(self):
        return len(self.expressions)

    def __getitem__(self, item):
        return self.expressions[item]
