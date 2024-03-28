# test_builtin_functions.py

from ....lexer.token_type import TokenType
from ....lexer.tokenizer import Tokenizer
from ....ast.ast_node import Variable
from ....ast.ast_statement import PrintStatement
from ....ast.ast_expression import FnExpression, Literal
from ...parser import Parser

def test_parse_builtin_sin_function():
    input_string = "10 PRINT SIN(30)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "SIN"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 30

def test_parse_builtin_cos_function():
    input_string = "20 PRINT COS(45)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "COS"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 45

def test_parse_builtin_tan_function():
    input_string = "30 PRINT TAN(60)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "TAN"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == 60

def test_parse_builtin_abs_function():
    input_string = "40 PRINT ABS(-10)"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert len(program.statements) == 1
    print_statement = program.statements[0]
    assert isinstance(print_statement, PrintStatement)
    fn_expression = print_statement.expression
    assert isinstance(fn_expression, FnExpression)
    assert fn_expression.name.name == "ABS"
    assert len(fn_expression.arguments) == 1
    assert isinstance(fn_expression.arguments[0], Literal)
    assert fn_expression.arguments[0].value == -10