def read_next(to_read):
    read = ''
    while to_read[0] != ' ':
        read += to_read[0]
        to_read = to_read[1:]
        if len(to_read) == 0:
            return read, to_read

    return read, to_read[1:]

def read_skip(to_read):
    read = ''
    count = 0
    while to_read[0] != ')' or count > 0:
        if to_read[0] == '(':
            count += 1
        elif to_read[0] == ')':
            count -= 1
        read += to_read[0]
        to_read = to_read[1:]
    read += to_read[0]
    to_read = to_read[1:]
    
    if len(to_read) > 0:
        return read, to_read[1:]
    return read, to_read

def remove_xor(circuit):
    if 'xor' not in circuit:
        print("Nothing to remove!")
        return circuit
    
    to_read = circuit
    read = ''

    read += to_read[0]
    to_read = to_read[1:]

    if read == '(':
        skipped, to_read = read_skip(to_read)
        sub_l = read + skipped
        sub_l = '(' + remove_xor(sub_l[1:-1]) + ')'
    elif read == 'n':
        return 'not (' + remove_xor(to_read[4:-1]) + ')'
    else:
        skipped, to_read = read_next(to_read)
        sub_l = read + skipped
    read = ''

    operator, to_read = read_next(to_read)

    read += to_read[0]
    to_read = to_read[1:]

    if read == '(':
        sub_r = read + to_read
        sub_r = '(' + remove_xor(sub_r[1:-1]) + ')'
    else:
        sub_r = read + to_read
    
    if operator == 'xor':
        tmp = '(' + sub_l + ' and (' + 'not ' + sub_r + '))'
        sub_r = '((not ' + sub_l + ') and ' + sub_r + ')'
        sub_l = tmp
        operator = 'or' 

    return sub_l + ' ' + operator + ' ' + sub_r 

def push_not(circuit, not_found = False):
    read = ''
    to_read = circuit

    read += to_read[0]
    to_read = to_read[1:]

    if read == '(':
        skipped, to_read = read_skip(to_read)
        sub_l = read + skipped
        sub_l = '(' + push_not(sub_l[1:-1], not_found) + ')'
    elif read == 'n':
        read = to_read[3]
        to_read = to_read[4:]
        if read == '(':
            skipped, to_read = read_skip(to_read)
            sub_l = read + skipped
            if not_found:
                sub_l = '(' + push_not(sub_l[1:-1], False) + ')'
            else:
                sub_l = '(' + push_not(sub_l[1:-1], True) + ')'
        else:
            skipped, to_read = read_next(to_read)
            sub_l = read + skipped
            if not not_found:
                sub_l = 'not ' + sub_l
        return sub_l
    else:
        skipped, to_read = read_next(to_read)
        sub_l = read + skipped
        if not_found:
                sub_l = 'not ' + sub_l
                if len(to_read) != 0:
                    sub_l = '(' + sub_l + ')'    
        if len(to_read) == 0:
            return sub_l
        # else:
        #     sub_l = '(' + sub_l + ')'
    read = ''

    operator, to_read = read_next(to_read)
    if not_found:
        if operator == 'and':
            operator = 'or'
        else:
            operator = 'and'
    
    read += to_read[0]
    to_read = to_read[1:]

    if read == '(':
        sub_r = read + to_read
        sub_r = '(' + push_not(sub_r[1:-1], not_found) + ')'
    else:
        sub_r = read + to_read
        if not_found:
            sub_r = '(not ' + sub_r + ')'

    return sub_l + ' ' + operator + ' ' + sub_r 

def main():
    test_circuit1 = "(V1 or V3) and ((not V0) xor V2)"
    test_circuit2 = "not ((V1 or V3) and ((not V0) xor V2))"
    xorless = remove_xor(test_circuit1)
    print(xorless)
    
    notless = push_not(xorless)
    print(notless)

if __name__ == "__main__":

    main()