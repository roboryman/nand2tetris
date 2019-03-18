#!/usr/bin/env python3


"""Hack ASM Assembler (No Symbols)
Assembles the supplied Hack ASM file into its
Hack Machine Language equivalent. If input file
is '{some_file}.asm', output file will be in the
same directory as '{some_file}.hack'. Keep in
mind that this particular assembler does not have
support for symbols, i.e. a mapping of text to
decimal addresses. Please use the other supplied
assembler for this feature ('assembler.py').
"""


import sys
from pathlib import Path
from assembler_modules import code
from assembler_modules.parser import Parser
from assembler_modules.command import Command


__author__ = "Merrick Ryman"
__version__ = "1.0"


def main():
    asm_path = Path(sys.argv[-1])
    if not (asm_path.is_file() and (asm_path.suffix == '.asm')):
        raise IOError('Valid ASM file not supplied.')
    asm_parser = Parser(asm_path)

    hack_path = str(asm_path.parent) + '/' + (asm_path.name[:asm_path.name.find('.')] + '.hack')
    with open(hack_path, 'w+') as hack_file:
        while asm_parser.has_more_commands():
            if asm_parser.command_type() is Command.A_COMMAND:
                hack_file.write(f'{int(asm_parser.symbol()):016b}' + '\n')
            elif asm_parser.command_type() is Command.C_COMMAND:
                comp = ''.join(str(bit) for bit in code.comp(asm_parser.comp()))
                dest = ''.join(str(bit) for bit in code.dest(asm_parser.dest()))
                jump = ''.join(str(bit) for bit in code.jump(asm_parser.jump()))
                hack_file.write('111' + comp + dest + jump + '\n')
            elif asm_parser.command_type() is Command.L_COMMAND:
                hack_file.close()
                print('Encountered an L_COMMAND. This version of the assembler does not support symbols!')
                raise NotImplementedError
            else:
                hack_file.close()
                raise ValueError('This command type does not exist.')


if __name__ == "__main__":
    main()
