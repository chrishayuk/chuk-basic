from .statement import Statement

class FnEndStatement(Statement):
    def __init__(self, line_number):
        super().__init__()
        self.line_number = line_number

    def __str__(self):
        return "FNEND"

    def to_dict(self):
        return {
            "type": "FnEndStatement",
            "line_number": self.line_number
        }