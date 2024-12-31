from Parser import Parser
from Tokenizer import Tokenizer

if __name__ == "__main__":
    with open("Java", "r", encoding="utf-8") as file:
        java_code = file.read()

    tokenizer = Tokenizer(java_code)
    tokens = tokenizer.tokenize()

    print("Токены:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse_class()

    print("\nAST:")
    print(ast)
