from .statement import Statement

class PrintStatement(Statement):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def to_dict(self):
        if isinstance(self.expression, list):
            return {
                "type": "PrintStatement",
                "expressions": [expr.to_dict() for expr in self.expression]
            }
        else:
            return {
                "type": "PrintStatement",
                "expression": self.expression.to_dict()
            }