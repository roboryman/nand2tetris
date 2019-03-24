#!/usr/bin/env python3


"""Command Enum
Provides an enum for the command types associated with
the VM language.
"""


import enum


__author__ = "Merrick Ryman"
__version__ = "1.0"


class Command(enum.Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9
