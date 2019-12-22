#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Room
"""
from random import randint
from vect import Vect


class Room():
    """
    Classe définissant une pièce. Elle permet de l'initialiser
    et de la connecter à d'autres.
    """
    #Dimentions maximales minimales
    _VECT_COTE_MIN = Vect(10, 6)
    _VECT_COTE_MAX = Vect(10, 8)

    # Espace autour de la pièce
    _OFFSET_COLLIDE = 2

    def __init__(self, pos_xmax, pos_ymax):
        """
        initialise une pièce
                p[1]        p[2]
                +---------+ (X2, Y2) : self.p[2]
                |    L    |
                |H   C   H|         X2 = X0 + L - 1
                |    L    |         Y2 = X0 + H - 1
                +---------+         (L, H) : self.size
        (X0, Y0)p[0]        p[3]
        pos_max est un point existant

        """
        pmax = Vect(pos_xmax, pos_ymax)
        self.size = (self._VECT_COTE_MIN | self._VECT_COTE_MAX) + Vect(2, 2)
        self.p = [None for _ in range(4)]
        self.p[0] = Vect(0, 0) | (pmax - self.size)
        norm_size = self.size - Vect(1, 1)
        self.p[1] = self.p[0] + (norm_size & Vect(False, True))
        self.p[2] = self.p[0] + (norm_size & Vect(True, True))
        self.p[3] = self.p[0] + (norm_size & Vect(True, False))
        self.center = self.p[0] + norm_size // 2

    def newRandomPointInRoom(self):
        """
        Retourne un point dans la pièce (Pas dans les murs)
        """
        return (self.p[0] + Vect(1, 1)) | (self.p[2] - Vect(1, 1))

    def g_corners(self):
        """
        Retourne les 4 coins de la salle
        """
        return (point for point in self.p)

    def isPointCollide(self, point):
        """
        Retourne si le point touche la salle (mur inclus)
        """
        return self.p[0] <= point <= self.p[2]

    def isPointCollideWithMargin1(self, point):
        """
        Retourne si le point touche la salle avec une marge de 1 vers l'exterieur
        """
        return self.p[0]-Vect(1, 1) <= point <= self.p[2]

    def isRoomCollide(self, other_room):
        """
        Retourne si l'autre salle est en Collision
        A une distance (offset) près
        """
        offset = self._OFFSET_COLLIDE
        # La distance minimale entre les salles
        if other_room.p[0].x >= self.p[0].x + self.size.x + offset or \
           other_room.p[0].x + other_room.size.x + offset <= self.p[0].x or \
           other_room.p[0].y >= self.p[0].y + self.size.y + offset or \
           other_room.p[0].y + other_room.size.y + offset <= self.p[0].y:
            return False
        return True

    def connect(self, other_room):
        """
        crée le chemin entre les deux salles
        """
        assert not self.isRoomCollide(other_room), "Les salles se superposent"

        door1 = self.newRandomPointInRoom()
        door2 = other_room.newRandomPointInRoom()

        path = []

        m = randint(0, 1)
        depl = door1.dirrectionTo(door2) & Vect(m, 1-m)

        if depl == Vect(1, 0):
            door1.x = self.p[2].x
            door2.x = other_room.p[0].x
        elif depl == Vect(-1, 0):
            door1.x = self.p[0].x
            door2.x = other_room.p[2].x
        elif depl == Vect(0, 1):
            door1.y = self.p[2].y
            door2.y = other_room.p[0].y
        elif depl == Vect(0, -1):
            door1.y = self.p[0].y
            door2.y = other_room.p[2].y
        cur_point = door1 + depl
        # On crée un chemin tant que l'on arrive pas dans la other_room
        while cur_point != door2:
            path.append(cur_point)
            # Deplacement en x ou y aléatoire
            m = randint(0, 1)
            cur_point += cur_point.dirrectionTo(door2) & Vect(m, 1-m)


        assert len(path) >= self._OFFSET_COLLIDE, 'Chemin trop court'
        # On retourne un tripet porte, chemin, porte
        return (door1, path, door2)

    def distance(self, other_room):
        """
        Retourne la distance entre deux salles (Des centres)
        """
        return self.p[0].distanceSquare(other_room.p[0])

    def g_xy(self):
        """
        Generateur sur tous les points de la salle
        """
        for x in range(self.size.x):
            for y in range(self.size.y):
                yield self.p[0] + Vect(x, y)

    def g_xyRender(self, middle_char):
        """
        Indique le type de char a chaque xy :
        Retourne un couple ! (Vect , char)
        """
        from tableborder import BORDERS
        line_style = 2
        for pos in self.g_xy():
            if pos == self.p[0]:
                type_char = BORDERS[line_style].low_left
            elif pos == self.p[1]:
                type_char = BORDERS[line_style].top_left
            elif pos == self.p[2]:
                type_char = BORDERS[line_style].top_right
            elif pos == self.p[3]:
                type_char = BORDERS[line_style].low_right
            elif pos.x == self.p[0].x or pos.x == self.p[2].x:
                type_char = BORDERS[line_style].vertical
            elif pos.y == self.p[0].y or pos.y == self.p[2].y:
                type_char = BORDERS[line_style].horizontal
            else:
                type_char = middle_char
            yield (pos, type_char)


    def g_xyCollide(self):
        """
        Retourne les points accessible a @
        Retourne un génerateur de Vect
        Permet la création de matrice des collision
        """
        for x in range(1, self.size.x - 1):
            for y in range(1, self.size.y - 1):
                yield self.p[0] + Vect(x, y)



def main():
    """
    Test unitaire
    """

    SIZE_Y = 30
    SIZE_X = 60
    screen = [[' ' for _ in range(SIZE_Y+2)] for _ in range(SIZE_X+2)]

    room1 = Room(SIZE_X, SIZE_Y)
    room2 = Room(SIZE_X, SIZE_Y)
    while room1.isRoomCollide(room2):
        room2 = Room(SIZE_X, SIZE_Y)

    door1, path, door2 = room1.connect(room2)

    # RENDER
    for pos, char in room1.g_xyRender('1'):
        screen[pos.x][pos.y] = char

    for pos, char in room2.g_xyRender('2'):
        screen[pos.x][pos.y] = char

    for pos in path:
        screen[pos.x][pos.y] = 'x'
    screen[door1.x][door1.y] = 'A'
    screen[door2.x][door2.y] = 'Z'

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            print(screen[x][SIZE_Y- y-1], end='')
        print("")

    # COLLIDES
    for pos in room1.g_xyCollide():
        screen[pos.x][pos.y] = '#'

    for pos in room2.g_xyCollide():
        screen[pos.x][pos.y] = '#'

    for pos in path:
        screen[pos.x][pos.y] = '#'

    for y in range(SIZE_Y):

        for x in range(SIZE_X):
            print(screen[x][SIZE_Y- y-1], end='')
        print("")


    print("\n Collision : ", room1.isRoomCollide(room2))
    print("Distance square: ", room1.distance(room2))

    def print_path(d1, path, d2):
        print("PATH: ", d1, '->', end="")
        for pos in path:
            print(pos, "->", end="")
        print(d2)
    print_path(door1, path, door2)


if __name__ == '__main__':
    N = 10
    print(chr(27) + "[2J")
    for i in range(N):
        main()
        print()
