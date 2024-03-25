from .ast_node import ASTNode

class Statement(ASTNode):
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in self.__dict__.items()])})"

class LetStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

class RemStatement(Statement):
    def __init__(self, comment):
        self.comment = comment

class StopStatement(Statement):
    pass

class ReturnStatement(Statement):
    pass

class EndStatement(Statement):
    pass

class InputStatement(Statement):
    def __init__(self, variable):
        self.variable = variable

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression