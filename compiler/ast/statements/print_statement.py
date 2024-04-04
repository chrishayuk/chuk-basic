from .statement import Statement

class PrintStatement(Statement):
    def __init__(self, expression):
        # call the base constructor
        super().__init__()

        # set the expression
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