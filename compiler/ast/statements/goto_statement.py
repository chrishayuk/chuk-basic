from .statement import Statement

class GotoStatement(Statement):
    def __init__(self, target_line_number, line_number):
        super().__init__(line_number)
        self.target_line_number = target_line_number

    def to_dict(self):
        return {
            "type": "GotoStatement",
            "target": int(self.target_line_number.value),
        }