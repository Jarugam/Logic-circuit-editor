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
        read = ''
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

def main():
    test_circuit = "(V1 or V3) and ((not V0) xor V2)"
    xorless = remove_xor(test_circuit)
    print(xorless)

if __name__ == "__main__":

    main()