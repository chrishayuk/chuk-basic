from compiler.ast.statements.on_statement import OnStatement
from ....lexer.tokenizer import Tokenizer
from ....ast.expressions import BinaryExpression, Literal
from ....ast.statements import PrintStatement, IfStatement, ForStatement, GotoStatement, GosubStatement, NextStatement
from ...parser import Parser

def test_parse_if_statement():
    input_string = "10 IF x > 10 THEN PRINT \"Greater than 10\" ELSE PRINT \"Less than or equal to 10\""
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.lines) == 1  # Ensure there is exactly one line in the program
    line = program.lines[10]
    assert len(line) == 1  # Ensure there is exactly one statement in the line
    if_statement = line[0]

    # Check that the statement is indeed an IfStatement
    assert isinstance(if_statement, IfStatement)
    # Check the condition of the IfStatement
    assert isinstance(if_statement.condition, BinaryExpression)
    # Now check the then_clause and else_clause
    assert isinstance(if_statement.then_clause, PrintStatement)
    assert isinstance(if_statement.else_clause, PrintStatement)

def test_parse_for_statement():
    input_string = "20 FOR i = 1 TO 10 STEP 2\n30 PRINT i\n40 NEXT i"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object, which should contain the FOR loop

    assert len(program.lines) == 3  # Ensure there are three lines in the program
    for_line = program.lines[20]
    assert len(for_line) == 1  # Ensure there is exactly one statement in the FOR line
    for_statement = for_line[0]

    # Validate ForStatement structure
    assert isinstance(for_statement, ForStatement)
    assert for_statement.variable.name == "i"
    assert isinstance(for_statement.start_expression, Literal) and for_statement.start_expression.value == 1
    assert isinstance(for_statement.end_expression, Literal) and for_statement.end_expression.value == 10
    assert isinstance(for_statement.step_expression, Literal) and for_statement.step_expression.value == 2

    # Check loop body
    print_line = program.lines[30]
    assert len(print_line) == 1  # Ensure there is exactly one statement in the PRINT line
    body_statement = print_line[0]
    assert isinstance(body_statement, PrintStatement)  # The loop body should contain a PrintStatement

    # Validate the loop variable in the NEXT statement matches the FOR loop variable
    next_line = program.lines[40]
    assert len(next_line) == 1  # Ensure there is exactly one statement in the NEXT line
    next_statement = next_line[0]
    assert isinstance(next_statement, NextStatement)
    assert next_statement.variable.name == "i"


def test_parse_goto_statement():
    input_string = "50 GOTO 100"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()  # This returns a Program object
    assert len(program.lines) == 1  # Ensure there is exactly one line in the Program
    line = program.lines[50]
    assert len(line) == 1  # Ensure there is exactly one statement in the line
    statement = line[0]
    assert isinstance(statement, GotoStatement)
    assert statement.line_number == 50  # Check the line number where the GOTO statement is located
    assert statement.target_line_number.value == 100  # Check the target line number


def test_parse_gosub_statement():
    input_string = "60 GOSUB 200"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)

    program = parser.parse()  # This returns a Program object

    assert len(program.lines) == 1  # Ensure there is exactly one line in the Program

    line = program.lines[60]
    assert len(line) == 1  # Ensure there is exactly one statement in the line

    statement = line[0]
    assert isinstance(statement, GosubStatement)

    assert statement.line_number == 60  # Check the line number where the GOSUB statement is located
    assert statement.target_line_number.value == 200  # Check the target line number

def test_parse_on_goto_statement():
    input_string = "70 ON x GOTO 100, 200, 300"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)

    program = parser.parse()  # This returns a Program object

    assert len(program.lines) == 1  # Ensure there is exactly one line in the Program

    line = program.lines[70]
    assert len(line) == 1  # Ensure there is exactly one statement in the line

    on_goto_statement = line[0]
    assert isinstance(on_goto_statement, OnStatement)

    assert on_goto_statement.line_number == 70  # Check the line number where the ON GOTO statement is located
    assert not on_goto_statement.is_gosub  # Check if it's an ON GOTO statement
    assert len(on_goto_statement.line_numbers) == 3  # Check the correct number of line numbers
    assert on_goto_statement.line_numbers[0].value == 100  # Check the first line number
    assert on_goto_statement.line_numbers[1].value == 200  # Check the second line number
    assert on_goto_statement.line_numbers[2].value == 300  # Check the third line number

def test_parse_on_gosub_statement():
    input_string = "80 ON x GOSUB 100, 200, 300"
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)

    program = parser.parse()  # This returns a Program object

    assert len(program.lines) == 1  # Ensure there is exactly one line in the Program

    line = program.lines[80]
    assert len(line) == 1  # Ensure there is exactly one statement in the line

    on_gosub_statement = line[0]
    assert isinstance(on_gosub_statement, OnStatement)

    assert on_gosub_statement.line_number == 80  # Check the line number where the ON GOSUB statement is located
    assert on_gosub_statement.is_gosub  # Check if it's an ON GOSUB statement
    assert len(on_gosub_statement.line_numbers) == 3  # Check the correct number of line numbers
    assert on_gosub_statement.line_numbers[0].value == 100  # Check the first line number
    assert on_gosub_statement.line_numbers[1].value == 200  # Check the second line number
    assert on_gosub_statement.line_numbers[2].value == 300  # Check the third line number