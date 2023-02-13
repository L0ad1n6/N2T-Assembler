import processor

def symbol_removal(instructions, path):
    """Checks resolved instructions against given symbolless code"""
    test_instructions = processor.load_asm(path.replace(path))
    for i, (inst, test_inst) in enumerate(zip(instructions, test_instructions)):
        print(f"{i}: {inst}:{' '*(7-len(inst))} {test_inst}")
        if inst != test_inst:
            input()
