#!/usr/bin/env python3


"""The CodeWriter Module
Translates given VM commands into Hack ASM code.
Implements: + Stage I (Arithmetic and Logic Commands)
            + Stage II: (Memory Access Commands)
            + Stage III: (Program Flow Commands)
            + Stage IV: (Function Calling Commands)
"""


from .command import Command


__author__ = "Merrick Ryman"
__version__ = "2.0"


class CodeWriter:
    def __init__(self, out_path):
        self.out_path = out_path
        self._vm_file = None
        self._asm_file = open(out_path, 'w+')
        self._bool_jmp_logic_symbol = ''
        self._dynamic_labels = {'lt': 0, 'eq': 0, 'gt': 0, 'ret': 0}

    def _write_asm_commands(self, asm_commands):
        self._asm_file.writelines('{}\n'.format(x) for x in asm_commands)

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
        out = []
        if command in ['neg', 'not']:
            out.append('A=M-1[SP]')
            if command == 'neg':
                out.append('M=-M')
            elif command == 'not':
                out.append('M=!M')
        else:
            out.extend(['AM=M-1[SP]', 'D=M', 'A=A-1'])
            if command == 'add':
                out.append('M=M+D')
            elif command == 'sub':
                out.append('M=M-D')
            elif command in ['lt', 'eq', 'gt']:
                out.extend(['D=M-D', 'M=0'])
                if command == 'lt':
                    self._bool_jmp_logic_symbol = 'LTJGE${}'.format(self._dynamic_labels['lt'])
                    self._dynamic_labels['lt'] += 1
                    out.append('D;JGE[{}]'.format(self._bool_jmp_logic_symbol))
                elif command == 'eq':
                    self._bool_jmp_logic_symbol = 'EQJNE${}'.format(self._dynamic_labels['eq'])
                    self._dynamic_labels['eq'] += 1
                    out.append('D;JNE[{}]'.format(self._bool_jmp_logic_symbol))
                elif command == 'gt':
                    self._bool_jmp_logic_symbol = 'GTJLE${}'.format(self._dynamic_labels['gt'])
                    self._dynamic_labels['gt'] += 1
                    out.append('D;JLE[{}]'.format(self._bool_jmp_logic_symbol))
                out.extend(['A=M-1[SP]', 'M=-1', '({})'.format(self._bool_jmp_logic_symbol)])
            elif command == 'and':
                out.append('M=M&D')
            elif command == 'or':
                out.append('M=M|D')
        self._write_asm_commands(out)

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the
        translation of the given command, where
        command is either C_PUSH or C_POP.
        """
        out = []
        out.append('D=A[{}]'.format(index))
        if command is Command.C_PUSH:
            if segment == 'constant':
                out.extend(['AM=M+1[SP]', 'A=A-1', 'M=D'])
            elif segment in ['local', 'argument', 'this', 'that',
                             'pointer', 'temp', 'static']:
                if segment == 'local':
                    out.append('A=D+M[LCL]')
                elif segment == 'argument':
                    out.append('A=D+M[ARG]')
                elif segment == 'this':
                    out.append('A=D+M[THIS]')
                elif segment == 'that':
                    out.append('A=D+M[THAT]')
                elif segment == 'pointer':
                    out.append('A=D+A[THIS]')
                elif segment == 'temp':
                    out.append('A=D+A[5]')
                elif segment == 'static':
                    out.append('@{}.{}'.format(self._vm_file, index))
                out.extend(['D=M', 'AM=M+1[SP]', 'A=A-1', 'M=D'])
            else:
                raise ValueError('Invalid segment ', segment)
                self.close()
        elif command is Command.C_POP:
            if segment in ['local', 'argument', 'this', 'that',
                           'pointer', 'temp', 'static']:
                if segment == 'local':
                    out.append('D=D+M[LCL]')
                elif segment == 'argument':
                    out.append('D=D+M[ARG]')
                elif segment == 'this':
                    out.append('D=D+M[THIS]')
                elif segment == 'that':
                    out.append('D=D+M[THAT]')
                elif segment == 'pointer':
                    out.append('D=D+A[THIS]')
                elif segment == 'temp':
                    out.append('D=D+A[5]')
                elif segment == 'static':
                    out.append('D=A[{}.{}]'.format(self._vm_file, index))
                out.extend(['M=D[R13]', 'AM=M-1[SP]', 'D=M', 'A=M[R13]', 'M=D'])
            else:
                raise ValueError('Invalid segment ', segment)
                self.close()
        else:
            raise ValueError('Invalid command ', command)
            self.close()
        self._write_asm_commands(out)

    def write_init(self):
        """Writes Hack ASM that effects the VM
        initialization, also called bootstrap
        code. This code must be placed at the
        beginning of the output file.
        """
        self._write_asm_commands(['D=A[256]', 'M=D[SP]'])
        self.write_call('Sys.init', 0)

    def write_label(self, label):
        """Writes Hack ASM that effects the
        label command.
        """
        self._write_asm_commands(['({})'.format(label)])

    def write_goto(self, label):
        """Writes Hack ASM that effects the
        goto command.
        """
        self._write_asm_commands(['0;JMP[{}]'.format(label)])

    def write_if(self, label):
        """Writes Hack ASM that effects the
        if-goto command.
        """
        self._write_asm_commands(['AM=M-1[SP]', 'D=M',
                                  'D;JNE[{}]'.format(label)])

    def _push_pointer_value(self, pointer_name):
        """Push the value of a special pointer,
        given the name (LCL, ARG, THIS, THAT).
        """
        self._write_asm_commands(['D=M[{}]'.format(pointer_name), 'AM=M+1[SP]',
                                  'A=A-1', 'M=D'])

    def write_call(self, function_name, num_args):
        """Writes Hack ASM that effects the
        call command. Ultimately, it sets up
        the pointers and working stack for
        the subroutine.
        """
        return_label = '{}$ret.{}'.format(function_name, self._dynamic_labels['ret'])
        self._dynamic_labels['ret'] += 1
        self._write_asm_commands(['D=A[{}]'.format(return_label), 'AM=M+1[SP]',
                                  'A=A-1', 'M=D'])
        self._push_pointer_value('LCL')
        self._push_pointer_value('ARG')
        self._push_pointer_value('THIS')
        self._push_pointer_value('THAT')
        self._write_asm_commands(['D=M[SP]', 'D=D-A[{}]'.format(num_args),
                                  'D=D-A[5]', 'M=D[ARG]',
                                  'D=M[SP]', 'M=D[LCL]',
                                  '0;JMP[{}]'.format(function_name)])
        self.write_label(return_label)

    def write_return(self):
        """Writes Hack ASM that effects the
        return command. Ultimately, it sets
        back up the pointers for the caller.
        """
        self._write_asm_commands(['D=M[LCL]', 'M=D[R13]',
                                  'D=D-A[5]', 'A=D', 'D=M', 'M=D[R14]',
                                  'AM=M-1[SP]', 'D=M', 'A=M[ARG]', 'M=D',
                                  'D=M+1[ARG]', 'M=D[SP]',
                                  'D=M-1[R13]', 'A=D', 'D=M', 'M=D[THAT]',
                                  'D=A[2]', 'D=M-D[R13]', 'A=D', 'D=M', 'M=D[THIS]',
                                  'D=A[3]', 'D=M-D[R13]', 'A=D', 'D=M', 'M=D[ARG]',
                                  'D=A[4]', 'D=M-D[R13]', 'A=D', 'D=M', 'M=D[LCL]',
                                  'A=M[R14]', '0;JMP'])

    def write_function(self, function_name, num_locals):
        """Writes Hack ASM that effects the
        function command. Create a label
        to refer to the function in Hack ASM,
        and allocate space for local variables.
        """
        self.write_label(function_name)
        for x in range(0, num_locals):
            self.write_push_pop(Command.C_PUSH, 'constant', 0)

    def close(self):
        """Closes the output Hack ASM file.
        """
        self._asm_file.close()
