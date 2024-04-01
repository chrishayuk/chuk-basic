from compiler.ast.expressions.literal_expression import Literal
from ...lexer.token_type import TokenType
from ...ast.statements import IfStatement, GotoStatement
from .base_statement_parser import BaseStatementParser

class IfStatementParser(BaseStatementParser):
    def parse(self, in_function_body=False):
        """Parse an IF statement from the token stream."""
        # Get the current line number
        line_number = self.parser.line_number

        # Advance past the 'IF' token
        self.parser.advance()

        # Parse the condition
        condition = self.parser.parse_expression()

        # Expect and skip the 'THEN' keyword
        if self.parser.current_token.token_type != TokenType.THEN:
            raise SyntaxError(f"Expected 'THEN' keyword after condition, but got '{self.parser.current_token.value}'")

        # Advance past 'THEN'
        self.parser.advance()

        # Parse the THEN clause
        if self.parser.current_token.token_type == TokenType.NUMBER:
            # THEN clause is a line number
            target_line_number = int(self.parser.current_token.value)
            self.parser.advance()
            then_clause = GotoStatement(Literal(target_line_number), line_number)
        else:
            # THEN clause is a statement
            then_clause = self.parser.parse_statement()

        if then_clause is None:
            raise SyntaxError("Expected a statement after 'THEN' keyword")

        # Initialize else_clause as None
        else_clause = None

        # Check for an 'ELSE' clause and parse the ELSE statement if present
        if self.parser.current_token and self.parser.current_token.token_type == TokenType.ELSE:
            # Advance past 'ELSE'
            self.parser.advance()

            # Parse the statement following 'ELSE'
            else_clause = self.parser.parse_statement()

            # Check for an else statement
            if else_clause is None:
                raise SyntaxError("Expected a statement after 'ELSE' keyword")

        # Return the constructed IfStatement
        if in_function_body:
            return IfStatement(condition, then_clause, else_clause, line_number, in_function_body=True)
        else:
            return IfStatement(condition, then_clause, else_clause, line_number)