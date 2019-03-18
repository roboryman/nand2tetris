#!/usr/bin/env python3


"""The Code Module
Translates Hack ASM mnemonics into Hack Machine Language.
"""


__author__ = "Merrick Ryman"
__version__ = "1.0"


def dest(mnemonic):
    """Returns the Hack Machine Language equivalent of a
    dest mnemonic (3 bits).
    """
    return {    #A D M
        'null': [0,0,0],
           'M': [0,0,1],
           'D': [0,1,0],
          'MD': [0,1,1],
           'A': [1,0,0],
          'AM': [1,0,1],
          'AD': [1,1,0],
         'AMD': [1,1,1]
    }[mnemonic]


def comp(mnemonic):
    """Returns the Hack Machine Language equivalent of a
    comp mnemonic (7 bits).
    """
    return { #a c1 c2 c3 c4 c5 c6
        '0': [0,1,0,1,0,1,0],
        '1': [0,1,1,1,1,1,1],
       '-1': [0,1,1,1,0,1,0],
        'D': [0,0,0,1,1,0,0],
        'A': [0,1,1,0,0,0,0],   'M': [1,1,1,0,0,0,0],
       '!D': [0,0,0,1,1,0,1],
       '!A': [0,1,1,0,0,0,1],  '!M': [1,1,1,0,0,0,1],
       '-D': [0,0,0,1,1,1,1],
       '-A': [0,1,1,0,0,1,1],  '-M': [1,1,1,0,0,1,1],
      'D+1': [0,0,1,1,1,1,1],
      'A+1': [0,1,1,0,1,1,1], 'M+1': [1,1,1,0,1,1,1],
      'D-1': [0,0,0,1,1,1,0],
      'A-1': [0,1,1,0,0,1,0], 'M-1': [1,1,1,0,0,1,0],
      'D+A': [0,0,0,0,0,1,0], 'D+M': [1,0,0,0,0,1,0],
      'D-A': [0,0,1,0,0,1,1], 'D-M': [1,0,1,0,0,1,1],
      'A-D': [0,0,0,0,1,1,1], 'M-D': [1,0,0,0,1,1,1],
      'D&A': [0,0,0,0,0,0,0], 'D&M': [1,0,0,0,0,0,0],
      'D|A': [0,0,1,0,1,0,1], 'D|M': [1,0,1,0,1,0,1]
    }[mnemonic]


def jump(mnemonic):
    """Returns the Hack Machine Language equivalent of a
    jump mnemonic (3 bits).
    """
    return {    #A D M
        'null': [0,0,0],
         'JGT': [0,0,1],
         'JEQ': [0,1,0],
         'JGE': [0,1,1],
         'JLT': [1,0,0],
         'JNE': [1,0,1],
         'JLE': [1,1,0],
         'JMP': [1,1,1]
    }[mnemonic]
