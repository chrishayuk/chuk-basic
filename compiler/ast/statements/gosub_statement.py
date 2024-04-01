from .statement import Statement

class GosubStatement(Statement):
    def __init__(self, target_line_number, line_number):
        super().__init__(line_number)
        self.target_line_number = target_line_number

    def to_dict(self):
        return {
            "type": "GosubStatement",
            "line_number": self.line_number,
            "target_line_number": self.target_line_number.to_dict()
        }
