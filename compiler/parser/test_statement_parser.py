from compiler.lexer.tokenizer import Tokenizer
from compiler.parser.ast import (
    BinaryExpression,
    IfStatement,
    ForStatement,
    GotoStatement,
    GosubStatement,
    NextStatement,
    ReturnStatement,
    InputStatement,
    LetStatement,
    RemStatement,
    Statement,
    StopStatement,
    PrintStatement,
    EndStatement,
    OnStatement,
    DefStatement,
    FnExpression,
)
from compiler.parser.expression_parser import parse_expression
from compiler.parser.statement_parser import parse_statement
from compiler.parser.parser import Parser

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
    assert isinstance(statement.loop_body, Statement)
    assert isinstance(statement.next_statement, NextStatement)
    assert statement.next_statement.variable.name == "i"

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

# def test_parse_on_statement():
#     input_string = "ON x GOTO 100, 200, 300"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)
#     statement = parse_statement(parser)
#     assert isinstance(statement, OnStatement)
#     assert statement.is_gosub == False

# def test_parse_on_gosub_statement():
#     input_string = "ON x GOSUB 100, 200, 300"
#     tokenizer = Tokenizer(input_string)
#     tokens = tokenizer.tokenize()
#     parser = Parser(tokens)
#     statement = parse_statement(parser)
#     assert isinstance(statement, OnStatement)
#     assert statement.is_gosub == True

def test_parse_def_statement():
    input_string = "DEF Square(x) = x * x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    statement = parse_statement(parser)
    assert isinstance(statement, DefStatement)

def test_parse_fn_expression():
    input_string = "def FNSquare(5) = 5 * 5"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parse_expression(parser)
    assert isinstance(expression, FnExpression)