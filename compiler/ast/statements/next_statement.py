from .statement import Statement

class NextStatement(Statement):
    def __init__(self, variable, line_number):
        super().__init__()
        self.variable = variable
        self.line_number = line_number

    def to_dict(self):
        return {
            "type": "NextStatement",
            "variable": self.variable.to_dict(),
        }