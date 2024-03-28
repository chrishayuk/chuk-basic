from ...lexer.token_type import TokenType
from ...ast.ast_control_flow import IfStatement, GotoStatement
from .base_statement_parser import BaseStatementParser

class IfStatementParser(BaseStatementParser):
    def parse(self, in_function_body=False):
        """Parse an IF statement from the token stream."""
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
        if in_function_body and self.parser.current_token.token_type == TokenType.NUMBER:
            # THEN clause is a line number within the function body
            line_number = int(self.parser.current_token.value)
            self.parser.advance()
            then_clause = GotoStatement(line_number)
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
        return IfStatement(condition, then_clause, else_clause)