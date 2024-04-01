from .statement import Statement

class RemStatement(Statement):
    def __init__(self, comment):
        super().__init__()
        self.comment = comment

    def to_dict(self):
        return {
            "type": "RemStatement",
            "comment": self.comment
        }