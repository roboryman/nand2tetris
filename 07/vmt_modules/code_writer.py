#!/usr/bin/env python3


"""The CodeWriter Module
Translates given VM commands into Hack ASM code.
"""


from .command import Command


class CodeWriter:
    def __init__(self, out_path):
        self.out_path = out_path
        self._dynamic_labels = {'lt':0, 'eq':0, 'gt':0}
        self._bool_jmp_logic_symbol = ''
        self._asm_file = open(out_path, 'w+')


    def set_file_name(self, file_name):
        """Informs the code writer that the
        translation of a new VM file has started.
        (Possibly for dynamic label making)?
        """


    def write_arithmetic(self, command):
        """Writes the assembly code that is the
        translation of the given arithmetic
        command.
        """
        self._asm_file.write('@SP\n')
        if command in ['neg', 'not']:
            self._asm_file.write('A=M-1\n')
            if command == 'neg':
                self._asm_file.write('M=-M\n')
            elif command == 'not':
                self._asm_file.write('M=!M\n')
        else:
            self._asm_file.write('AM=M-1\n')
            self._asm_file.write('D=M\n')
            self._asm_file.write('A=A-1\n')
            if command == 'add':
                self._asm_file.write('M=M+D\n')
            elif command == 'sub':
                self._asm_file.write('M=M-D\n')
            elif command in ['lt', 'eq', 'gt']:
                self._asm_file.write('D=M-D\n')
                self._asm_file.write('M=0\n')
                if command == 'lt':
                    self._bool_jmp_logic_symbol = 'LTJGE$' + str(self._dynamic_labels['lt'])
                    self._dynamic_labels['lt'] += 1
                    self._asm_file.write('@'+self._bool_jmp_logic_symbol+'\n')
                    self._asm_file.write('D;JGE\n')
                elif command == 'eq':
                    self._bool_jmp_logic_symbol = 'EQJNE$' + str(self._dynamic_labels['eq'])
                    self._dynamic_labels['eq'] += 1
                    self._asm_file.write('@'+self._bool_jmp_logic_symbol+'\n')
                    self._asm_file.write('D;JNE\n')
                elif command == 'gt':
                    self._bool_jmp_logic_symbol = 'GTJLE$' + str(self._dynamic_labels['gt'])
                    self._dynamic_labels['gt'] += 1
                    self._asm_file.write('@'+self._bool_jmp_logic_symbol+'\n')
                    self._asm_file.write('D;JLE\n')
                self._asm_file.write('@SP\n')
                self._asm_file.write('A=M-1\n')
                self._asm_file.write('M=-1\n')
                self._asm_file.write('('+self._bool_jmp_logic_symbol+')\n')
            elif command == 'and':
                self._asm_file.write('M=M&D\n')
            elif command == 'or':
                self._asm_file.write('M=M|D\n')


    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the
        translation of the given command, where
        command is either C_PUSH or C_POP.
        """
        self._asm_file.write('@'+str(index)+'\n')
        self._asm_file.write('D=A\n')
        if command is Command.C_PUSH:
            if segment == 'constant':
                self._asm_file.write('@SP\n')
                self._asm_file.write('AM=M+1\n')
                self._asm_file.write('A=A-1\n')
                self._asm_file.write('M=D\n')
            elif segment in ['local', 'argument', 'this', 'that', 'pointer', 'temp', 'static']:
                if segment == 'local':
                    self._asm_file.write('@LCL\n')
                    self._asm_file.write('A=D+M\n')
                elif segment == 'argument':
                    self._asm_file.write('@ARG\n')
                    self._asm_file.write('A=D+M\n')
                elif segment == 'this':
                    self._asm_file.write('@THIS\n')
                    self._asm_file.write('A=D+M\n')
                elif segment == 'that':
                    self._asm_file.write('@THAT\n')
                    self._asm_file.write('A=D+M\n')
                elif segment == 'pointer':
                    self._asm_file.write('@THIS\n')
                    self._asm_file.write('A=D+A\n')
                elif segment == 'temp':
                    self._asm_file.write('@5\n')
                    self._asm_file.write('A=D+A\n')
                elif segment == 'static':
                    self._asm_file.write('@16\n')
                    self._asm_file.write('A=D+A\n')
                self._asm_file.write('D=M\n')
                self._asm_file.write('@SP\n')
                self._asm_file.write('AM=M+1\n')
                self._asm_file.write('A=A-1\n')
                self._asm_file.write('M=D\n')
            else:
                raise ValueError('Invalid segment ', segment)
                self.close()
        elif command is Command.C_POP:
            if segment in ['local', 'argument', 'this', 'that', 'pointer', 'temp', 'static']:
                if segment == 'local':
                    self._asm_file.write('@LCL\n')
                    self._asm_file.write('D=D+M\n')
                elif segment == 'argument':
                    self._asm_file.write('@ARG\n')
                    self._asm_file.write('D=D+M\n')
                elif segment == 'this':
                    self._asm_file.write('@THIS\n')
                    self._asm_file.write('D=D+M\n')
                elif segment == 'that':
                    self._asm_file.write('@THAT\n')
                    self._asm_file.write('D=D+M\n')
                elif segment == 'pointer':
                    self._asm_file.write('@THIS\n')
                    self._asm_file.write('D=D+A\n')
                elif segment == 'temp':
                    self._asm_file.write('@5\n')
                    self._asm_file.write('D=D+A\n')
                elif segment == 'static':
                    self._asm_file.write('@16\n')
                    self._asm_file.write('D=D+A\n')
                self._asm_file.write('@R13\n')
                self._asm_file.write('M=D\n')
                self._asm_file.write('@SP\n')
                self._asm_file.write('AM=M-1\n')
                self._asm_file.write('D=M\n')
                self._asm_file.write('@R13\n')
                self._asm_file.write('A=M\n')
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
