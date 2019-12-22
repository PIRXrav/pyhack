#!/usr/bin/env python3

from astar import main as TU_astar
from initroom import main as TU_initroom
from initvillage import main as TU_initvillage
from test_vision import main as TU_testvision
from vect import main as TU_vect
def main():
    """
    Travis TU
    """
    TU_astar()
    TU_initroom()
    TU_initvillage()
    TU_testvision()
    TU_vect()


if __name__ == '__main__':
    main()
