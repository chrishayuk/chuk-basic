from ....lexer.tokenizer import Tokenizer
from ....ast.expressions import BinaryExpression, Literal
from ....ast.statements import PrintStatement, IfStatement, ForStatement, GotoStatement, GosubStatement, NextStatement, OnStatement
from ...parser import Parser

def test_parse_if_statement():
    input_string = "IF x > 10 THEN PRINT \"Greater than 10\" ELSE PRINT \"Less than or equal to 10\""
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the program
    if_statement = program.statements[0]

    # Check that the statement is indeed an IfStatement
    assert isinstance(if_statement, IfStatement)
    # Check the condition of the IfStatement
    assert isinstance(if_statement.condition, BinaryExpression)
    # Now check the then_statement and else_statement
    assert isinstance(if_statement.then_statement, PrintStatement)
    assert isinstance(if_statement.else_statement, PrintStatement)

def test_parse_for_statement():
    input_string = "FOR i = 1 TO 10 STEP 2\nPRINT i\nNEXT i"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object, which should contain the FOR loop

    assert len(program.statements) == 1  # Ensure there is exactly one statement, the FOR loop
    for_statement = program.statements[0]

    # Validate ForStatement structure
    assert isinstance(for_statement, ForStatement)
    assert for_statement.variable.name == "i"
    assert isinstance(for_statement.start_expression, Literal) and for_statement.start_expression.value == 1
    assert isinstance(for_statement.end_expression, Literal) and for_statement.end_expression.value == 10
    assert isinstance(for_statement.step_expression, Literal) and for_statement.step_expression.value == 2

    # Check loop body
    assert len(for_statement.loop_body) == 1  # There should be one statement in the loop body
    body_statement = for_statement.loop_body[0]
    assert isinstance(body_statement, PrintStatement)  # The loop body should contain a PrintStatement

    # Validate the loop variable in the NEXT statement matches the FOR loop variable
    assert isinstance(for_statement.next_statement, NextStatement)
    assert for_statement.next_statement.variable.name == "i"


def test_parse_goto_statement():
    input_string = "GOTO 100"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    statement = program.statements[0]
    assert isinstance(statement, GotoStatement)
    assert statement.line_number.value == 100  # Assuming line_number is stored as an Expression


def test_parse_gosub_statement():
    input_string = "GOSUB 200"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    statement = program.statements[0]
    assert isinstance(statement, GosubStatement)
    assert statement.line_number.value == 200  # Assuming line_number is stored as an Expression

def test_parse_on_statement():
    input_string = "ON x GOTO 100, 200, 300"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    on_statement = program.statements[0]
    assert isinstance(on_statement, OnStatement)
    assert on_statement.is_gosub == False
    assert len(on_statement.line_numbers) == 3  # Check the correct number of line numbers

def test_parse_on_gosub_statement():
    input_string = "ON x GOSUB 100, 200, 300"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object
    assert len(program.statements) == 1  # Ensure there is exactly one statement in the Program
    on_statement = program.statements[0]
    assert isinstance(on_statement, OnStatement)
    assert on_statement.is_gosub == True
    assert len(on_statement.line_numbers) == 3  # Check the correct number of line numbers