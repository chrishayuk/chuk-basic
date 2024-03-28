from ...ast.ast_expression import BinaryExpression, Expression, FnExpression
from ...lexer.token_type import TokenType
from .base_expression import BaseExpressionParser
from .primary_expression import PrimaryExpressionParser

class BinaryExpressionParser(BaseExpressionParser):
    def __init__(self, parser):
        super().__init__(parser)
    
    def parse(self, left_expression=None, precedence=0):
        if left_expression is None:
            left_expression = self.parse_primary_expression()

        while self.parser.current_token and self.get_operator_precedence(self.parser.current_token.token_type) > precedence:
            # Check if the left expression is a function expression followed by a binary operator
            if isinstance(left_expression, FnExpression):
                left_expression = self.parse_function_expression_with_binary_operator(left_expression, precedence)
            else:
                # get the operator token and skip past it
                op_token = self.parser.current_token
                self.parser.advance()

                # parse the right expression
                right_expression = self.parse_primary_expression()

                # handle the precedence and get the right expression
                while self.parser.current_token and self.get_operator_precedence(self.parser.current_token.token_type) > self.get_operator_precedence(op_token.token_type):
                    right_expression = self.parse(right_expression, self.get_operator_precedence(op_token.token_type))

                # parse the left expression
                left_expression = BinaryExpression(left_expression, op_token, right_expression)

        return left_expression

    def parse_function_expression_with_binary_operator(self, function_expression, precedence):
        while self.parser.current_token and self.get_operator_precedence(self.parser.current_token.token_type) > precedence:
            op_token = self.parser.current_token
            self.parser.advance()
            right_expression = self.parse_primary_expression()

            while self.parser.current_token and self.get_operator_precedence(self.parser.current_token.token_type) > self.get_operator_precedence(op_token.token_type):
                right_expression = self.parse(right_expression, self.get_operator_precedence(op_token.token_type))

            new_left_expression = BinaryExpression(function_expression, op_token, right_expression)
            function_expression = new_left_expression

        return function_expression

    def get_operator_precedence(self, token_type: TokenType) -> int:
        # Precedence values for operators.
        precedences = {
            TokenType.OR: 1,
            TokenType.AND: 2,
            TokenType.EQ: 3, TokenType.NE: 3,
            TokenType.LT: 4, TokenType.LE: 4, TokenType.GT: 4, TokenType.GE: 4,
            TokenType.PLUS: 5, TokenType.MINUS: 5,
            TokenType.MUL: 6, TokenType.DIV: 6,
            TokenType.POW: 7,
        }
        return precedences.get(token_type, 0)

    def parse_primary_expression(self):
        # Direct call to parse a primary expression.
        return PrimaryExpressionParser(self.parser).parse()

