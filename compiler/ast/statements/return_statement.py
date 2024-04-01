from .statement import Statement

class ReturnStatement(Statement):
    def __init__(self, expression=None):
        super().__init__()
        self.expression = expression

    def to_dict(self):
        return {
            "type": "ReturnStatement",
            "expression": self.expression.to_dict() if self.expression else None
        }