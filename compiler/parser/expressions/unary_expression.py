from ...lexer.token_type import TokenType
from ...ast.ast_expression import UnaryExpression
from .base_expression import BaseExpressionParser
from .primary_expression import PrimaryExpressionParser

class UnaryExpressionParser(BaseExpressionParser):
    def parse(self):
        # get the current token
        token = self.parser.current_token

        # check the next token type is a +,-,!
        if token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            # advanced past the +,-.!
            self.parser.advance()

            # parse the expression
            operand = self.parser.parse_expression()

            # return a unary expression
            return UnaryExpression(token, operand)
        
        # wasn't a +, -, !, you should use the primary expression parser
        return PrimaryExpressionParser(self.parser).parse()
