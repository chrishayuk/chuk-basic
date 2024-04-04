from .statement import Statement

class FnEndStatement(Statement):
    def __init__(self, line_number):
        # call the base constructor
        super().__init__(line_number)

    def __str__(self):
        return "FNEND"

    def to_dict(self):
        return {
            "type": "FnEndStatement",
            "line_number": self.line_number
        }