#!/usr/bin/env python3
"""
SANDBOX
"""

# http://nicofo.tuxfamily.org/index.php?post/2007/01/10/19-mouvement-du-curseur-dans-le-terminal
# https://rosettacode.org/wiki/Terminal_control/Preserve_screen#Python

import sys
import termios

import os



fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
new = termios.tcgetattr(fd)
new[3] = new[3] & ~termios.ECHO          # lflags


BUFFER_SIZE = 500*500
def start():
    """
    TODO
    """
    # Lancement ecran second
    print("\033[?1049h\033[H", end="")
    sys.stdout.flush()
    # Bufferisarion de stdout
    sys.stdout = open(sys.stdout.fileno(), "w", BUFFER_SIZE)


def stop():
    """
    TODO
    """
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
    print("\033[?1049l", end="")



def main():
    """
    TODO
    """

    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        start()

        for i in range(9999999999):# main loop
            H, L = map(int, os.popen('stty size', 'r').read().split())
            H = int(H)-1

            print('\033[0;0H', end='')

            terrain = [[chr(i%200+50) for _ in range(L)] for _ in range(H)]

            for h in range(H):
                for l in range(L):
                    if(l == 0 or l==L-1 or h==0 or h==H-1):
                        print('\x1b[6;30;42m' + '#' + '\x1b[0m', end = '', flush=False)
                    else:
                        print(terrain[h][l], end='', flush=False)
                print('')
            sys.stdout.flush()
            # time.sleep(0.01)
    finally:
        stop()
        print("END")

main()
