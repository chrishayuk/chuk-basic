from .statement import Statement

class EndStatement(Statement):
    def __init__(self):
        # call the base constructor
        super().__init__()

    def to_dict(self):
        return {
            "type": "EndStatement"
        }