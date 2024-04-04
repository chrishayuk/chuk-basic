from .statement import Statement

class NextStatement(Statement):
    def __init__(self, variable, line_number):
        # call the base constructor
        super().__init__(line_number)

        # set the variable
        self.variable = variable

    def to_dict(self):
        return {
            "type": "NextStatement",
            "variable": self.variable.to_dict(),
        }