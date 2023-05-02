from z3 import *


class Tile:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


FOOD = Tile("food", ".")
POWERUP = Tile("powerup", "o")
EMPTY = Tile("empty", " ")
WALL = Tile("wall", "#")
GHOST = Tile("ghost", "G")


class Path:
    def __init__(self, tiles):
        # a path is a list of tiles
        self.tiles: list[Tile] = tiles


class PacNim(object):
    def ___init___(self):

        self.paths = [Path(Int("start_%d" % i), Int("end_%d" % i))
                      for i in range(4)]
        self.tiles = [[Int("tile_%d_%d" % (i, j))
                       for j in range(5)] for i in range(4)]

        for i in range(4):
            for j in range(5):
                self.s.add(Or([self.tiles[i][j] == getattr(tile, "symbol")
                           for tile in [FOOD, POWERUP, EMPTY, WALL, GHOST, CANDY]]))

    def solve(self):


if __name__ == "__main__":
    p = PacNim()


"""
PAC-NIM
main sigs: 

Positions?
Pacman path
Ghost path
Tiles (dot, superdot, empty, ghost, food, wall)


"""
