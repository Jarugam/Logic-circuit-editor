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
                print("Choose what to NOT:\n")
                circuit.print_objects()
                choice2 = input()
                if int(choice2) + 1 > len(circuit.var_list) | int(choice2) < 0:
                    print("Wrong choice!")
                else:
                    break

            circuit.not_gate(int(choice2))
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
                    circuit.add_var(f'V{i+1}')
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
        "2) Visualize a cirucit\n" \
        "3) Save an exit\n")
        match choice:
            case '1':
                pick_a_gate(circuit)
                print(circuit.expr_list)
            case '2':
                pass
            case '3':
                break
            case _:
                print("Wrong choice!")

def main():
    text_ui()

if __name__ == "__main__":
    main()