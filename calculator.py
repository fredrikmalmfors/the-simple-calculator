import sys


"""Register object representing a register in the calculator.

Contains the name of the register, along with a list of instructions (add, subtract...)
to be performed on this register.

"""
registers = set()


"""Allowed operations

"""
operations = ["add", "subtract", "multiply"]


class Register:
    """Register object representing a register in the calculator.

    Contains the name of the register, along with lists of instructions (add, subtract...)
    to be performed on this register.

    The active_instructions list contains the instructions that has not yet
    been executed in the current print register call. It is used to handle circular dependencies of registers.

    """

    def __init__(self, name):
        self.name = name
        self.active_instructions = []
        self.all_instructions = []
        self.register_value = 0

    def add_instruction(self, operation, value):
        """Appends an instruction [operation, value] to this registers list of instructions.

        """
        self.all_instructions.append([operation, value])

    def reset_instructions(self):
        """ Called before a print register call, to say that all instructions must be evaluated again.

        """
        self.active_instructions = self.all_instructions

    def evaluate(self):
        """Evaluates the value of the register by executing (calculating) the instructions in order.

        If the value given in the instruction is a register, then this function is called in the
        corresponding Register object in a recursive manner.

        Returns the final value after all instructions has been executed.

        """

        while len(self.active_instructions) > 0:
            inst = self.active_instructions.pop(0)
            operation = inst[0]
            value = inst[1]

            # value is number.
            if value.isdecimal():
                self.register_value = calculate(self.register_value, operation, int(value))

            # value is register.
            else:
                for register in registers:
                    if register.name == value:
                        self.register_value = calculate(self.register_value, operation, register.evaluate())
                        break
                else:
                    print("The register " + value + " could not be found")

        return self.register_value


def find_register(register_name):
    """Finds and returns the register that matches the given name,
    else returns False.

    """
    return next((reg for reg in registers if reg.name == register_name), False)


def new_instruction(register_name, operation, value):
    """If register_name is new, new_entry creates a new Register object and adds
    it to the registers set.

    Then adds the instruction to the register.

    """
    register = find_register(register_name)
    if not register:
        register = Register(register_name)
        registers.add(register)

    register.add_instruction(operation, value)


def print_register(register_name):
    """Prints the value of the given register by calling evaluate()

    """

    register = find_register(register_name)
    if not register:
        print("No register with name: " + register_name)
    else:
        reset_all_register_instructions()
        print(register.evaluate())


def reset_all_register_instructions():
    for register in registers:
        register.reset_instructions()


def calculate(register_value, operation, value):
    """Performs given operation on register_value with given value.

    Returns the result.

    PS. Here you might want to add additional operations, e.g division.

    """
    if operation == "add":
        register_value += value
    elif operation == "subtract":
        register_value -= value
    elif operation == "multiply":
        register_value *= value
    else:
        print("invalid operation: " + operation)
    return register_value


def read_file(file_path):
    """Reads given file line by line.

    Returns a list of strings. One string per line.

    """
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()
    return lines


def execute_line(line_str):
    """Parses and executes a given line.

    """

    line = line_str.lower().split()

    # print <register>
    if (line[0] == "print") and (len(line) == 2):
        print_register(line[1])

    # <register> <operation> <value>
    elif (line[1] in operations) and (len(line) == 3):
        new_instruction(line[0], line[1], line[2])

    # Invalid line will be ignored.
    else:
        print("Invalid input: " + line_str)


def main():
    """Reads lines either from console or from file if <file_path> is given as an argument.

    It then executes all the read lines.

    """

    lines_to_execute = []

    # If an argument was given: read from file.
    if len(sys.argv) > 1:
        try:
            lines_to_execute = read_file(sys.argv[1])
        except FileNotFoundError:
            print("File '%s' could not be read from" % sys.argv[1])

    # Else, read input from console.
    else:
        while True:
            input_line = input()
            # Stop if input is 'quit', else append line to lines.
            if not input_line.lower() == "quit":
                lines_to_execute.append(input_line)
            else:
                break

    # Execute all read lines.
    for line in lines_to_execute:
        if not line.lower() == "quit":
            execute_line(line)
        else:
            break


main()

