from ...lexer.token_type import TokenType
from ...ast.expressions import UnaryExpression, Literal
from .base_expression import BaseExpressionParser
from .primary_expression import PrimaryExpressionParser

class UnaryExpressionParser(BaseExpressionParser):
    def parse(self):
        token = self.parser.current_token

        # Check if the token is a unary operator (+, -, !)
        if token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            operator = token
            self.parser.advance()

            operand = self.parser.parse_expression()

            # Special case: If the operator is '-' and the operand is a Literal, negate the value
            if operator.token_type == TokenType.MINUS and isinstance(operand, Literal):
                return Literal(-operand.value)
            else:
                return UnaryExpression(operator, operand)

        # If not a unary operator, parse as a primary expression
        return PrimaryExpressionParser(self.parser).parse()