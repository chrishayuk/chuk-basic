from .statement import Statement

class GosubStatement(Statement):
    def __init__(self, line_number):
        self.line_number = line_number