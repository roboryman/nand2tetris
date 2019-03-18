#!/usr/bin/env python3


"""The SymbolTable Module
Keeps a correspondence between symbolic labels and numeric
addresses. This is done easily in Python using dictionaries.
Addresses are kept as decimal integers inside the table map.
"""


__author__ = "Merrick Ryman"
__version__ = "1.0"


class SymbolTable:
    def __init__(self):
        self._table = {}


    def add_entry(self, symbol, address):
        """Adds the mapping {symbol: address} to the table.
        """
        self._table.update({symbol:address})


    def contains(self, symbol):
        """Returns True if the table map contains the given
        symbol.
        """
        return symbol in self._table


    def get_address(self, symbol):
        """Returns the address mapped to the symbol from the table.
        """
        return self._table.get(symbol)
