from ...lexer.token_type import TokenType
from ...ast.ast_statement import LetStatement
from .base_statement_parser import BaseStatementParser

class LetStatementParser(BaseStatementParser):
    def parse(self):
        # Advance past the 'LET' token
        self.parser.advance()

        # Parse the variable
        variable = self.parser.parse_variable()

        # Expect an equals sign
        if self.parser.current_token.token_type != TokenType.EQ:
            raise SyntaxError("Expected '=' after variable in LET statement")
        self.parser.advance()

        # Parse the expression for the LET statement
        expression = self.parser.parse_expression()

        # Return the LET statement
        return LetStatement(variable, expression)