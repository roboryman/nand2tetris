#!/usr/bin/env python3


"""The Parser Module
Encapsulates access to the input code (ASM file). Reads
a Hack ASM command, parses it, and provides convenient access
to the command's components (fields and symbols). In addition,
removes all whitespace, comments, and empty lines.

Version 1.0: Standard Parser Module as described in TECS.
Version 2.0: (3/18/19) Added support for macro-commands, for
             example: 'M=D[123]' is equivalent to '@123'
             followed by 'M=D'. Of course, this also works
             for symbols: 'M=D[foo]' == '@foo' ... 'M=D'.
"""


import re
from .command import Command


__author__ = "Merrick Ryman"
__version__ = "2.0"


class Parser:
    def __init__(self, asm_path):
        self.asm_path = asm_path
        self._asm_commands = None
        self._asm_command_current = None
        self._asm_commands_iter = None
        self._parse_asm_file()
        self.reset_iter()


    def _parse_asm_file(self):
        """Parse the Hack ASM file into memory so it
        is easier to work with. Remove comments, spaces,
        empty lines, etc, so all that remains are commands
        (and pseudo-commands). Also, create an iterable
        to get the next command.
        """
        with open(self.asm_path, 'r') as asm_file:
            lines = asm_file.readlines()
            lines = list(map(lambda x: x[:x.find('//')].replace(' ', ''), lines))
            lines = list(filter(None, lines))
            self._asm_commands = self._split_macro_commands(lines)


    def _split_macro_commands(self, commands):
        """Splits all macro-commands found in the ASM
        source into its respective A-Instruction and
        C-Instruction parts. Returns the formatted
        list (source)
        """
        formatted_list = []
        for x in commands:
            macro = re.findall('(?<=\[).+?(?=\])', x)
            if len(macro) > 0:
                formatted_list.append( ('@' + macro[0]) )
                formatted_list.append(x[:x.find('[')])
            else:
                formatted_list.append(x)
        return formatted_list


    def reset_iter(self):
        """Resets (or sets) the iterator object that
        iterates over the asm commands. Useful for
        re-parsing the file as necessary.
        """
        self._asm_commands_iter = iter(self._asm_commands)


    def has_more_commands(self):
        """Are there any more commands in the file?
        Returns True if command iterable successfully
        gets the next command. Otherwise, return False.
        """
        try:
            self._asm_command_current = next(self._asm_commands_iter)
            return True
        except StopIteration:
            return False


    def command_type(self):
        """Returns the type of the current ASM command.
        If command starts with '@', this is an A-Instruction
        command. If command starts with '(', this is an
        L-Instruction command. Otherwise, this is a
        C-Instruction command.
        """
        return {
            '@': Command.A_COMMAND,
            '(': Command.L_COMMAND
        }.get(self._asm_command_current[0], Command.C_COMMAND)


    def symbol(self):
        """Returns the symbol or decimal constant xyz
        of the current command @xyz or (xyz). Should
        only be called when the command type is
        A_COMMAND or L_COMMAND.
        """
        return re.sub('[@()]', '', self._asm_command_current)


    def is_dest_c_instruction(self):
        """ Returns True if the dest mnemonic is
        present in the current C_COMMAND. Otherwise,
        return False because this is a jump. Should
        only be called when the command type is
        C_COMMAND.
        """
        if self._asm_command_current.find('=') < 0: # '=' not found
            return False
        return True


    def dest(self):
        """Returns the dest mnemonic in the current
        C_COMMAND (8 possibilities). Should only be
        called when the command type is C_COMMAND.
        """
        if self.is_dest_c_instruction():
            return self._asm_command_current[:self._asm_command_current.find('=')]
        return 'null'


    def comp(self):
        """Returns the comp mnemonic in the current
        C_COMMAND (28 possibilities). Should only be
        called when the command type is C_COMMAND.
        """
        if self.is_dest_c_instruction():
            return self._asm_command_current[self._asm_command_current.find('=')+1:]
        return self._asm_command_current[:self._asm_command_current.find(';')]


    def jump(self):
        """Returns the jump mnemonic in the current
        C_COMMAND (8 possibilities). Should only be
        called when the command type is C_COMMAND.
        """
        if self.is_dest_c_instruction():
            return 'null'
        return self._asm_command_current[self._asm_command_current.find(';')+1:]
