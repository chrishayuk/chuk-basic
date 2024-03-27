class BaseExpressionParser:
    def __init__(self, parser):
        self.parser = parser

    def parse(self):
        raise NotImplementedError("Each subclass must implement its own parse method.")
