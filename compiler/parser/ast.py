from ..lexer.token_type import TokenType

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Statement(ASTNode):
    pass

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class LetStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

class Expression(ASTNode):
    pass

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

class Variable(Expression):
    def __init__(self, name):
        self.name = name