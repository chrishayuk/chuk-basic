from .statement import Statement

class InputStatement(Statement):
    def __init__(self, variable):
        # call the base constructor
        super().__init__()

        # set the variable
        self.variable = variable

    def to_dict(self):
        return {
            "type": "InputStatement",
            "variable": self.variable.to_dict()
        }