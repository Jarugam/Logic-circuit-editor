from circuit import circ
import schemdraw
from schemdraw.parsing import logicparse
import sys

def pick_a_gate(circuit):
    while True:
        choice1 = input("Choose a gate to add:\n" \
        "1) not\n" \
        "2) and\n" \
        "3) or\n" \
        "4) xor\n")

        if choice1 == '1':
            while True:
                print("Choose an object:\n")
                circuit.print_objects()
                choice2 = input()
                if int(choice2) + 1 > len(circuit.object_list) or int(choice2) < 0:
                    print("Wrong choice!")
                else:
                    break

            circuit.not_gate(int(choice2))
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
                if int(choice2) + 1 > len(circuit.object_list) or int(choice2) < 0:
                    print("Wrong choice!")
                else:
                    multi_choice.append(choice2)
                    count += 1
            
            circuit.multi_gate(int(multi_choice[0]), int(multi_choice[1]), chosen_gate)
            return 0
        else:
            print("Wrong choice!")

def text_ui():
    while True:
        choice = input("What would you like to do today?\n" \
        "1) Create a circuit\n" \
        "2) Edit a circuit (t.b.i.)\n" \
        "3) Quit\n")
        match choice:
            case '1':
                circuit = circ()
                for i in range(4):
                    circuit.add_var(f'V{i}')
                break
            case '2':
                pass
            case '3':
                print("Have a nice day!")
                sys.exit()
            case _:
                print("Wrong choice!")

    while True:
        choice = input("1) Add a gate\n" \
        "2) Preview a cirucit\n" \
        "3) Save an exit\n")
        match choice:
            case '1':
                pick_a_gate(circuit)
                print(f"New circuit added: {circuit.object_list[-1]}")
            case '2':
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
            case '3':
                break
            case _:
                print("Wrong choice!")

    return 0

def main():
    text_ui()

if __name__ == "__main__":
    main()