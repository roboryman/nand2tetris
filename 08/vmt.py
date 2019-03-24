#!/usr/bin/env python3


"""Virtual Machine Translator
Translates the VM code (either a single .vm file
or a directory of .vm files) into its Hack ASM
equivalent, which can then be assembled and run
on Hack.
"""


import sys
from pathlib import Path
from vmt_modules.parser import Parser
from vmt_modules.command import Command
from vmt_modules.code_writer import CodeWriter


__author__ = "Merrick Ryman"
__version__ = "2.0"


def main():
    vm_path = Path(sys.argv[-1])
    vm_glob = []
    asm_path = (str(vm_path.parent)
                + '/'
                + (vm_path.name[:vm_path.name.find('.')]
                + '.asm'))

    if vm_path.name == 'vmt.py':
        raise IOError('Please supply a .vm source file/directory.')
    if vm_path.is_dir():
        vm_glob = list(vm_path.glob('*.vm'))
        if not vm_glob:
            raise RuntimeError('No *.vm files found in supplied directory.')
        asm_path = (str(vm_path.parent)
                    + '/' + vm_path.name
                    + '/' + vm_path.name
                    + '.asm')
    elif vm_path.is_file():
        if vm_path.suffix != '.vm':
            raise IOError('Valid VM source file not supplied.')
        vm_glob.append(vm_path)

    code_writer = CodeWriter(asm_path)
    code_writer.write_init()
    for vm_file in vm_glob:
        code_writer.set_file_name(vm_file.name)
        func_name = '$'
        vm_parser = Parser(vm_file)
        while vm_parser.has_more_commands():
            if vm_parser.command_type() is Command.C_ARITHMETIC:
                code_writer.write_arithmetic(vm_parser.arg1())
            elif vm_parser.command_type() is Command.C_PUSH:
                code_writer.write_push_pop(Command.C_PUSH,
                                           vm_parser.arg1(),
                                           vm_parser.arg2())
            elif vm_parser.command_type() is Command.C_POP:
                code_writer.write_push_pop(Command.C_POP,
                                           vm_parser.arg1(),
                                           vm_parser.arg2())
            elif vm_parser.command_type() is Command.C_LABEL:
                code_writer.write_label(func_name+'$'+vm_parser.arg1())
            elif vm_parser.command_type() is Command.C_GOTO:
                code_writer.write_goto(func_name+'$'+vm_parser.arg1())
            elif vm_parser.command_type() is Command.C_IF:
                code_writer.write_if(func_name+'$'+vm_parser.arg1())
            elif vm_parser.command_type() is Command.C_FUNCTION:
                code_writer.write_function(vm_parser.arg1(), vm_parser.arg2())
                func_name = vm_parser.arg1()
            elif vm_parser.command_type() is Command.C_CALL:
                code_writer.write_call(vm_parser.arg1(), vm_parser.arg2())
            elif vm_parser.command_type() is Command.C_RETURN:
                code_writer.write_return()
            else:
                raise ValueError('Command not recognized: ',
                                 vm_parser.command_type())
    code_writer.close()

    print('[=>] IN .vm file(s):')
    print(*vm_glob, sep='\n')
    print('[<=] OUT .asm file:\n' + asm_path)


if __name__ == "__main__":
    main()
