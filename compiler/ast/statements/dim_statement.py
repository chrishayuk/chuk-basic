from .statement import Statement

class DimStatement(Statement):
    def __init__(self, variable, dimensions, line_number=None):
        # call the basic instructor
        super().__init__(line_number)

        # set the variable and dimensions
        self.variable = variable
        self.dimensions = dimensions

    def __str__(self):
        dimensions_str = ", ".join(str(dim) for dim in self.dimensions)
        return f"DimStatement({self.variable}({dimensions_str}))"