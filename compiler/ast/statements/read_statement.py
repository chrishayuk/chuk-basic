from .statement import Statement

class ReadStatement(Statement):
    def __init__(self, variables):
        self.variables = variables