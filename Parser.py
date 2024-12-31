class Node:
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value
        self.children = children if children else []

    def __repr__(self, level=0):
        indent = '  ' * level
        repr_str = f"{indent}Node({self.type}, {repr(self.value)})"
        if self.children:
            repr_str += '\n' + '\n'.join([child.__repr__(level + 1) for child in self.children])
        return repr_str


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type=None):
        print(f"Eat called with: {self.current_token()}")
        if token_type:
            if self.current_token() and self.current_token().type == token_type:
                current = self.current_token()
                self.current_token_index += 1
                return current
            else:
                raise ValueError(f"Expected token type {token_type}, but got {self.current_token()}")
        else:
            current = self.current_token()
            self.current_token_index += 1
            return current

    def parse_class(self):
        print("Starting to parse class...")
        node = Node("Class")
        if self.current_token() and self.current_token().type == 'KEYWORD' and self.current_token().value == 'class':
            self.eat('KEYWORD')  # 'class'
            class_name = self.eat('IDENTIFIER')
            node.value = class_name.value
            print(f"Class found: {class_name.value}")
            self.eat('LBRACE')
            node.children = self.parse_body()
            self.eat('RBRACE')
        else:
            print("Error: Expected class keyword")
        return node

    def parse_body(self):
        body = []
        while self.current_token() and self.current_token().type != 'RBRACE':
            body.append(self.parse_statement())
        return body

    def parse_statement(self):
        current = self.current_token()
        print(f"Parsing statement: {current}")

        if current.type == 'KEYWORD':
            if current.value in ['int', 'String', 'double']:
                return self.parse_variable_declaration()
            elif current.value == 'public':
                return self.parse_method_declaration()
            else:
                raise ValueError(f"Unknown keyword: {current.value}")
        elif current.type == 'IDENTIFIER':
            next_token = self.peek()
            if next_token and next_token.type == 'OPERATOR' and next_token.value == '=':
                return self.parse_assignment()
            else:
                return self.parse_variable_usage()
        else:
            raise ValueError(f"Unexpected token: {current}")

    def parse_variable_declaration(self):
        data_type = self.eat('KEYWORD')
        var_name = self.eat('IDENTIFIER')

        if self.current_token() and self.current_token().type == 'OPERATOR' and self.current_token().value == '=':
            self.eat('OPERATOR')
            value = self.eat('STRING' if data_type.value == 'String' else 'NUMBER')
        else:
            value = None

        self.eat('SEMICOLON')
        return Node("VariableDeclaration", value=f"{data_type.value} {var_name.value}", children=[
            Node("Value", value=value.value if value else None)
        ])

    def parse_method_declaration(self):
        access_modifier = self.eat('KEYWORD')
        return_type = self.eat('KEYWORD')
        method_name = self.eat('IDENTIFIER')
        self.eat('LPAREN')
        self.eat('RPAREN')
        self.eat('LBRACE')
        method_body = self.parse_body()
        self.eat('RBRACE')
        return Node("MethodDeclaration", value=f"{access_modifier.value} {return_type.value} {method_name.value}",
                    children=method_body)

    def parse_variable_usage(self):
        var_name = self.eat('IDENTIFIER')
        return Node("VariableUsage", value=var_name.value)

    def parse_assignment(self):
        # Обработка присваивания
        var_name = self.eat('IDENTIFIER')
        if self.current_token() and self.current_token().type == 'OPERATOR' and self.current_token().value == '=':
            self.eat('OPERATOR')
        else:
            raise ValueError(f"Expected '=' operator after variable {var_name.value}")

        value = None
        if self.current_token().type == 'STRING':
            value = self.eat('STRING')
        elif self.current_token().type == 'NUMBER':
            value = self.eat('NUMBER')
        else:
            raise ValueError(f"Expected value after '=', but got {self.current_token()}")

        self.eat('SEMICOLON')
        return Node("Assignment", value=f"{var_name.value} = {value.value}", children=[
            Node("Variable", value=var_name.value),
            Node("Value", value=value.value)
        ])

    def peek(self, offset=1):
        idx = self.current_token_index + offset
        return self.tokens[idx] if idx < len(self.tokens) else None
