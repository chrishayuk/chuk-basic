from ...lexer.token_type import TokenType
from ...ast.variable import Variable
from ...ast.statements import DimStatement
from .base_statement_parser import BaseStatementParser

class DimStatementParser(BaseStatementParser):
    def parse(self):
        self.parser.advance()  # Skip 'DIM'
        
        # Check if the next token represents a function variable.
        if self.parser.current_token.token_type == TokenType.FN:
            # This is a function variable. Ensure the next token is an identifier.
            self.parser.advance()  # Skip 'FN'
            if self.parser.current_token is None or self.parser.current_token.token_type != TokenType.IDENTIFIER:
                raise SyntaxError("Expected function name after 'FN'")
            variable_name = f"FN{self.parser.current_token.value}"
            self.parser.advance()  # Move past the variable name.
        elif self.parser.current_token.token_type == TokenType.IDENTIFIER:
            # This is a standard variable.
            variable_name = self.parser.current_token.value
            self.parser.advance()  # Move past the variable name.
        else:
            raise SyntaxError("Expected variable name after 'DIM'")
        
        dimensions = self.expect_dimensions()

        return DimStatement(Variable(variable_name), dimensions, line_number=self.parser.line_number)
    
    def expect_dimensions(self):
        """Expect and parse the dimensions for the DIM statement."""
        dimensions = []
        if self.parser.current_token and self.parser.current_token.token_type == TokenType.LPAREN:
            self.parser.advance()  # Consume the '(' indicating the start of dimensions.
            
            while self.parser.current_token and self.parser.current_token.token_type != TokenType.RPAREN:
                dimension = self.parser.parse_expression()
                dimensions.append(dimension)
                
                if self.parser.current_token and self.parser.current_token.token_type == TokenType.COMMA:
                    self.parser.advance()  # Skip over the comma for the next dimension.
                
            if self.parser.current_token and self.parser.current_token.token_type == TokenType.RPAREN:
                self.parser.advance()  # Consume the ')' at the end of dimensions.
            else:
                raise SyntaxError("Expected ')' after dimensions")
        else:
            raise SyntaxError("Expected '(' after variable name to start dimensions")
        
        return dimensions

