from .statement import Statement

class OnStatement(Statement):
    def __init__(self, expression, line_numbers, is_gosub):
        self.expression = expression
        self.line_numbers = line_numbers
        self.is_gosub = is_gosub