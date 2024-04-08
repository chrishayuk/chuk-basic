from decimal import Decimal
from ....lexer.tokenizer import Tokenizer
from ....parser.parser import Parser
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

# Adjust how you call json.dumps in your ast_to_json function to use this encoder:
def ast_to_json(input_string):
    tokenizer = Tokenizer(input_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    for line, stmts in sorted(program.lines.items()):
        print(f"Line {line}: {[str(stmt) for stmt in stmts]}")
    program_dict = program.to_dict()
    return json.dumps(program_dict, indent=4, cls=CustomJSONEncoder)

def test_if_statement():
    input_string = '30 IF x = 10 THEN PRINT "x is 10"'
    expected_json = json.dumps({
        "type": "Program",
        "lines": [
            {
                "line_number": 30,
                "statements": [
                    {
                        "type": "IfStatement",
                        "condition": {
                            "type": "BinaryExpression",
                            "operator": "=",
                            "left": {
                                "type": "Variable",
                                "name": "x"
                            },
                            "right": {
                                "type": "LiteralExpression",
                                "value": 10
                            }
                        },
                        "thenPart": {
                            "type": "PrintStatement",
                            "expression": {
                                "type": "LiteralExpression",
                                "value": "x is 10"
                            }
                        }
                    }
                ]
            }
        ]
    }, indent=4, cls=CustomJSONEncoder)

    actual_json = ast_to_json(input_string)
    print("Actual JSON:", actual_json)
    print("Expected JSON:", expected_json)
    assert actual_json == expected_json


def test_for_loop():
    input_string = '40 FOR i = 1 TO 10\n50 PRINT i\n60 NEXT i'
    expected_json = json.dumps({
        "type": "Program",
        "lines": [
            {
                "line_number": 40,
                "statements": [
                    {
                        "type": "ForStatement",
                        "variable": {
                            "type": "Variable",
                            "name": "i"
                        },
                        "start": {
                            "type": "LiteralExpression",
                            "value": 1
                        },
                        "end": {
                            "type": "LiteralExpression",
                            "value": 10
                        },
                        "step": None,
                        "body": [
                            {
                                "line_number": 50,
                                "statements": [
                                    {
                                        "type": "PrintStatement",
                                        "expression": {
                                            "type": "Variable",
                                            "name": "i"
                                        }
                                    }
                                ]
                            }
                        ],
                        "next": {
                            "line_number": 60,
                            "statement": {
                                "type": "NextStatement",
                                "variable": {
                                    "type": "Variable",
                                    "name": "i"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }, indent=4, cls=CustomJSONEncoder)

    actual_json = ast_to_json(input_string)
    print("Actual JSON:", actual_json)
    print("Expected JSON:", expected_json)
    assert actual_json == expected_json

def test_goto_statement():
    input_string = '70 GOTO 100'
    expected_json = json.dumps({
        "type": "Program",
        "lines": [
            {
                "line_number": 70,
                "statements": [
                    {
                        "type": "GotoStatement",
                        "target": 100
                    }
                ]
            }
        ]
    }, indent=4, cls=CustomJSONEncoder)

    actual_json = ast_to_json(input_string)
    print("Actual JSON:", actual_json)
    print("Expected JSON:", expected_json)
    assert actual_json == expected_json

def test_gosub_statement():
    input_string = '70 GOSUB 100'
    expected_json = json.dumps({
        "type": "Program",
        "lines": [
            {
                "line_number": 70,
                "statements": [
                    {
                        "type": "GosubStatement",
                        "target": 100
                    }
                ]
            }
        ]
    }, indent=4, cls=CustomJSONEncoder)

    actual_json = ast_to_json(input_string)
    print("Actual JSON:", actual_json)
    print("Expected JSON:", expected_json)
    assert actual_json == expected_json
