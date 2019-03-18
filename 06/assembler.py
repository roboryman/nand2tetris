#!/usr/bin/env python3


"""Hack ASM Assembler
Assembles the supplied Hack ASM file into its
Hack Machine Language equivalent. If input file
is '{some_file}.asm', output file will be in the
same directory as '{some_file}.hack'.
"""


import sys
from pathlib import Path
from assembler_modules import code
from assembler_modules.parser import Parser
from assembler_modules.command import Command
from assembler_modules.symbol_table import SymbolTable


__author__ = "Merrick Ryman"
__version__ = "1.0"


def main():
    asm_path = Path(sys.argv[-1])
    if not (asm_path.is_file() and (asm_path.suffix == '.asm')):
        raise IOError('Valid ASM file not supplied.')
    hack_path = str(asm_path.parent) + '/' + (asm_path.name[:asm_path.name.find('.')] + '.hack')
    asm_parser = Parser(asm_path)
    asm_symbols = SymbolTable()

    #Initialize Symbol Table
    for i in range(0,16):
        asm_symbols.add_entry('R'+str(i), i)
    asm_symbols.add_entry('SP', 0)
    asm_symbols.add_entry('LCL', 1)
    asm_symbols.add_entry('ARG', 2)
    asm_symbols.add_entry('THIS', 3)
    asm_symbols.add_entry('THAT', 4)
    asm_symbols.add_entry('SCREEN', 16384)
    asm_symbols.add_entry('KBD', 24576)

    #First Pass - Build label symbol maps
    ROM_address = 0
    while asm_parser.has_more_commands():
        if asm_parser.command_type() is Command.A_COMMAND:
            ROM_address += 1
        elif asm_parser.command_type() is Command.C_COMMAND:
            ROM_address += 1
        elif asm_parser.command_type() is Command.L_COMMAND:
            asm_symbols.add_entry(asm_parser.symbol(), ROM_address)
        else:
            raise ValueError('This command type does not exist.')

    #Second Pass - Build variable symbol maps and assemble.
    asm_parser.reset_iter()
    RAM_address = 16
    with open(hack_path, 'w+') as hack_file:
        while asm_parser.has_more_commands():
            if asm_parser.command_type() is Command.A_COMMAND:
                symbol = asm_parser.symbol()
                try:
                    symbol = int(symbol)
                except ValueError:
                    if asm_symbols.contains(symbol):
                        symbol = asm_symbols.get_address(symbol)
                    else:
                        asm_symbols.add_entry(symbol, RAM_address)
                        symbol = RAM_address
                        RAM_address += 1
                hack_file.write(f'{symbol:016b}' + '\n')
            elif asm_parser.command_type() is Command.C_COMMAND:
                comp = ''.join(str(bit) for bit in code.comp(asm_parser.comp()))
                dest = ''.join(str(bit) for bit in code.dest(asm_parser.dest()))
                jump = ''.join(str(bit) for bit in code.jump(asm_parser.jump()))
                hack_file.write('111' + comp + dest + jump + '\n')
            elif asm_parser.command_type() is Command.L_COMMAND:
                continue
            else:
                hack_file.close()
                raise ValueError('This command type does not exist.')


if __name__ == "__main__":
    main()
