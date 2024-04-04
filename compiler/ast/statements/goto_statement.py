from .statement import Statement

class GotoStatement(Statement):
    def __init__(self, target_line_number, line_number):
        # call the base constructor
        super().__init__(line_number)

        # set the target line number
        self.target_line_number = target_line_number

    def to_dict(self):
        return {
            "type": "GotoStatement",
            "target": int(self.target_line_number.value),
        }