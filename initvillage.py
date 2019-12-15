#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Village
Un village est un tableau de pièce
"""

from initroom import Room

class Village:
    """
    Classe village :
    Ordonne des salles / chemins
    """
    def __init__(self, XMAX, YMAX, NB_ROOMS):
        """
        Règles de générations
        """
        self.NB_ROOMS = NB_ROOMS
        self.XMAX = XMAX
        self.YMAX = YMAX

        self.rooms = []
        self.paths = []

    def _newRoom(self):
        """
        Initialise une pièce aléatoire dans le Village
        """
        return Room(self.XMAX, self.YMAX)

    def _getNearestRoom(self, room):
        """
        Retourne la pièce la plus proche
        """
        return min(self.rooms, key=room.distance)

    def isCollidePathInPaths(self, path1):
        """
        Retourne si le chemin path1 est en collision les autres chemins
        """
        for path2 in self.paths:
            for p2 in path2:
                for p1 in path1:
                    if p1 == p2:
                        return True
        return False

    def isCollidePathInRooms(self, path1):
        """
        Retourne si le chemin path1 est en collision les autres salles
        """
        for room in self.rooms:
            for p1 in path1:
                if room.isPointCollide(p1):
                    return True
        return False

    def isCollideRoomInPaths(self, room):
        """
        Retourne si la salle room est en collision les autres chemins
        """
        for path in self.paths:
            for point in path:
                if room.isPointCollide(point):
                    return True
        return False

    def isCollideRoomInRooms(self, room):
        """
        Retourne si la salle room est en collision les autres salles
        """
        for room2 in self.rooms:
            if room.isRoomCollide(room2):
                return True
        return False

    def isCollidePath(self, path):
        """
        Retourne si un chemin est en collision
        """
        # Des chemins peuvent se croiser
        return self.isCollidePathInRooms(path)
        # Des chemions ne peuvent pas se croiser
        return self.isCollidePathInPaths(path) or \
               self.isCollidePathInRooms(path)

    def isCollideRoom(self, room):
        """
        Retourne si une salle est en collision
        """
        return self.isCollideRoomInPaths(room) or \
               self.isCollideRoomInRooms(room)

    def addAndConnectNewRoom(self):
        """
        Ajoute et connecte une salle
        L'objet reste sans collision
        """
        if self.rooms == []:
            # On ajoute une salle sans chemins
            self.rooms.append(self._newRoom())
        else:
            # On ajoute une salle valide avec chemin valide
            errors = -1
            while True:
                errors += 1
                # Nouvelle bonne pièce
                room = self._newRoom()
                if self.isCollideRoom(room):
                    continue
                # Nouveau chemin
                door1, path, door2 = room.connect(self._getNearestRoom(room))
                if self.isCollidePath(path):
                    # Si le chemin est faux, on génere une nouvelle salle
                    continue

                self.paths.append([door1]+path+[door2])
                self.rooms.append(room)
                return errors
        return 0

    def generate(self):
        """
        Genere les salles et leurs chemins
        """
        import sys
        for _ in range(self.NB_ROOMS):
            print(self.addAndConnectNewRoom())
            sys.stdout.flush()

    def g_xyRender(self):
        """
        Indique le type de char a chaque xy :
        Retourne un génerateur de couple (Vect , char)
        Permet la création de matrice d'affichage
        """
        for room in self.rooms:
            for pos, char in room.g_xyRender('.'):
                yield (pos, char)

        for path in self.paths:
            index_max = len(path) - 1
            for index, pos in enumerate(path):
                if index == 0:
                    # Porte de depart
                    yield (pos, "\033[33m" + 'D' + "\033[0m")
                elif index == index_max:
                    # Porte d'arrivé
                    yield (pos, "\033[33m" + '\u25A1' + "\033[0m")
                else:
                    # Chemin
                    yield (pos, "\033[33m" + '\u2591' + "\033[0m")

    def g_xyCollide(self):
        """
        Retourne les points accessible a @
        Retourne un génerateur de Vect
        Permet la création de matrice des collision
        """
        # L'interieur des pièces
        for room in self.rooms:
            for pos in room.g_xyCollide():
                yield pos

        # Les chemions
        for path in self.paths:
            for pos in path:
                yield pos



def main():
    """
    Test unitaire
    """
    SIZE_Y = 50
    SIZE_X = 100
    screen = [[' ' for _ in range(SIZE_Y)] for _ in range(SIZE_X)]


    village = Village(SIZE_X, SIZE_Y, 15)
    village.generate()

    # COLLIDES
    for pos in village.g_xyCollide():
        screen[pos.x][pos.y] = "\033[33m" + '\u2591' + "\033[0m"

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            print(screen[x][SIZE_Y - y -1], end='')
        print("")

    # RENDER
    for pos, char in village.g_xyRender():
        screen[pos.x][pos.y] = char

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            print(screen[x][SIZE_Y - y -1], end='')
        print("")



if __name__ == '__main__':
    main()
