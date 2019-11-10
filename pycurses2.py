#!/usr/bin/env python3
# pylint: disable=C0103
"""
Main script
"""
import time


from core import Core
from myeventloop import MyEventLoop
from screen import Screen

def main():
    """
    Entry point
    """
    try:
        #Coeur du jeu
        core = Core()
        core.generatePlateau()
        # Ecran
        screen = Screen()
        # boucle d'evenements
        event_loop = MyEventLoop()
        event_loop.start()

        while True:
            core.update(event_loop.get())
            screen.update(core.plateau, core.pos_x, core.pos_y)
            time.sleep(0)

    finally:
        # Attrape erreur
        screen.__del__()


if __name__ == "__main__":
    main()
