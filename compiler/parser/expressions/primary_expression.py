from ...lexer.token_type import TokenType
from ...ast.ast_node import Variable
from ...ast.ast_expression import FnExpression, Literal
from ...parser.expressions.builtin_functions import BUILTIN_FUNCTIONS, BuiltinFunctionParser
from ...parser.expressions.fn_expression import FnExpressionParser
from .base_expression import BaseExpressionParser

class PrimaryExpressionParser(BaseExpressionParser):
    def parse(self):
        token = self.parser.current_token

        if token.token_type == TokenType.NUMBER:
            self.parser.advance()
            return Literal(token.value)
        elif token.token_type == TokenType.STRING:
            self.parser.advance()
            return Literal(token.value)
        elif token.value.upper() in BUILTIN_FUNCTIONS:
            return BuiltinFunctionParser(self.parser).parse()
        elif token.token_type == TokenType.IDENTIFIER:
            self.parser.advance()
            return Variable(token.value)
        elif token.token_type == TokenType.LPAREN:
            self.parser.advance()
            expression = self.parser.parse_expression()
            if self.parser.current_token.token_type != TokenType.RPAREN:
                raise SyntaxError("Expected ')'")
            self.parser.advance()
            return expression
        elif token.token_type == TokenType.FN:
            return FnExpressionParser(self.parser).parse()
        else:
            print(f"Error: Unexpected token {token.token_type} with value '{token.value}'")  # Diagnostic print
            raise SyntaxError("Invalid expression")
