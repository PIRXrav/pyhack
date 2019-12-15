#!/usr/bin/env python3
# pylint: disable=C0103
"""
Classique A*
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
"""
from heapq import heappush, heappop
import numpy
from vect import Vect

# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)

def heuristic(a, b):
    """
    heuristic
    """
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(array, start, goal):
    """
    A*
    """
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),
                 (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return reversed(data)

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 0:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return []

def calc_path_astart(mat_collide, start, end):
    """
    Couche de compatibilite
    """
    return list(map(lambda tup: Vect(tup[0], tup[1]),
                    astar(numpy.array(mat_collide),
                          (start.x, start.y), (end.x, end.y))))

def main():
    """
    TU
    """
    tab = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    start = Vect(0, 0)
    end = Vect(7, 6)

    path = calc_path_astart(tab, start, end)
    print(path)


if __name__ == '__main__':
    main()
