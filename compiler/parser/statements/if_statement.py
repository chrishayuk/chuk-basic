from ...lexer.token_type import TokenType
from ...ast.ast_control_flow import IfStatement
from .base_statement_parser import BaseStatementParser

class IfStatementParser(BaseStatementParser):
    def parse(self):
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

        # Parse the THEN statement (expecting a single statement)
        then_statement = self.parser.parse_statement()
        if then_statement is None:
            raise SyntaxError("Expected a statement after 'THEN' keyword")

        # Initialize else_statement as None
        else_statement = None

        # Check for an 'ELSE' clause and parse the ELSE statement if present
        if self.parser.current_token and self.parser.current_token.token_type == TokenType.ELSE:
            # Advance past 'ELSE'
            self.parser.advance()

            # Parse the statement following 'ELSE'
            else_statement = self.parser.parse_statement()

            # check for an else statement
            if else_statement is None:
                raise SyntaxError("Expected a statement after 'ELSE' keyword")

        # Return the constructed IfStatement
        return IfStatement(condition, then_statement, else_statement)
