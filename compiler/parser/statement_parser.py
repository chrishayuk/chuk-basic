from ..lexer.token_type import TokenType
from .expression_parser import parse_fn_expression
from .control_flow_parser import parse_control_flow_statement
from .basic_statement_parser import parse_basic_statement
from .function_parser import parse_def_statement

def parse_statement(parser):
    # get the current token type
    token_type = parser.current_token.token_type

    # parse the statements
    if token_type == TokenType.DEF:
        return parse_def_statement(parser)
    else:
        # parse control statement
        basic = parse_control_flow_statement(parser)
        if basic is not None:
            return basic

        # parse basic statement
        basic = parse_basic_statement(parser)
        if basic is not None:
            return basic
        
    # not found
    return None