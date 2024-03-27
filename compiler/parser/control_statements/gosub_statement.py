from ...lexer.token_type import TokenType
from ...ast.ast_control_flow import GosubStatement
from .base_control_statement_parser import BaseControlStatementParser
from ..expression_parser import parse_expression

class GoSubStatementParser(BaseControlStatementParser):
    def parse(self):
        """Parse a GOSUB statement from the token stream."""

        # Ensure the current token is 'GO', then advance to 'SUB'
        if self.parser.current_token.token_type != TokenType.GO:
            raise SyntaxError("Expected 'GO' at the start of GOSUB statement")
        
        # Advance past 'GO'
        self.parser.advance()

        # Check for 'SUB' keyword
        if self.parser.current_token.token_type != TokenType.SUB:
            raise SyntaxError("Expected 'SUB' keyword after 'GO'")
        
        # Advance past 'SUB'
        self.parser.advance()

        # Parse the line number for the GOSUB
        line_number = parse_expression(self.parser)

        # Return the GosubStatement
        return GosubStatement(line_number)
