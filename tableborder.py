#!/usr/bin/env python3
# pylint: disable=C0103
# pylint: disable=R0902
# pylint: disable=R0903
# pylint: disable=R0913

"""
Définie la classe TableBorder
"""

class TableBorder:
    """
    Facillite l'usage de l'UNICODE
    """
    def __init__(self,
                 top_left, top_split, top_right,
                 mid_left, mid_split, mid_right,
                 low_left, low_split, low_right,
                 horizontal, vertical):
        """
        Constructeur
        """
        self.top_left = top_left
        self.top_split = top_split
        self.top_right = top_right
        self.mid_left = mid_left
        self.mid_split = mid_split
        self.mid_right = mid_right
        self.low_left = low_left
        self.low_split = low_split
        self.low_right = low_right
        self.horizontal = horizontal
        self.vertical = vertical

BORDERS = [TableBorder('+', '+', '+',\
                       '+', '+', '+',\
                       '+', '+', '+',\
                       '-', '|'),
           TableBorder(u'\u250c', u'\u252C', u'\u2510',\
                       u'\u251C', u'\u253C', u'\u2524',\
                       u'\u2514', u'\u2534', u'\u2518',\
                       u'\u2500', u'\u2502'),
           TableBorder(u'\u2554', u'\u2566', u'\u2557',\
                       u'\u2560', u'\u256C', u'\u2563',\
                       u'\u255a', u'\u2569', u'\u255d',\
                       u'\u2550', u'\u2551')
          ]
