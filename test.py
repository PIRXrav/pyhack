#!/usr/bin/env python3
"""
SANDBOX
"""
# TEST champ de vision avec tracé de ligne
# https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python

from vect import Vect

def g_case_visible(tab_collide, center, radius):
    """
    retourne sur toutes les cases visibles
    depuis un point center dans un rayon radius
    """
    # Nb : prend les segments depuis un cercle et non un rect
    # n'est pas OK
    border = center.g_rect(Vect(radius, radius))
    for bordure_pos in border:
        for pos in center.g_bresenham_line(bordure_pos):
            if center.distance(pos) >= radius:
                break
            if not tab_collide[pos.x][pos.y]:
                break
            yield pos


def main():
    """
    Entry point
    """
    try:

        SIZE_Y = 30
        SIZE_X = 60
        screen = [[True for _ in range(SIZE_Y+2)] for _ in range(SIZE_X+2)]

        for _ in range(4):
            p1 = Vect(0, 0) | Vect(SIZE_X, SIZE_Y)
            p2 = Vect(0, 0) | Vect(SIZE_X, SIZE_Y)
            for pos in p1.g_bresenham_line(p2):
                screen[pos.x][pos.y] = False
                screen[pos.x+1][pos.y] = False


        # Calculs
        center = Vect(30, 15)
        for pos in g_case_visible(screen, center, 10):
            screen[pos.x][pos.y] = 'F'

        screen[center.x][center.y] = '@'

        # affichage
        for y in range(SIZE_Y):
            for x in range(SIZE_X):
                char = screen[x][SIZE_Y- y-1]
                if char == False:
                    print_char = "\033[0;34;41m" + ' ' + "\033[0m"
                if char == True:
                    print_char = ' '
                if char == 'F':
                    print_char = "\033[0;34;43m" + ' ' + "\033[0m"
                if char == '@':
                    print_char = "\033[0;31;45m" + ' ' + "\033[0m"
                if char == 'B':
                    print_char = "\033[0;34;40m" + 'X' + "\033[0m"
                print(print_char, end='')
            print("")
    finally:
        print("END")

main()
