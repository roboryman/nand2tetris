#!/usr/bin/env python3


"""The Parser Module
Handles the parsing of a single .vm file, and encapsulates
access to the input code. Overall: reads VM commands, parses them,
and provides convenient access to their components. In addition,
remove all white space and comments.
"""


from .command import Command


__author__ = "Merrick Ryman"
__version__ = "1.0"


class Parser:
    def __init__(self, in_path):
        self.in_path = in_path
        self._vm_commands = None
        self._vm_command_current = None
        self._vm_commands_iter = None
        self._parse_vm_file()
        self._reset_iter()

    def _parse_vm_file(self):
        """Parse the Hack ASM file into memory so it
        is easier to work with. Remove comments, spaces,
        empty lines, etc, so all that remains are commands
        (and pseudo-commands). Also, create an iterable
        to get the next command.
        """
        with open(self.in_path, 'r') as vm_file:
            lines = vm_file.readlines()
            lines = list(map(lambda x: x[:x.find('//')], lines))
            lines = list(filter(None, lines))
            self._vm_commands = self._format_vm_commands(lines)

    def _format_vm_commands(self, commands):
        """Format a list of VM commands; in other words,
        break up the input arguments. Returns the
        commands in the form of a list of dictionaries.
        Each dictionary pertains to its particular
        command.
        """
        formatted_list = []
        for command in commands:
            args_dict = {'name': None, 'arg1': None, 'arg2': None}
            args = command.split()
            args_dict['name'] = args[0]
            if len(args) == 2 or len(args) == 3:
                args_dict['arg1'] = args[1]
            if len(args) == 3:
                args_dict['arg2'] = args[2]
            formatted_list.append(args_dict)
        return formatted_list

    def _reset_iter(self):
        """Resets (or sets) the iterator object that
        iterates over the vm commands. Useful for
        re-parsing the file as necessary.
        """
        self._vm_commands_iter = iter(self._vm_commands)

    def has_more_commands(self):
        """Are there any more commands in the file?
        Returns True if command iterable successfully
        gets the next command. Otherwise, return False.
        """
        try:
            self._vm_command_current = next(self._vm_commands_iter)
            return True
        except StopIteration:
            return False

    def command_type(self):
        """Returns the type of the current VM command.
        C_ARITHMETIC is returned for all the arithmetic
        commands.
        """
        return {
            'push': Command.C_PUSH,
            'pop': Command.C_POP,
            'label': Command.C_LABEL,
            'goto': Command.C_GOTO,
            'if-goto': Command.C_IF,
            'function': Command.C_FUNCTION,
            'call': Command.C_CALL,
            'return': Command.C_RETURN
        }.get(self._vm_command_current['name'], Command.C_ARITHMETIC)

    def arg1(self):
        """Returns the first argument of the current
        command. In the case of C_ARITHMETIC, the
        command itself (add, sub, etc.) is returned.
        Should not be called if the current command is
        C_RETURN.
        """
        if self.command_type() is Command.C_ARITHMETIC:
            return self._vm_command_current['name']
        else:
            return self._vm_command_current['arg1']

    def arg2(self):
        """Returns the second argument of the current
        command. Should only be called if the current
        command is C_PUSH, C_POP, C_FUNCTION, or
        C_CALL.
        """
        return int(self._vm_command_current['arg2'])
