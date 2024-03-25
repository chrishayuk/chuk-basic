# basic_statement_parser.py
from ..lexer.token_type import TokenType
from ..ast.ast_statement import PrintStatement, ReturnStatement, LetStatement, RemStatement, InputStatement, EndStatement, StopStatement
from .expression_parser import parse_expression


def parse_basic_statement(parser):
    # get the current token type
    token_type = parser.current_token.token_type

    # parse the basic statements
    if token_type == TokenType.RETURN:
        return parse_return_statement(parser)
    elif token_type == TokenType.INPUT:
        return parse_input_statement(parser)
    elif token_type == TokenType.LET:
        return parse_let_statement(parser)
    elif token_type == TokenType.REM:
        return parse_rem_statement(parser)
    elif token_type == TokenType.STOP:
        return parse_stop_statement(parser)
    elif token_type == TokenType.PRINT:
        return parse_print_statement(parser)
    elif token_type == TokenType.END:
        return parse_end_statement(parser)
    else:
        return None
       
def parse_return_statement(parser):
    # set the position
    parser.advance()

    # return the statement
    return ReturnStatement()

def parse_input_statement(parser):
    # set the position
    parser.advance()

    # parse the variable
    variable = parser.parse_variable()

    # return the statement
    return InputStatement(variable)

def parse_let_statement(parser):
    # set the position
    parser.advance()
    
    # parse the variable
    variable = parser.parse_variable()

    # parse the expression
    parser.advance()  # skip '='
    expression = parse_expression(parser)

    # return the statement
    return LetStatement(variable, expression)

def parse_rem_statement(parser):
    # set the position
    parser.advance()

    # check we have a current token
    if parser.current_token is not None:
        # get the comment
        comment = parser.current_token.value

        # move to the next token
        parser.advance()  
    else:
        # empty comment
        comment = ""

    # return the statement
    return RemStatement(comment)

def parse_stop_statement(parser):
    # set the position
    parser.advance()

    # return the statement
    return StopStatement()

def parse_print_statement(parser):
    # set the position
    parser.advance()

    # parse the expression
    expression = parse_expression(parser)

    # return the statement
    return PrintStatement(expression)

def parse_end_statement(parser):
    # set the position
    parser.advance()

    # return the statement
    return EndStatement()