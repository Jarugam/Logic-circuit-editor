from circuit import circ
import schemdraw
from schemdraw.parsing import logicparse
import sys

def text_ui():
    
    while True:
        choice = input("What would you like to do today:\n" \
        "1) Create a circuit\n" \
        "2) Edit a circuit (t.b.i.)\n" \
        "3) Quit\n")
        if choice == '1':
            circuit = circ()
            for i in range(4):
                circuit.add_var(f'V{i+1}')
            break
        elif choice == '3':
            sys.exit()
        else:
            print("Wrong choice!")

def main():
    text_ui()

if __name__ == "__main__":
    main()