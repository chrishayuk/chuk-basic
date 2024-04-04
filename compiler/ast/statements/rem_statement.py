from .statement import Statement

class RemStatement(Statement):
    def __init__(self, comment):
        # call the base constructor
        super().__init__()

        # set the comments for the rem statmeent
        self.comment = comment

    def to_dict(self):
        return {
            "type": "RemStatement",
            "comment": self.comment
        }