from .statement import Statement

class RemStatement(Statement):
    def __init__(self, comment):
        self.comment = comment