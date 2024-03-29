from .statement import Statement

class InputStatement(Statement):
    def __init__(self, variable):
        self.variable = variable