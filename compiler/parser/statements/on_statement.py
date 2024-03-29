from ...lexer.token_type import TokenType
from ...ast.statements import OnStatement
from .base_statement_parser import BaseStatementParser

class OnStatementParser(BaseStatementParser):
    def parse(self):
        """Parse an ON statement from the token stream."""

        # Advance past 'ON'
        self.parser.advance()  

        # Parse the controlling expression
        expression = self.parser.parse_expression()

        # Look ahead to ensure correct handling of 'GOTO' or 'GOSUB'
        if not (self.parser.current_token and self.parser.current_token.token_type == TokenType.GO):
            raise SyntaxError("Expected 'GO' keyword after expression in ON statement")
        
        # Advance past 'GO'
        self.parser.advance()  

        # Now check if it's GOTO or GOSUB
        if self.parser.current_token.token_type == TokenType.TO:
            is_gosub = False
        elif self.parser.current_token.token_type == TokenType.SUB:
            is_gosub = True
        else:
            raise SyntaxError("Expected 'TO' or 'SUB' keyword after 'GO' in ON statement")
        
        # Advance past 'TO' or 'SUB'
        self.parser.advance()  

        # Parse the line numbers as targets
        line_numbers = []
        while self.parser.current_token and self.parser.current_token.token_type == TokenType.NUMBER:
            line_number = self.parser.current_token.value
            line_numbers.append(line_number)

            # Advance past line number
            self.parser.advance()  
            
            if self.parser.current_token and self.parser.current_token.token_type == TokenType.COMMA:
                # Skip comma for next line number
                self.parser.advance()  
            else:
                break  # End of line numbers

        return OnStatement(expression, line_numbers, is_gosub)

