#!/usr/bin/env python3
# pylint: disable=C0103
"""
Main script
"""

from pit import Pit
from core import Core
from myeventloop import MyEventLoop
from screen import Screen

def main():
    """
    Entry point
    """

    def game_update(pit_info):
        """
        Boucle principale du jeu
        """
        if not core.update(event_loop.get()):
            return False
        screen.update(core.render(screen.get_size(), screen.g_pos(), pit_info))
        return True

    try:
        # Ecran
        screen = Screen()
        #Coeur du jeu
        core = Core()
        core.generate()
        # boucle d'evenements
        event_loop = MyEventLoop()
        event_loop.start()

        timer = Pit(0.1, game_update)
        timer.start()

        screen.stop()
        print("Votre score : {}$".format(core.player.money))
        return True

    finally:
        # Attrape erreur
        screen.stop()




if __name__ == "__main__":
    main()
