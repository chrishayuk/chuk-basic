from .statement import Statement

class ReturnStatement(Statement):
    def __init__(self, expression=None):
        # call the base constructor
        super().__init__()

        # set the expression
        self.expression = expression

    def to_dict(self):
        return {
            "type": "ReturnStatement",
            "expression": self.expression.to_dict() if self.expression else None
        }