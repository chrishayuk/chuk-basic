from ....lexer.tokenizer import Tokenizer
from ....ast.program import Program
from ....ast.statements import PrintStatement, ReturnStatement, LetStatement, RemStatement, InputStatement, EndStatement, StopStatement
from ...parser import Parser

def test_parse_return_statement():
    input_string = "RETURN"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert isinstance(program, Program)  # Ensure we have a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    assert isinstance(program.statements[0], ReturnStatement)  # Check the type of the statement


def test_parse_input_statement():
    input_string = "INPUT x"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, InputStatement)
    assert statement.variable.name == "x"  # Verify the variable name


def test_parse_let_statement():
    input_string = "LET x = 10"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, LetStatement)
    assert statement.variable.name == "x"  # Check the variable name
    assert statement.expression.value == 10  # Check the assigned value


def test_parse_rem_statement():
    input_string = "REM This is a comment"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert isinstance(program, Program)  # Ensure we have a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    assert isinstance(program.statements[0], RemStatement)  # Check the type of the statement


def test_parse_stop_statement():
    input_string = "STOP"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert isinstance(program, Program)  # Ensure we have a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    assert isinstance(program.statements[0], StopStatement)  # Check the type of the statement


def test_parse_print_statement():
    input_string = "PRINT \"Hello, world!\""
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, PrintStatement)
    assert statement.expression.value == "Hello, world!"  # Verify the printed string


def test_parse_end_statement():
    input_string = "END"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert isinstance(program, Program)  # Ensure we have a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    assert isinstance(program.statements[0], EndStatement)  # Check the type of the statement
