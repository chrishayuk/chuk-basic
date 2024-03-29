from ...lexer.token_type import TokenType
from ...ast.statements import ReadStatement
from .base_statement_parser import BaseStatementParser

class ReadStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past the 'READ' token
        self.parser.advance()

        # Parse the variables
        variables = []
        while self.parser.current_token is not None and self.parser.current_token.token_type != TokenType.NEWLINE:
            variable = self.parser.parse_variable()
            variables.append(variable)
            if self.parser.current_token is not None and self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()  # Consume the ','

        # Return the READ statement
        return ReadStatement(variables)