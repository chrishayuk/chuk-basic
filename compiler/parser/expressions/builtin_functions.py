from ...lexer.token_type import TokenType
from ...ast.variable import Variable
from ...ast.expressions import FnExpression, Literal

BUILTIN_FUNCTIONS = {
    "SIN", "COS", "ATN", "INT", "TAN", "EXP", "ABS", "LOG", "SQR", "RND",
    "CHR$", "LEFT$", "RIGHT$", "MID$", "SGN", "STR$", "VAL", "SPC", "TAB"
}

class BuiltinFunctionParser:
    def __init__(self, parser):
        self.parser = parser

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
        while self.parser.current_token and self.parser.current_token.token_type != TokenType.RPAREN:
            expression = self.parser.parse_expression()
            if isinstance(expression, Literal):
                value = expression.value
                if isinstance(value, int):
                    expression = Literal(float(value))
            arguments.append(expression)

            # Check for comma separator
            if self.parser.current_token and self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()

        # Consume the closing parenthesis
        if self.parser.current_token and self.parser.current_token.token_type == TokenType.RPAREN:
            self.parser.advance()
        else:
            raise SyntaxError("Expected ')' in argument list of built-in function")

        # Return the built-in function expression
        return FnExpression(Variable(function_name), arguments)