from typing import Optional
from contextlib import suppress
from .ast.ast_node import Variable
from .ast.ast_expression import Expression, BinaryExpression, FnExpression, Literal, UnaryExpression
from ..lexer.token_type import TokenType

def parse_expression(parser) -> Optional[Expression]:
    """Parse and return the top-level expression in the token stream."""
    # parse a binary expression by default
    return parse_binary_expression(parser, 0)

def parse_binary_expression(parser, precedence: int) -> Optional[Expression]:
    """Parse and return a binary expression with the given precedence."""
    # left is unary
    left = parse_unary_expression(parser)

    # get right hand token
    while parser.current_pos < len(parser.tokens):
        # get the token
        token = parser.current_token

        # plus, minus, multiply, divide, comparison operators, and inbuilt functions are binary operators
        if token.token_type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POW,
            TokenType.AND, TokenType.OR,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE
        ]:
            operator_precedence = get_operator_precedence(token.token_type)
            if operator_precedence > precedence:
                parser.advance()
                right = parse_binary_expression(parser, operator_precedence)
                left = BinaryExpression(left, token, right)
            else:
                break
        elif token.token_type in [TokenType.RPAREN, TokenType.THEN, TokenType.TO, TokenType.EQ, TokenType.ELSE, TokenType.STEP, TokenType.PRINT, TokenType.NEXT]:
            # These tokens are valid in other contexts, so we should not raise an error here
            break
        else:
            raise SyntaxError(f"Unexpected token '{token.value}' ({token.token_type}) while parsing binary expression")

    return left

def parse_unary_expression(parser) -> Optional[Expression]:
    """Parse and return a unary expression."""
    with suppress(StopIteration):
        # get the token
        token = parser.current_token

        # math stuff, +, -, NOT
        if token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            parser.advance()
            operand = parse_unary_expression(parser)
            return UnaryExpression(token, operand)

    return parse_primary_expression(parser)

def parse_primary_expression(parser) -> Optional[Expression]:
    """Parse and return a primary expression."""
    with suppress(StopIteration):
        # get the current token
        token = parser.current_token

        # numbers are literals
        if token.token_type == TokenType.NUMBER:
            parser.advance()
            return Literal(token.value)
        # strings are literals
        elif token.token_type == TokenType.STRING:
            parser.advance()
            return Literal(token.value)
        elif token.token_type == TokenType.IDENTIFIER:
            parser.advance()
            return Variable(token.value)
        # parenthesis
        elif token.token_type == TokenType.LPAREN:
            parser.advance()
            # parse expression handles the right parenthesis
            expression = parse_expression(parser)
            if parser.current_token is None:
                raise SyntaxError("Unexpected end of token stream while parsing parenthesized expression")
            elif parser.current_token.token_type != TokenType.RPAREN:
                raise SyntaxError(f"Expected closing parenthesis, but got '{parser.current_token.value}' ({parser.current_token.token_type})")
            parser.advance()
            return expression
        # line number
        elif token.token_type == TokenType.LINENO:
            # Skip line number tokens in expressions
            parser.advance()
            return parse_primary_expression(parser)
        elif token.token_type == TokenType.FN:
            return parse_fn_expression(parser)
        else:
            raise SyntaxError(f"Unexpected token '{token.value}' ({token.token_type}) while parsing primary expression")

    return None

def get_operator_precedence(token_type: TokenType) -> int:
    """Get the operator precedence for the given token type."""
    # set the operator precedence for each operator
    if token_type in [TokenType.OR]:
        return 1
    elif token_type in [TokenType.AND]:
        return 2
    elif token_type in [TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE]:
        return 3
    elif token_type in [TokenType.PLUS, TokenType.MINUS]:
        return 4
    elif token_type in [TokenType.MUL, TokenType.DIV]:
        return 5
    elif token_type in [TokenType.POW]:
        return 6
    else:
        return 0
    
def parse_fn_expression(parser) -> Optional[FnExpression]:
    """Parse and return an FN expression."""
    # expect the FN keyword
    if parser.current_token is None or parser.current_token.token_type != TokenType.FN:
        raise SyntaxError("Expected 'FN' keyword")
    parser.advance()

    # parse the function name
    if parser.current_token is None or parser.current_token.token_type != TokenType.IDENTIFIER:
        raise SyntaxError("Expected function name after 'FN' keyword")
    function_name = Variable(parser.current_token.value)
    parser.advance()

    # expect the opening parenthesis
    if parser.current_token is None or parser.current_token.token_type != TokenType.LPAREN:
        raise SyntaxError("Expected '(' after function name in FN statement")
    parser.advance()

    # parse the argument
    argument = parse_expression(parser)
    if argument is None:
        raise SyntaxError("Expected an expression as the argument in FN statement")
    parser.advance()

    # expect the '=' sign
    if parser.current_token is None or parser.current_token.token_type != TokenType.EQ:
        raise SyntaxError("Expected '=' after argument in FN statement")
    parser.advance()

    # parse the function body
    function_body = parse_expression(parser)
    if function_body is None:
        raise SyntaxError("Expected an expression as the function body in FN statement")

    # return the FnExpression
    return FnExpression(function_name, argument, function_body)