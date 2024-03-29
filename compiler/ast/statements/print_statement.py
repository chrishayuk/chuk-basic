from .statement import Statement

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression