from .statement import Statement

class StopStatement(Statement):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "type": "StopStatement"
        }