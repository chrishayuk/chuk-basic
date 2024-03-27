class BaseStatementParser:
    def __init__(self, parser):
        self.parser = parser

    def parse(self):
        raise NotImplementedError("Each statement parser must implement its own parse method.")
