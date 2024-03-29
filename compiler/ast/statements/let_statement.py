from .statement import Statement

class LetStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression