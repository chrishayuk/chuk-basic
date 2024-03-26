from ...lexer.tokenizer import Tokenizer
from ...ast.ast_statement import PrintStatement, ReturnStatement, LetStatement, RemStatement, InputStatement, EndStatement, StopStatement
from ..statement_parser import parse_statement
from ..parser import Parser

def test_parse_return_statement():
    input_string = "RETURN"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, ReturnStatement)

def test_parse_input_statement():
    input_string = "INPUT x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, InputStatement)

def test_parse_let_statement():
    input_string = "LET x = 10"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, LetStatement)

def test_parse_rem_statement():
    input_string = "REM This is a comment"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, RemStatement)

def test_parse_stop_statement():
    input_string = "STOP"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, StopStatement)

def test_parse_print_statement():
    input_string = "PRINT \"Hello, world!\""
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, PrintStatement)

def test_parse_end_statement():
    input_string = "END"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, EndStatement)