from .ast_node import ASTNode

class Expression(ASTNode):
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items()])})"

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(Expression):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class Literal(Expression):
    def __init__(self, value):
        self.value = value

class FnExpression(Expression):
    def __init__(self, name, argument, body):
        self.name = name
        self.argument = argument
        self.body = body