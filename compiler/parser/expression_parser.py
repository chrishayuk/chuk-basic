from ast import *
from ..lexer.token_type import TokenType
from .ast import BinaryExpression, FnExpression, Literal, UnaryExpression, Variable

def parse_expression(parser):
    return parse_binary_expression(parser, 0)

def parse_binary_expression(parser, precedence):
    # left is unary
    left = parse_unary_expression(parser)

    # get right hand token
    while parser.current_pos < len(parser.tokens):
        # get the token
        token = parser.tokens[parser.current_pos]

        # plus, minus, multiply, divide, comparison operators, and inbuilt functions are binary operators
        if token.token_type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POW,
            TokenType.AND, TokenType.OR,
            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE
        ]:
            operator_precedence = get_operator_precedence(token.token_type)
            if operator_precedence > precedence:
                parser.current_pos += 1
                right = parse_binary_expression(parser, operator_precedence)
                left = BinaryExpression(left, token, right)
            else:
                break
        else:
            break

    return left

def parse_unary_expression(parser):
    # ensure we still have tokens
    if parser.current_pos < len(parser.tokens):
        # parse the token
        token = parser.tokens[parser.current_pos]

        # math stuff, +, -, NOT
        if token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            parser.current_pos += 1
            operand = parse_unary_expression(parser)
            return UnaryExpression(token, operand)

    return parse_primary_expression(parser)

def parse_primary_expression(parser):
    # ensure we still have tokens
    if parser.current_pos < len(parser.tokens):
        # get the current token
        token = parser.tokens[parser.current_pos]

        # numbers are literals
        if token.token_type == TokenType.NUMBER:
            parser.current_pos += 1
            return Literal(token.value)
        # strings are literals
        elif token.token_type == TokenType.STRING:
            parser.current_pos += 1
            return Literal(token.value)
        elif token.token_type == TokenType.IDENTIFIER:
            parser.current_pos += 1
            return Variable(token.value)
        # parenthesis
        elif token.token_type == TokenType.LPAREN:
            parser.current_pos += 1
            expression = parse_expression(parser)
            if parser.current_pos < len(parser.tokens) and parser.tokens[parser.current_pos].token_type == TokenType.RPAREN:
                parser.current_pos += 1
                return expression
            else:
                raise ValueError("Expected closing parenthesis")
        # line number
        elif token.token_type == TokenType.LINENO:
            # Skip line number tokens in expressions
            parser.current_pos += 1
            return parse_primary_expression(parser)
        elif token.token_type == TokenType.FN:
            return parse_fn_expression(parser)

    return None

def get_operator_precedence(token_type):
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
    
def parse_fn_expression(parser):
    # expect the FN keyword
    if parser.current_token.token_type != TokenType.FN:
        raise SyntaxError("Expected 'FN' keyword")
    parser.advance()

    # parse the function name
    function_name = parser.parse_variable()

    # expect the opening parenthesis
    if parser.current_token.token_type != TokenType.LPAREN:
        raise SyntaxError("Expected '(' after function name in FN statement")
    parser.advance()

    # parse the argument
    argument = parse_expression(parser)
    parser.advance()

    # expect the '=' sign
    if parser.current_token.token_type != TokenType.EQ:
        raise SyntaxError("Expected '=' after argument in FN statement")
    parser.advance()
    print("current token type: ", parser.current_token.token_type)

    # parse the function body
    function_body = parse_expression(parser)

    # return the FnExpression
    return FnExpression(function_name, argument, function_body)