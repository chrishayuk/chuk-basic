# test_expression_parser.py
from ast import *
from compiler.lexer.token_type import TokenType
from compiler.lexer.tokenizer import Tokenizer
from .ast import BinaryExpression, Literal, UnaryExpression, Variable
from .expression_parser import parse_expression
from .parser import Parser

def test_parse_literal_expression():
    input_string = "42"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parse_expression(parser)
    assert isinstance(expression, Literal)
    assert expression.value == 42

def test_parse_variable_expression():
    input_string = "x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parse_expression(parser)
    assert isinstance(expression, Variable)
    assert expression.name == "x"

def test_parse_binary_expression():
    input_string = "x + 5 * 3"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parse_expression(parser)
    assert isinstance(expression, BinaryExpression)
    assert isinstance(expression.left, Variable)
    assert expression.left.name == "x"
    assert expression.operator.token_type == TokenType.PLUS
    assert isinstance(expression.right, BinaryExpression)
    assert isinstance(expression.right.left, Literal)
    assert expression.right.left.value == 5
    assert expression.right.operator.token_type == TokenType.MUL
    assert isinstance(expression.right.right, Literal)
    assert expression.right.right.value == 3

def test_parse_unary_expression():
    input_string = "-x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parse_expression(parser)
    assert isinstance(expression, UnaryExpression)
    assert expression.operator.token_type == TokenType.MINUS
    assert isinstance(expression.operand, Variable)
    assert expression.operand.name == "x"

def test_parse_parenthesized_expression():
    input_string = "(x + 5) * 3"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    expression = parse_expression(parser)
    assert isinstance(expression, BinaryExpression)
    assert isinstance(expression.left, BinaryExpression)
    assert isinstance(expression.left.left, Variable)
    assert expression.left.left.name == "x"
    assert expression.left.operator.token_type == TokenType.PLUS
    assert isinstance(expression.left.right, Literal)
    assert expression.left.right.value == 5
    assert expression.operator.token_type == TokenType.MUL
    assert isinstance(expression.right, Literal)
    assert expression.right.value == 3