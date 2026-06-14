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

            if self.peek() == "not":
                self.consume()
                expr = self.parse_expr()

                assert self.consume() == ")"
                return Not(expr)

            left = self.parse_expr()

            op = self.consume()
            assert op in ("and", "or", "xor")

            right = self.parse_expr()

            assert self.consume() == ")"

            return Multi_gate(op, left, right)
        
def remove_xor(node):
    token = node[0]

    if token == "var":
        return node

    if token == "not":
        return Not(remove_xor(node[1]))

    a = remove_xor(node[1])
    b = remove_xor(node[2])

    if token in ("and", "or"):
        return Multi_gate(token, a, b)

    if token == "xor":
        return Multi_gate("or",
            Multi_gate("and", a, Not(b)),
            Multi_gate("and", Not(a), b)
        )
    
def push_not(node):
    token = node[0]

    if token == "var":
        return node

    if token == "not":
        child = node[1]

        if child[0] == "var":
            return node

        if child[0] == "not":
            return push_not(child[1])

        if child[0] == "and":
            return Multi_gate("or",
                push_not(Not(child[1])),
                push_not(Not(child[2]))
            )

        if child[0] == "or":
            return Multi_gate("and",
                push_not(Not(child[1])),
                push_not(Not(child[2]))
            )

    if token == "and":
        return Multi_gate("and",
            push_not(node[1]),
            push_not(node[2])
        )

    if token == "or":
        return Multi_gate("or",
            push_not(node[1]),
            push_not(node[2])
        )

def distribute(a, b):
    if a[0] == "and":
        return Multi_gate("and",
            distribute(a[1], b),
            distribute(a[2], b)
        )

    if b[0] == "and":
        return Multi_gate("and",
            distribute(a, b[1]),
            distribute(a, b[2])
        )

    return Multi_gate("or", a, b)


def to_cnf(node):
    token = node[0]

    if token in ("var", "not"):
        return node

    left = to_cnf(node[1])
    right = to_cnf(node[2])

    if token == "and":
        return Multi_gate("and", left, right)

    if token == "or":
        return distribute(left, right)
    
def gather_var(node):
    token = node[0]
    
    if token == 'or':
        return gather_var(node[1]) + gather_var(node[2])

    if token == 'var':
        return [node[1]]
    
    if token == 'not':
        return ['not ' + node[1][1]]
    
def into_clauses(node):
    token = node[0]

    if token == 'and':
        left = into_clauses(node[1])
        right = into_clauses(node[2])
        return left + right

    if token == 'or':
        return [gather_var(node[1]) + gather_var(node[2])]
    
    if token == 'var':
        return [[node[1]]]
    
    if token == 'not':
        return [['not ' + node[1][1]]]
    
def remove_truth(clauses, vars):
    j = 0
    while j < len(clauses):
        for var in vars:
            if (var in clauses[j]) and (('not ' + var) in clauses[j]):
                i = 0
                while i < len(clauses[j]):
                    if (clauses[j][i] == var) or (clauses[j][i] == 'not ' + var):
                        clauses[j].pop(i)
                    else:
                        i += 1
                if clauses[j] == []:
                    clauses.pop(j)
                    j -= 1
        j += 1

    return clauses


def pprint(node):
    token = node[0]

    if token == "var":
        return node[1]

    if token == "not":
        return f"(not {pprint(node[1])})"

    return (
        f"({pprint(node[1])} "
        f"{token} "
        f"{pprint(node[2])})"
    )
    
def main():
    test_circuit1 = "((V1 or V3) and ((not V0) xor V2))"
    test_circuit2 = "(not ((V1 or V3) and ((not V0) xor V2)))"

    ast = Parser(test_circuit1)
    ast = ast.parse_expr()
    xorless = remove_xor(ast)
    notless = push_not(xorless)
    cnf = to_cnf(notless)
    print(pprint(cnf))
    clauses = into_clauses(cnf)
    print(clauses)
    print(remove_truth(clauses, ['V0','V1','V2','V3']))


if __name__ == "__main__":
    main()