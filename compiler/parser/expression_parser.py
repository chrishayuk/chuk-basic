from ast import *
from ..lexer.token_type import TokenType
from .ast import BinaryExpression, Literal, UnaryExpression, Variable

def parse_expression(parser):
    return parse_binary_expression(parser, 0)

def parse_binary_expression(parser, precedence):
    left = parse_unary_expression(parser)

    while parser.current_pos < len(parser.tokens):
        token = parser.tokens[parser.current_pos]
        if token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.POW, TokenType.AND, TokenType.OR]:
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
    if parser.current_pos < len(parser.tokens):
        token = parser.tokens[parser.current_pos]
        if token.token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            parser.current_pos += 1
            operand = parse_unary_expression(parser)
            return UnaryExpression(token, operand)

    return parse_primary_expression(parser)

def parse_primary_expression(parser):
    if parser.current_pos < len(parser.tokens):
        token = parser.tokens[parser.current_pos]
        if token.token_type == TokenType.NUMBER:
            parser.current_pos += 1
            return Literal(token.value)
        elif token.token_type == TokenType.STRING:
            parser.current_pos += 1
            return Literal(token.value)
        elif token.token_type == TokenType.CHAR:
            parser.current_pos += 1
            return Variable(token.value)
        elif token.token_type == TokenType.LPAREN:
            parser.current_pos += 1
            expression = parse_expression(parser)
            if parser.current_pos < len(parser.tokens) and parser.tokens[parser.current_pos].token_type == TokenType.RPAREN:
                parser.current_pos += 1
                return expression
            else:
                raise ValueError("Expected closing parenthesis")

    return None

def get_operator_precedence(token_type):
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