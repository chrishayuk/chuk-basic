import decimal
from .expression import Expression

class Literal(Expression):
    def __init__(self, value):
        try:
            self.value = decimal.Decimal(value)
        except (ValueError, decimal.InvalidOperation):
            self.value = value

    def __str__(self):
        return str(self.value)