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

class RemStatement(Statement):
    def __init__(self, comment):
        self.comment = comment

class StopStatement(Statement):
    pass

class IfStatement(Statement):
    def __init__(self, condition, then_statement, else_statement):
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

class ForStatement(Statement):
    def __init__(self, variable, start_expression, end_expression, step_expression):
        self.variable = variable
        self.start_expression = start_expression
        self.end_expression = end_expression
        self.step_expression = step_expression

class GotoStatement(Statement):
    def __init__(self, line_number):
        self.line_number = line_number

class GosubStatement(Statement):
    def __init__(self, line_number):
        self.line_number = line_number

class ReturnStatement(Statement):
    pass

class InputStatement(Statement):
    def __init__(self, variable):
        self.variable = variable

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