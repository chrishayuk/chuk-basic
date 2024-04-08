from ast import Expression
from typing import List
from compiler.ast.variable import Variable
from .statement import Statement
from .next_statement import NextStatement

class ForStatement(Statement):
    def __init__(self, variable: Variable, start_expression: Expression, end_expression: Expression, step_expression: Expression = None, loop_body: List[Statement] = [], next_statement: NextStatement = None, line_number: int = None):
        super().__init__()
        self.variable = variable
        self.start_expression = start_expression
        self.end_expression = end_expression
        self.step_expression = step_expression
        self.loop_body = loop_body
        self.next_statement = next_statement
        self.line_number = line_number

    def to_dict(self):
        for_dict = {
            "type": "ForStatement",
            "variable": self.variable.to_dict(),
            "start": self.start_expression.to_dict() if self.start_expression else None,
            "end": self.end_expression.to_dict(),
            "step": self.step_expression.to_dict() if self.step_expression else None,
            "body": [
                {
                    "line_number": stmt.line_number,
                    "statements": [stmt.to_dict()]
                } for stmt in self.loop_body
            ],
            "next": {
                "line_number": self.next_statement.line_number,
                "statement": self.next_statement.to_dict()
            }
        }

        return for_dict

    def to_statements(self):
        """Convert the FOR loop into a list of separate statements."""
        statements = []

        # Add the ForStatement itself
        statements.append({
            'line_number': self.line_number,
            'statement': self
        })

        # # Add the loop body statements
        # for stmt in self.loop_body:
        #     statements.append({
        #         'line_number': stmt.line_number,
        #         'statement': stmt
        #     })

        # # Add the NextStatement
        # statements.append({
        #     'line_number': self.next_statement.line_number,
        #     'statement': self.next_statement
        # })

        return statements