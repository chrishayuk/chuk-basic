from ast import Expression
from typing import List
from compiler.ast.variable import Variable
from ...lexer.token_type import TokenType
from ..expressions.binary_expression import BinaryExpression
from .let_statement import LetStatement
from .if_statement import IfStatement
from .goto_statement import GotoStatement
from .statement import Statement
from .next_statement import NextStatement  # Import NextStatement here

class ForStatement(Statement):
    def __init__(self, variable: Variable, start_expression: Expression, end_expression: Expression, step_expression: Expression, loop_body: List[Statement], next_statement: NextStatement, line_number: int):
        super().__init__()
        self.variable = variable
        self.start_expression = start_expression
        self.end_expression = end_expression
        self.step_expression = step_expression
        self.loop_body = loop_body
        self.next_statement = next_statement
        self.line_number = line_number

    def to_statements(self):
        """Convert the FOR loop into a list of separate statements."""
        statements = []

        # Add the ForStatement itself
        statements.append({
            'line_number': self.line_number,
            'statement': self
        })

        # Add the loop body statements
        for stmt in self.loop_body:
            statements.append({
                'line_number': stmt.line_number,
                'statement': stmt
            })

        # Add the NextStatement
        statements.append({
            'line_number': self.next_statement.line_number,
            'statement': self.next_statement
        })

        return statements
    
class NextStatement(Statement):
    def __init__(self, variable, line_number):
        self.variable = variable
        self.line_number = line_number