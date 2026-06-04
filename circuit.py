class circ:
    __slots__ = ['circuit', 'var_list', 'expr_list', 'object_list']

    def __init__(self, vars = [], exprs = []):
        self.circuit = ''
        self.var_list = vars
        self.expr_list = exprs
        self.object_list = vars + exprs

    def update_objects(self):
        self.object_list = self.var_list + self.expr_list
        return 0

    def add_var(self, var_name):
        if type(var_name) != str:
            raise Exception('variable name has to be a string!')
        
        if var_name in self.var_list:
            return 0

        self.var_list.append(var_name)
        self.update_objects()
        return 0

    def print_objects(self):
        for i in range(len(self.object_list)):
            print(f"{i})\t {self.object_list[i]}")

    def not_gate(self, object):
        if object + 1 > len(self.var_list):
            self.expr_list.pop(object - len(self.var_list))
            object_name = '(' + self.object_list[object] + ')'
        else:
            object_name = self.object_list[object]

        new_expr = 'not ' + object_name

        self.expr_list.append(new_expr)
        self.update_objects()
        return 0
    
    def multi_gate(self, object1, object2, gate):
        if object1 + 1 > len(self.var_list):
            self.expr_list.pop(object1 - len(self.var_list))
            object1_name = '(' + self.object_list[object1] + ')'
        else:
            object1_name = self.object_list[object1]
        
        if object2 + 1 > len(self.var_list):
            self.expr_list.pop(object2 - len(self.var_list))
            object2_name = '(' + self.object_list[object2] + ')'
        else:
            object2_name = self.object_list[object2]

        new_expr = object1_name + ' ' + gate + ' ' + object2_name

        self.expr_list.append(new_expr)
        self.update_objects()
        return 0
    
    def finalize(self):
        if not len(self.expr_list):
            raise Exception('no circuit to finalize')
        self.circuit = self.expr_list[-1]

def main():
    test1 = circ()
    test1.add_var('v1')
    test1.add_var('v2')

    test1.not_gate(1)
    test1.multi_gate(0, 2, 'and')
    test1.multi_gate(0, 2, 'or')
    print(test1.object_list)
    test1.finalize()

if __name__ == "__main__":
    main()