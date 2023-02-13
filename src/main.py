import processor
import assembler
import debug
import sys


def main():
    file_path = sys.argv[1]

    symbolic_asm = processor.load_asm(file_path)
    asm = processor.resolve_symbols(symbolic_asm)

    binary = assembler.assemble(asm)
    processor.store_asm(binary, file_path)


if __name__ == '__main__':
    main()
