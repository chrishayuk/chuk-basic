from ...lexer.tokenizer import Tokenizer
from ...ast.ast_expression import BinaryExpression
from ...ast.ast_statement import Statement, PrintStatement
from ...ast.ast_control_flow import IfStatement, ForStatement, GotoStatement, GosubStatement, OnStatement
from ..statement_parser import parse_statement
from ..parser import Parser

def test_parse_if_statement():
    input_string = "IF x > 10 THEN PRINT \"Greater than 10\" ELSE PRINT \"Less than or equal to 10\""
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, IfStatement)
    assert isinstance(statement.condition, BinaryExpression)
    assert isinstance(statement.then_statement, PrintStatement)
    assert isinstance(statement.else_statement, PrintStatement)

def test_parse_for_statement():
    input_string = "FOR i = 1 TO 10 STEP 2\nPRINT i\nNEXT i"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)

    assert isinstance(statement, ForStatement)
    for body_statement in statement.loop_body:
        assert isinstance(body_statement, Statement)

def test_parse_goto_statement():
    input_string = "GOTO 100"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, GotoStatement)

def test_parse_gosub_statement():
    input_string = "GOSUB 200"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, GosubStatement)

def test_parse_on_statement():
    input_string = "ON x GOTO 100, 200, 300"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, OnStatement)
    assert statement.is_gosub == False

def test_parse_on_gosub_statement():
    input_string = "ON x GOSUB 100, 200, 300"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, OnStatement)
    assert statement.is_gosub == True