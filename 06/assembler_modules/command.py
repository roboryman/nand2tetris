#!/usr/bin/env python3


"""Command Enum
Provides an enum for the command types associated with
the source Hack ASM (A_COMMAND, C_COMMAND, L_COMMAND)
"""


import enum


__author__ = "Merrick Ryman"
__version__ = "1.0"


class Command(enum.Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3
