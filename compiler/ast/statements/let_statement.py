from .statement import Statement

class LetStatement(Statement):
    def __init__(self, variable, expression):
        # call the base constructor
        super().__init__()

        # set the variable and expression
        self.variable = variable
        self.expression = expression

    def to_dict(self):
        return {
            "type": "LetStatement",
            "variable": self.variable.to_dict(),
            "expression": self.expression.to_dict()
        }