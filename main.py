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
        # Ecran
        screen = Screen()
        #Coeur du jeu
        core = Core()
        core.generate()

        # boucle d'evenements
        event_loop = MyEventLoop()
        event_loop.start()

        while True:
            core.update(event_loop.get())
            screen.update(core.render(screen.get_size()))
            time.sleep(0.001)

    finally:
        # Attrape erreur
        screen.__del__()


if __name__ == "__main__":
    main()
