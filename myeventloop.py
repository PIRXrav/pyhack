#!/usr/bin/env python3
# pylint: disable=C0103
"""
MyEventLoop
"""
from queue import Queue
from pynput import keyboard

# TODO: [BUG FIX] est active mm quand la fenetre est au segond plan ! A coorigé
class MyEventLoop():
    """
    Event eventLoop
    """
    # state
    _PRESS = True
    _RELEASE = False

    # définition du tuple de la queu
    _KEY = 0 # Key
    _VAL = 1 # Valeur

    def __init__(self):
        """
        Constructeur
        """
        self._my_eventq = Queue() # THREAD SAFE !!
        self._current_key_state = {}

    def _onRawPress(self, key):
        """
        Callback on press
        """
        self._my_eventq.put((key, self._PRESS))

    def _onRawRelase(self, key):
        """
        Callback on relase
        """
        self._my_eventq.put((key, self._RELEASE))

    def start(self):
        """
        Start listener
        """
        listener = keyboard.Listener(
            on_press=self._onRawPress,
            on_release=self._onRawRelase)
        listener.start()

    def stop(self):
        """
        Stop eventLoop
        """
        # TODO: pass

    def pause(self):
        """
        Pause eventLoop
        """
        # TODO: pass

    def resume(self):
        """
        Resume eventLoop
        """
        # TODO: pass

    def get(self):
        """
        retourne toutes tes touches qui se sont trouvé enfoncé depuis le dernier appel
        = union(touches presse avant le dernier appel mais pas relacher = dict,
                touches presser et relacher entre les deux appels = Queus)
        """
        # tableau des touches a retourner : (dict.keys)
        keyboard_state = {}

        while not self._my_eventq.empty():
            event = self._my_eventq.get()
            # touches presser et relacher entre les deux appels
            if event[self._KEY] in self._current_key_state.keys():
                # Si la valeur existe
                if not self._current_key_state[event[self._KEY]]:
                    # Si la touche est relache
                    keyboard_state[event[self._KEY]] = self._PRESS
                    # Alors l'utilisateur enfonce la touche
            # mise a jour de l'état de touches
            self._current_key_state[event[self._KEY]] = event[self._VAL]

        # On ajoute toutes les touches enfonces a retourner
        for key, state in self._current_key_state.items():
            if state:
                keyboard_state[key] = self._PRESS

        return list(keyboard_state.keys())


if __name__ == '__main__':
    import time

    print("TU : MY_eventLoop")

    event_loop = MyEventLoop()
    event_loop.start()

    while True:
        event_array = event_loop.get()
        print(event_array)
        print(event_array)

        if 'q' in event_array:
            # Si un q est pressé on stop la boucle d'evenement
            print("HEEHE")
            event_loop.stop()

        if 'e' in event_array:
            # Si un e est pressé on stop le programme
            print("Done")
            event_loop.stop()
            exit()

        time.sleep(.1)
