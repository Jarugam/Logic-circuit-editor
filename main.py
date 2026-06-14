from circuit import circ
from dimacs import to_dimacs
import schemdraw
from schemdraw.parsing import logicparse
import sys
import json
import time
import os

def pick_a_gate(circuit):
    while True:
        choice1 = input("Choose a gate to add:\n" \
        "1) not\n" \
        "2) and\n" \
        "3) or\n" \
        "4) xor\n")

        if choice1 == '1':
            while True:
                print("Choose an object:")
                circuit.print_objects()
                choice2 = input()
                if int(choice2) > len(circuit.object_list) or int(choice2) < 1:
                    print("Wrong choice!")
                else:
                    break

            circuit.not_gate(int(choice2) - 1)
            return 0
        
        elif choice1 in ['2', '3', '4']:
            chosen_gate = ['and', 'or', 'xor'][int(choice1) - 2]
            count = 0
            multi_choice = []

            while count < 2:
                if count == 0:
                    print("Choose first object:\n")
                else:
                    print("Choose second object:\n")

                circuit.print_objects()
                choice2 = input()
                if int(choice2) > len(circuit.object_list) or int(choice2) < 1:
                    print("Wrong choice!")
                else:
                    multi_choice.append(choice2)
                    count += 1
            
            circuit.multi_gate(int(multi_choice[0]) - 1, int(multi_choice[1]) - 1, chosen_gate)
            return 0
        else:
            print("Wrong choice!")

def text_ui():
    while True:
        choice = input("What would you like to do today?\n" \
        "1) Create a circuit\n" \
        "2) Edit a circuit\n" \
        "3) Circuit -> DIMACS\n" \
        "4) Quit\n")
        match choice:
            case '1':
                circuit = circ()
                for i in range(4):
                    circuit.add_var(f'V{i + 1}')
                break
            case '2':
                file_name = input("Provide the save file name (from circuits folder):\n")
                file_path = os.path.join(os.getcwd(), 'circuits', file_name)

                with open(file_path, 'r') as f:
                    save_file = json.loads(f.readline())
                
                circuit = circ(circuit = save_file['circuit'], 
                                vars = save_file['vars'], 
                                exprs = save_file['exprs']
                                )
                break
            case '3':
                file_name = input("Provide the save file name (from circuits folder):\n")
                file_path = os.path.join(os.getcwd(), 'circuits', file_name)

                with open(file_path, 'r') as f:
                    save_file = json.loads(f.readline())
                
                dimacs = to_dimacs(save_file['circuit'], save_file['vars'])
                
                file_name = file_name[6:-5] + '.cnf'
                file_path = os.path.join(os.getcwd(), 'dimacs', file_name)
                with open(file_path, 'w') as f:
                    f.writelines(dimacs)

                print("DIMACS file path: " + file_path) 

            case '4':
                print("Have a nice day!")
                sys.exit()
            case _:
                print("Wrong choice!")

    while True:
        choice = input("1) Add a gate\n" \
        "2) Show details\n" \
        "3) Preview a cirucit\n" \
        "4) Save\n" \
        "5) Exit\n")
        match choice:
            case '1':
                pick_a_gate(circuit)
                print(f"New circuit added: {circuit.object_list[-1]}")

            case '2':
                print(40*'-')
                print(10*'=' + ' VARS ' + 24*'=')
                for i in range(len(circuit.var_list)):
                    print(f"{i + 1}) {circuit.var_list[i]}")

                if circuit.expr_list != '':
                    print(10*'=' + ' CIRCUITS ' + 20*'=')
                    for i in range(len(circuit.expr_list)):
                        print(f"{i + 1}) {circuit.expr_list[i]}")

                if circuit.circuit != '':
                    print(10*'=' + ' FINAL CIRCUIT ' + 15*'=')

                print(40*'-')

            case '3':
                if len(circuit.expr_list) == 0:
                    print("No circuits to preview!")
                else:
                    while True:
                        print("Choose a circuit to preview:")
                        for i in range(len(circuit.expr_list)):
                            print(f"{i + 1}) {circuit.expr_list[i]}")
                        
                        choice = input()
                        if int(choice) > len(circuit.expr_list) or int(choice) < 1:
                            print("Wrong choice!")
                        else:
                            break

                    with schemdraw.Drawing():
                        logicparse(circuit.expr_list[int(choice) - 1]) 
            
            case '4':
                if len(circuit.expr_list) == 0:
                    print("There's nothing to save...")
                else:
                    while True:
                        print("Choose your final circuit:")
                        for i in range(len(circuit.expr_list)):
                            print(f"{i + 1}) {circuit.expr_list[i]}")
                        
                        choice = input()
                        if int(choice) > len(circuit.expr_list) or int(choice) < 1:
                            print("Wrong choice!")
                        else:
                            break
                    
                    circuit.finalize(int(choice) - 1)
                    
                    save_file = {}
                    save_file['circuit'] = circuit.circuit
                    save_file['vars'] = circuit.var_list
                    save_file['exprs'] = circuit.expr_list

                    current_time = str(int(time.time()))
                    file_path = os.path.join(os.getcwd(), 'circuits', 'saved_circuit' + current_time + '.circ')
                    with open(file_path, 'w') as f:
                        f.write(json.dumps(save_file))
                    print("Saved ciruit path: " + file_path)

                    image_path = os.path.join(os.getcwd(), 'circuits', 'circuit_image' + current_time + '.svg')
                    with schemdraw.Drawing(show = False, file = image_path):
                        logicparse(circuit.expr_list[int(choice) - 1]) 
                    print("Saved ciruit diagram path: " + image_path + '\n')
                    
            case '5':
                break
            
            case _:
                print("Wrong choice!")

    return 0

def main():
    text_ui()

if __name__ == "__main__":
    main()