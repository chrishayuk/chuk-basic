from ...lexer.token_type import TokenType
from ...ast.ast_node import Variable
from ...ast.ast_expression import FnExpression
from .base_expression import BaseExpressionParser

from ...lexer.token_type import TokenType
from ...ast.ast_node import Variable
from ...ast.ast_expression import FnExpression
from .base_expression import BaseExpressionParser

class FnExpressionParser(BaseExpressionParser):
    def parse(self):
        # skipped past the FN
        self.parser.advance()

        # expect the function name
        if self.parser.current_token.token_type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function name after FN keyword")

        # get the function name and skip past it
        function_name = Variable(self.parser.current_token.value)  # Create a Variable object for the function name
        self.parser.advance()

        # get the left parenthesis
        if self.parser.current_token.token_type != TokenType.LPAREN:
            raise SyntaxError("Expected '(' after function name in FN expression")
        self.parser.advance()

        arguments = []

        # loop until we get the right parenthesis
        while self.parser.current_token.token_type != TokenType.RPAREN:
            # parse the expression
            expression = self.parser.parse_expression()
            arguments.append(expression)

            # loop through commas
            if self.parser.current_token.token_type == TokenType.COMMA:
                self.parser.advance()  # Consume the ','
            elif self.parser.current_token.token_type != TokenType.RPAREN:
                raise SyntaxError("Expected ',' or ')' in argument list of FN expression")

        # skip past the right parenthesis
        self.parser.advance()

        # return the function expression
        return FnExpression(function_name, arguments)
    