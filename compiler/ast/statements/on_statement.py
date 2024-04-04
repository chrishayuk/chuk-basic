from .statement import Statement

class OnStatement(Statement):
    def __init__(self, expression, line_numbers, is_gosub, line_number):
        # call the base constructor
        super().__init__(line_number)

        # set expression, line numbers and whether goto or gosub
        self.expression = expression
        self.line_numbers = line_numbers
        self.is_gosub = is_gosub

    def to_dict(self):
        return {
            "type": "OnGosubStatement" if self.is_gosub else "OnGotoStatement",
            "line_number": self.line_number,
            "expression": self.expression.to_dict(),
            "line_numbers": [line_number.to_dict() for line_number in self.line_numbers]
        }