from lexer.tokenizer import Tokenizer, TokenizationError

def read_basic_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Example usage
#file_path = 'samples/test1.bas'
file_path = 'samples/aceyducey.bas'
#file_path = 'samples/dartmouth_first.bas'
file_path = 'samples/complex.bas'

try:
    input_code = read_basic_file(file_path)
    tokenizer = Tokenizer(input_code)
    tokens = tokenizer.tokenize()
    for token in tokens:
        print(token)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except TokenizationError as e:
    print(f"Tokenization error: {str(e)}")