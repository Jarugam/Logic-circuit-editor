import re

def Var(name):
    return ("var", name)

def Not(x):
    return ("not", x)

def Multi_gate(op, a, b):
    return (op, a, b)

TOKEN_REGEX = re.compile(
    r'V\d+|and|or|not|xor|\(|\)'
)

def tokenize(s):
    return TOKEN_REGEX.findall(s)

class Parser:
    def __init__(self, circuit):
        self.tokens = tokenize(circuit)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse_expr(self):
        token = self.peek()

        if re.fullmatch(r"V\d+", token):
            self.consume()
            return Var(token)

        if token == "(":
            self.consume()

            # unary NOT
            if self.peek() == "not":
                self.consume()
                expr = self.parse_expr()

                assert self.consume() == ")"
                return Not(expr)

            # binary operation
            left = self.parse_expr()

            op = self.consume()
            assert op in ("and", "or", "xor")

            right = self.parse_expr()

            assert self.consume() == ")"

            return Multi_gate(op, left, right)
    
def main():
    test_circuit1 = "((V1 or V3) and ((not V0) xor V2))"
    test_circuit2 = "(not ((V1 or V3) and ((not V0) xor V2)))"

    ast = Parser(test_circuit2)
    print(ast.tokens)
    print(ast.parse_expr())
    # print(ast.pos)
    # print(ast.peek())


if __name__ == "__main__":
    main()