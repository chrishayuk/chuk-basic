from .statement import Statement

class IfStatement(Statement):
    def __init__(self, condition, then_clause, else_clause, line_number, in_function_body=False):
        self.condition = condition
        self.then_clause = then_clause
        self.else_clause = else_clause
        self.line_number = line_number
        self.in_function_body = in_function_body

    def to_dict(self):
        return {
            "type": "IfStatement",
            "line_number": self.line_number,
            "condition": self.condition.to_dict(),
            "then_clause": self.then_clause.to_dict(),
            "else_clause": self.else_clause.to_dict() if self.else_clause else None,
            "in_function_body": self.in_function_body
        }