from .statement import Statement

class DimStatement(Statement    ):
    def __init__(self, variable, dimensions, line_number=None):
        self.variable = variable
        self.dimensions = dimensions
        self.line_number = line_number

    def __str__(self):
        dimensions_str = ", ".join(str(dim) for dim in self.dimensions)
        return f"DimStatement({self.variable}({dimensions_str}))"