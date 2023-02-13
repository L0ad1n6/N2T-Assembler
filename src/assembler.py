import processor
from lookup_tables import COMP_TABLE, JUMP_TABLE


def assemble(instructions):
    """
    Assembles the resolved assembly instructions into binary.

        Parameters:
            instructions (str): Array of instructions with no symbolic references

        Return:
            binary (list[str]): Array of binary strings
    """
    for instruction in instructions:
        if "@" in instruction:
            # First bit is the bit that determines whether it is A or C, not part of value
            yield processor.to_bin(instruction[1:], min_bits=16)
            continue

        dest_bits = "000"
        jump_bits = "000"
        comp = None

        # Destination Processing
        if "=" in instruction:
            [dest, comp] = instruction.split("=")

            dest_bits_int = 0
            if "M" in dest: dest_bits_int += 1 # +001
            if "D" in dest: dest_bits_int += 2 # +010
            if "A" in dest: dest_bits_int += 4 # +100

            dest_bits = processor.to_bin(dest_bits_int, min_bits=3)

        # Jump Processing
        elif ";" in instruction:
            [comp, jump] = instruction.split(";")
            jump_bits = JUMP_TABLE[jump] # Look up jump bits from JUMP_TABLE
        
        # Comparison Processing
        comp_bits = COMP_TABLE[comp] # Look up Comparison bits from COMP_TABLE

        yield f"111{comp_bits}{dest_bits}{jump_bits}" # Yield concatenated result of bits