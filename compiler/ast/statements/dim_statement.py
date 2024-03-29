from .statement import Statement

class DimStatement(Statement):
    def __init__(self, variable, dimensions):
        self.variable = variable
        self.dimensions = dimensions