from contextlib import suppress
from compiler.lexer.token_type import TokenType
from ..ast.ast_function import DefStatement
from .expression_parser import parse_expression

def parse_def_statement(parser):
    # set the position
    parser.advance()

    # parse the function name
    function_name = parser.parse_variable()

    # expect the opening parenthesis
    if parser.current_token.token_type != TokenType.LPAREN:
        raise SyntaxError("Expected '(' after function name in DEF statement")
    parser.advance()

    # parse the parameter list
    parameters = []
    while parser.current_token.token_type != TokenType.RPAREN:
        parameter = parser.parse_variable()
        parameters.append(parameter)
        if parser.current_token.token_type == TokenType.COMMA:
            parser.advance()
        else:
            break

    # expect the closing parenthesis
    if parser.current_token.token_type != TokenType.RPAREN:
        raise SyntaxError("Expected ')' after parameter list in DEF statement")
    parser.advance()

    # expect the '=' sign
    if parser.current_token.token_type != TokenType.EQ:
        raise SyntaxError("Expected '=' after parameter list in DEF statement")
    parser.advance()

    # parse the function body
    function_body = parse_expression(parser)

    # return the statement
    return DefStatement(function_name, parameters, function_body)