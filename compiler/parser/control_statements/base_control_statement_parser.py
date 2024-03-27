class BaseControlStatementParser:
    def __init__(self, parser):
        self.parser = parser

    def parse(self):
        raise NotImplementedError("Each control flow statement parser must implement its own parse method.")
