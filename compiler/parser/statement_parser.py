from ..lexer.token_type import TokenType
from .expression_parser import parse_fn_expression
from .control_flow_parser import parse_control_flow_statement
from .basic_statement_parser import parse_basic_statement
from .function_parser import parse_def_statement

def parse_statement(parser):
    # get the current token type
    token_type = parser.current_token.token_type

    # parse the statements
    # elif token_type == TokenType.GO:
    #     if parser.current_pos + 1 < len(parser.tokens) and parser.tokens[parser.current_pos + 1].token_type == TokenType.TO:
    #         return (parser)
    #     elif parser.current_pos + 1 < len(parser.tokens) and parser.tokens[parser.current_pos + 1].token_type == TokenType.SUB:
    #         return (parser)
    #     else:
    #         raise SyntaxError("Expected 'TO' or 'SUB' keyword after 'GO'")
    
    # parse control statement
    basic = parse_control_flow_statement(parser)
    if basic != None:
        return basic 
    
    # parse basic statement
    basic = parse_basic_statement(parser)
    if basic != None:
        return basic
    
    

 