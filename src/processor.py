from lookup_tables import SYMBOL_TABLE

def resolve_symbols(instructions):
    """
    Resolves all symbols to addresses

        Parameters:
            instructions (list[str]): Symbolic ASM instructions

        Return:
            instructions (list[str]): Array of string instructions, free of labels and symbolic references
    """
    smallest_free_register = 16
    lines = 0
    L_instructions = []

    # Add all the labels to the symbol table
    for i, instruction in enumerate(instructions):

        if not instruction.startswith("("):
            lines += 1

        # Technically this check is unnecessary since every label should 
        # appear exactly once, however it is useful to keep this check 
        # for the possible expansion of error handling in the future
        elif (label := instruction[1:-1]) not in SYMBOL_TABLE:
            SYMBOL_TABLE[label] = lines
            L_instructions.append(i) # Appends to array for future deletion
            # I'm sure there is a way to do this inside this look but all of 
            # my attempts has lead to inexplicable failure
            
    # Filter out all the labels from the instructions
    for i in reversed(L_instructions): instructions.pop(i)

    # Substitute symbolic references and variables with resolved addresses
    for i, instruction in enumerate(instructions):
        if not instruction.startswith("@"): continue # If it is a C instructions there can't be symbolic references
        if (variable := instruction[1:]).isdigit(): continue # Symbol starting with number is a syntax error

        # Bind variable to register if not in symbol table
        if variable not in SYMBOL_TABLE:
            SYMBOL_TABLE[variable] = smallest_free_register
            smallest_free_register += 1

        # Replace symbolic reference with resolved instruction
        instructions[i] = f"@{SYMBOL_TABLE[variable]}"

    return instructions
    

def load_asm(path):
    """
    Loads raw ASM file into program

        Parameters:
            path (str): Path to ASM file

        Return:
            instructions (list[str]): Array of string instructions, pruned of comments and spaces
    """

    with open(path, "r") as f:
        instructions = f\
                .read()\
                .replace("\r", "")\
                .replace(" ", "")\
                .split("\n") # Splits into individual trimmed instructions

        # Removes Comments
        instructions = [
            instruction\
                .split("//")[0]\
                .strip() 
                for instruction in instructions
        ] 
    return list(filter(lambda x: x != "", instructions))


def store_asm(instructions, path):
    """
    Stores binary instructions into desired path, will override or create new file if required.

        Parameters:
            instructions (list[str]): List of binary instructions in the form of strings
            path (str): Path to ASM file
    """
    with open(path.replace(".asm", ".hack"), "w+") as f:
        f.write("\n".join(instructions))


def to_bin(value, min_bits=0):
    """
    Converts integer to binary string

    Convert dest bits to binary, 
    bin return '0bXXXXXXX...' so out[2:] strips first two characters
    bin returns binary representation with minimum bits .zfill in order to complete to min_bits bits

        Parameters:
            value (int): Integer value to be turned into binary string
            min_bits (int): Minimum return bits (determines how much the output will be padded)

        Returns:
            bin_string (str): 
    """
    return bin(int(value))[2:].zfill(min_bits)
