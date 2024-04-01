from ...lexer.token_type import TokenType
from ...ast.statements import GotoStatement
from .base_statement_parser import BaseStatementParser

class GotoStatementParser(BaseStatementParser):
    def parse(self):
        """Parse a GOTO statement from the token stream."""
        # Get the line number
        line_number = self.parser.line_number

        # Ensure the current token is 'GO', then advance to 'TO'
        if self.parser.current_token.token_type != TokenType.GO:
            raise SyntaxError("Expected 'GO' at the start of GOTO statement")

        # Advance past 'GO'
        self.parser.advance()

        # Check for 'TO' keyword
        if self.parser.current_token.token_type != TokenType.TO:
            raise SyntaxError("Expected 'TO' keyword after 'GO'")

        # Advance past 'TO'
        self.parser.advance()

        # Parse the line number for the GOTO
        target_line_number = self.parser.parse_expression()

        # Return the GotoStatement with the line number
        return GotoStatement(target_line_number, line_number)
