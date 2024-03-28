from ...ast.ast_node import Variable
from ...ast.ast_expression import FnExpression
from ...lexer.token_type import TokenType
from .base_expression import BaseExpressionParser

BUILTIN_FUNCTIONS = ["SIN", "COS", "TAN", "ABS", "LOG", "EXP", "SQR", "INT", "RND"]

class BuiltinFunctionParser(BaseExpressionParser):
    def parse(self):
        function_name = self.parser.current_token.value.upper()
        if function_name not in BUILTIN_FUNCTIONS:
            raise ValueError(f"{function_name} is not a built-in function")

        self.parser.advance()  # Consume the function name

        # Get the left parenthesis
        if self.parser.current_token.token_type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after built-in function name")
        self.parser.advance()

        arguments = []
        # Parse arguments
        while self.parser.current_token.token_type != TokenType.RPAREN:
            expression = self.parser.parse_expression()
            arguments.append(expression)

            # Check for comma separator or closing parenthesis
            if self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()
            elif self.parser.current_token.token_type != TokenType.RPAREN:
                raise SyntaxError("Expected ',' or ')' in argument list of built-in function")

        # Advance past the closing parenthesis
        self.parser.advance()

        # Return the built-in function as a FnExpression
        return FnExpression(Variable(function_name), arguments)