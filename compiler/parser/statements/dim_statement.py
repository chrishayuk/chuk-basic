from ...lexer.token_type import TokenType
from ...ast.statements import DimStatement
from .base_statement_parser import BaseStatementParser

class DimStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past the 'DIM' token
        self.parser.advance()

        # Parse the variable
        variable = self.parser.parse_variable()

        # Parse the dimensions
        dimensions = []
        if self.parser.current_token.token_type == TokenType.LPAREN:
            self.parser.advance()  # Consume the '('
            while self.parser.current_token.token_type != TokenType.RPAREN:
                dimension = self.parser.parse_expression()
                dimensions.append(dimension)
                if self.parser.current_token.token_type == TokenType.COMMA:
                    self.parser.advance()  # Consume the ','
            self.parser.advance()  # Consume the ')'

        # Return the DIM statement
        return DimStatement(variable, dimensions)