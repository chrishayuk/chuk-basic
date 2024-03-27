from ...lexer.token_type import TokenType
from ...ast.ast_control_flow import GotoStatement
from .base_control_statement_parser import BaseControlStatementParser
from ..expression_parser import parse_expression

class GoToStatementParser(BaseControlStatementParser):
    def parse(self):
        """Parse a GOTO statement from the token stream."""

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
        line_number = parse_expression(self.parser)

        # Return the GotoStatement
        return GotoStatement(line_number)
