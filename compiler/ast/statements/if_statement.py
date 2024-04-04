from .statement import Statement

class IfStatement(Statement):
    def __init__(self, condition, then_clause, else_clause, line_number, in_function_body=False):
        self.condition = condition
        self.then_clause = then_clause
        self.else_clause = else_clause
        self.line_number = line_number
        self.in_function_body = in_function_body

    def to_dict(self):
        if_dict = {
            "type": "IfStatement",
            "condition": self.condition.to_dict(),
            "thenPart": self.then_clause.to_dict(),
        }

        if self.else_clause:
            if_dict["elseClause"] = self.else_clause.to_dict()

        if self.in_function_body:
            if_dict["in_function_body"] = self.in_function_body

        return if_dict