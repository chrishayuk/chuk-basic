from .statement import Statement

class InputStatement(Statement):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def to_dict(self):
        return {
            "type": "InputStatement",
            "variable": self.variable.to_dict()
        }