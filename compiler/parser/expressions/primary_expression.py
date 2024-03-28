from ...lexer.token_type import TokenType
from ...ast.ast_node import Variable
from ...ast.ast_expression import FnExpression, Literal
from ...parser.expressions.builtin_functions import BUILTIN_FUNCTIONS, BuiltinFunctionParser
from .base_expression import BaseExpressionParser

class PrimaryExpressionParser(BaseExpressionParser):
    def parse(self):
        # get the token
        token = self.parser.current_token

        # check the token type
        if token.token_type == TokenType.NUMBER:
            self.parser.advance()
            return Literal(int(token.value))
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
            return self.parse_fn_expression()
        else:
            print(f"Error: Unexpected token {token.token_type} with value '{token.value}'")  # Diagnostic print
            raise SyntaxError("Invalid expression")
    
    def parse_fn_expression(self):
        # Consume the FN token
        self.parser.advance()  

        if self.parser.current_token.token_type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function name after FN keyword")

        function_name = self.parser.current_token.value
        self.parser.advance()  # Consume the function name

        if self.parser.current_token.token_type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after function name in FN expression")
        self.parser.advance()  # Consume the '('

        arguments = []
        while self.parser.current_token.token_type != TokenType.RPAREN:
            expression = self.parser.parse_expression()
            arguments.append(expression)

            if self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()  # Consume the ','
            elif self.parser.current_token.token_type != TokenType.RPAREN:
                raise SyntaxError("Expected ',' or ')' in argument list of FN expression")

        self.parser.advance()  # Consume the ')'

        return FnExpression(function_name, arguments)