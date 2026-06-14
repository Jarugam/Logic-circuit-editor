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
    i = 0
    while i < len(clauses):
        j = 0
        while j < len(vars) and clauses[i] != []:
            if (vars[j] in clauses[i]) and (('not ' + vars[j]) in clauses[i]):
                clauses[i] = []
            else:
                j += 1
        if clauses[i] == []:
            clauses.pop(i)
        else:
            i += 1

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

def ordered_append(lit_list, var):
    read = []

    while lit_list != []:
        if int(lit_list[0][-1]) > int(var[-1]):
            return (read + [var] + lit_list)
        elif int(lit_list[0][-1]) == int(var[-1]):
            return(read + lit_list)
        read.append(lit_list.pop(0)) 

    read.append(var)
    return read

def order_literals(clauses):
    ordered_list = [] 
    for clause in clauses:
        literals = []
        if clause[0][0] == 'n':
            literals.append('-' + clause[0][-1])
        else:
            literals.append(clause[0][-1])
        for var in clause[1:]:
            if var[0] == 'n':
                literals = ordered_append(literals, '-' + var[-1])
            else:
                literals = ordered_append(literals, var[-1])
        ordered_list.append(literals)
    return ordered_list

def to_dimacs(circuit, vars):
    ast = Parser(circuit).parse_expr()
    
    ast = remove_xor(ast)
    ast = push_not(ast)
    
    cnf_clauses = into_clauses(to_cnf(ast))
    cnf_clauses = remove_truth(cnf_clauses, vars)
    cnf_clauses = order_literals(cnf_clauses)

    i = 0
    while i < len(cnf_clauses):
        j = i + 1
        while j < len(cnf_clauses):
            if cnf_clauses[i] == cnf_clauses[j]:
                cnf_clauses.pop(j)
            else:
                j += 1
        i += 1


    outptut = []
    outptut.append(f"p cnf {len(vars)} {len(cnf_clauses)}\n")
    for clause in cnf_clauses:
        text_line = ""
        for var in clause:
            text_line += (var + ' ') 
        text_line += '0\n'
        outptut.append(text_line)

    return outptut
    
def main():
    test_circuit1 = "((V2 or V4) and ((not V1) xor V3))"
    test_circuit2 = "(not ((V2 or V4) and ((not V1) xor V3)))"

    # ast = Parser('(((not V1) xor V2) or (not ((not V4) and V3)))')
    # ast = Parser(test_circuit2)
    # ast = ast.parse_expr()
    # print(ast)
    # xorless = remove_xor(ast)
    # notless = push_not(xorless)
    # cnf = to_cnf(notless)
    # print(pprint(cnf))
    # clauses = into_clauses(cnf)
    # print(clauses)
    # truthless = remove_truth(clauses, ['V0','V1','V2','V3'])
    # print(truthless)
    # ordered = order_literals(truthless)
    # print(ordered)

    dimacs_test = to_dimacs(test_circuit1, ['V0', 'V1', 'V2', 'V3'])
    for line in dimacs_test:
        print(line, end='')

if __name__ == "__main__":
    main()