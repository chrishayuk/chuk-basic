from ...lexer.token_type import TokenType
from ...ast.ast_control_flow import GosubStatement
from .base_statement_parser import BaseStatementParser

class GoSubStatementParser(BaseStatementParser):
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
        line_number = self.parser.parse_expression()

        # Return the GosubStatement
        return GosubStatement(line_number)
