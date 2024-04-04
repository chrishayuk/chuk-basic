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

def test_print_statement():
    input_string = '10 PRINT "Hello World"'
    expected_json = json.dumps({
        "type": "Program",
        "lines": [
            {
                "line_number": 10,
                "statements": [
                    {
                        "type": "PrintStatement",
                        "expression": {
                            "type": "LiteralExpression",
                            "value": "Hello World"
                        }
                    }
                ]
            }
        ]
    }, indent=4)

    assert ast_to_json(input_string) == expected_json



def test_multiple_statements():
    input_string = '10 LET x = 5\n20 PRINT x'
    expected_json = json.dumps({
        "type": "Program",
        "lines": [
            {
                "line_number": 10,
                "statements": [
                    {
                        "type": "LetStatement",
                        "variable": {  # Updated to match the structure given by LetStatement's to_dict
                            "type": "Variable",
                            "name": "x"
                        },
                        "expression": {  # Assuming LiteralExpression's to_dict returns something like this
                            "type": "LiteralExpression",
                            "value": 5  # Adjust based on how numbers are actually serialized
                        }
                    }
                ]
            },
            {
                "line_number": 20,
                "statements": [
                    {
                        "type": "PrintStatement",
                        "expression": {  # Adjusted for consistency with LetStatement's usage of expression
                            "type": "Variable",
                            "name": "x"
                        }
                    }
                ]
            }
        ]
    }, indent=4)

    actual_json = ast_to_json(input_string)
    print("Actual JSON:", actual_json)
    print("Expected JSON:", expected_json)
    assert actual_json == expected_json