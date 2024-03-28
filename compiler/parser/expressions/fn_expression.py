from ...lexer.token_type import TokenType
from ...ast.ast_node import Variable
from ...ast.ast_expression import FnExpression, BinaryExpression
from .base_expression import BaseExpressionParser
from .builtin_functions import BuiltinFunctionParser, BUILTIN_FUNCTIONS

class FnExpressionParser(BaseExpressionParser):
    def parse(self):
        # Advance past the FN keyword
        self.parser.advance()

        # Check if the function name is a built-in function
        if self.parser.current_token and self.parser.current_token.token_type == TokenType.IDENTIFIER:
            function_name = self.parser.current_token.value.upper()
            if function_name in BUILTIN_FUNCTIONS:
                left_expression = BuiltinFunctionParser(self.parser).parse()
            else:
                left_expression = self.parse_user_defined_function()
        else:
            raise SyntaxError("Expected function name after FN keyword")

        # Check if there is a binary operator after the function call
        if self.parser.current_token and self.parser.current_token.token_type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POW,
            TokenType.AND, TokenType.OR,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE
        ]:
            operator = self.parser.current_token
            self.parser.advance()
            right_expression = self.parser.parse_expression()
            return BinaryExpression(operator, left_expression, right_expression)

        # If no binary operator, return the FnExpression
        return left_expression

    def parse_user_defined_function(self):
        # Expect the function name
        if not self.parser.current_token or self.parser.current_token.token_type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function name after FN keyword")

        # Get the function name and skip past it
        function_name = Variable(self.parser.current_token.value)
        self.parser.advance()

        # Get the left parenthesis
        if not self.parser.current_token or self.parser.current_token.token_type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after function name in FN expression")
        self.parser.advance()

        arguments = []
        # Loop until we get the right parenthesis
        while self.parser.current_token and self.parser.current_token.token_type != TokenType.RPAREN:
            # Parse the expression
            expression = self.parser.parse_expression()
            arguments.append(expression)

            # Loop through commas
            if self.parser.current_token and self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()  # Consume the ','
            elif self.parser.current_token and self.parser.current_token.token_type != TokenType.RPAREN:
                raise SyntaxError("Expected ',' or ')' in argument list of FN expression")

        # Skip past the right parenthesis
        if self.parser.current_token:
            self.parser.advance()

        # Return the function expression
        return FnExpression(function_name, arguments)