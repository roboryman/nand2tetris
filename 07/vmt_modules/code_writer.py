#!/usr/bin/env python3


"""The CodeWriter Module
Translates given VM commands into Hack ASM code.
Implements: + Stage I (Arithmetic and Logic Commands)
            + Stage II: (Memory Access Commands)
"""


from .command import Command


__author__ = "Merrick Ryman"
__version__ = "1.2"


class CodeWriter:
    def __init__(self, out_path):
        self.out_path = out_path
        self._dynamic_labels = {'lt':0, 'eq':0, 'gt':0}
        self._bool_jmp_logic_symbol = ''
        self._asm_file = open(out_path, 'w+')
        self._vm_file = None


    def set_file_name(self, file_name):
        """Informs the code writer that the
        translation of a new VM file has started.
        """
        self._vm_file = file_name[:file_name.find('.')]


    def write_arithmetic(self, command):
        """Writes the assembly code that is the
        translation of the given arithmetic
        command.
        """
        if command in ['neg', 'not']:
            self._asm_file.write('A=M-1[SP]\n')
            if command == 'neg': self._asm_file.write('M=-M\n')
            elif command == 'not': self._asm_file.write('M=!M\n')
        else:
            self._asm_file.write('AM=M-1[SP]\n')
            self._asm_file.write('D=M\n')
            self._asm_file.write('A=A-1\n')
            if command == 'add': self._asm_file.write('M=M+D\n')
            elif command == 'sub': self._asm_file.write('M=M-D\n')
            elif command in ['lt', 'eq', 'gt']:
                self._asm_file.write('D=M-D\n')
                self._asm_file.write('M=0\n')
                if command == 'lt':
                    self._bool_jmp_logic_symbol = 'LTJGE$' + str(self._dynamic_labels['lt'])
                    self._dynamic_labels['lt'] += 1
                    self._asm_file.write('D;JGE['+self._bool_jmp_logic_symbol+']\n')
                elif command == 'eq':
                    self._bool_jmp_logic_symbol = 'EQJNE$' + str(self._dynamic_labels['eq'])
                    self._dynamic_labels['eq'] += 1
                    self._asm_file.write('D;JNE['+self._bool_jmp_logic_symbol+']\n')
                elif command == 'gt':
                    self._bool_jmp_logic_symbol = 'GTJLE$' + str(self._dynamic_labels['gt'])
                    self._dynamic_labels['gt'] += 1
                    self._asm_file.write('D;JLE['+self._bool_jmp_logic_symbol+']\n')
                self._asm_file.write('A=M-1[SP]\n')
                self._asm_file.write('M=-1\n')
                self._asm_file.write('('+self._bool_jmp_logic_symbol+')\n')
            elif command == 'and': self._asm_file.write('M=M&D\n')
            elif command == 'or': self._asm_file.write('M=M|D\n')


    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the
        translation of the given command, where
        command is either C_PUSH or C_POP.
        """
        self._asm_file.write('D=A['+str(index)+']\n')
        if command is Command.C_PUSH:
            if segment == 'constant':
                self._asm_file.write('AM=M+1[SP]\n')
                self._asm_file.write('A=A-1\n')
                self._asm_file.write('M=D\n')
            elif segment in ['local', 'argument', 'this', 'that', 'pointer', 'temp', 'static']:
                if segment == 'local': self._asm_file.write('A=D+M[LCL]\n')
                elif segment == 'argument': self._asm_file.write('A=D+M[ARG]\n')
                elif segment == 'this': self._asm_file.write('A=D+M[THIS]\n')
                elif segment == 'that': self._asm_file.write('A=D+M[THAT]\n')
                elif segment == 'pointer': self._asm_file.write('A=D+A[THIS]\n')
                elif segment == 'temp': self._asm_file.write('A=D+A[5]\n')
                elif segment == 'static': self._asm_file.write('@'+self._vm_file+'.'+str(index)+'\n')
                self._asm_file.write('D=M\n')
                self._asm_file.write('AM=M+1[SP]\n')
                self._asm_file.write('A=A-1\n')
                self._asm_file.write('M=D\n')
            else:
                raise ValueError('Invalid segment ', segment)
                self.close()
        elif command is Command.C_POP:
            if segment in ['local', 'argument', 'this', 'that', 'pointer', 'temp', 'static']:
                if segment == 'local': self._asm_file.write('D=D+M[LCL]\n')
                elif segment == 'argument': self._asm_file.write('D=D+M[ARG]\n')
                elif segment == 'this': self._asm_file.write('D=D+M[THIS]\n')
                elif segment == 'that': self._asm_file.write('D=D+M[THAT]\n')
                elif segment == 'pointer': self._asm_file.write('D=D+A[THIS]\n')
                elif segment == 'temp': self._asm_file.write('D=D+A[5]\n')
                elif segment == 'static': self._asm_file.write('D=A['+self._vm_file+'.'+str(index)+']\n')
                self._asm_file.write('M=D[R13]\n')
                self._asm_file.write('AM=M-1[SP]\n')
                self._asm_file.write('D=M\n')
                self._asm_file.write('A=M[R13]\n')
                self._asm_file.write('M=D\n')
            else:
                raise ValueError('Invalid segment ', segment)
                self.close()
        else:
            raise ValueError('Invalid command ', command)
            self.close()


    def close(self):
        """Closes the output Hack ASM file.
        """
        self._asm_file.close()
