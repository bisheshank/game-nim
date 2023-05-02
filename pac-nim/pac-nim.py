from z3 import *

# --------------- MAZE --------------------- #

MAZE = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XN           XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X                          X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X      XX    XX    XX      X",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XX          XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX X   G  X XX XXXXXX",
    "X         X G    X         X",
    "XXXXXX XX X   G  X XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX          XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "X            XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X   XX       G        XX   X",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "X      XX    XX    XX      X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X                          X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]


# --------------- CONSTANTS -------------------- #

# Define the dimensions of the MAZE
ROW = len(MAZE)
COL = len(MAZE[0])


# --------------- ITEMS -------------------- #
class Tile:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


FOOD = Tile("food", " ")
# POWERUP = Tile("powerup", "")
WALL = Tile("wall", "X")
NIM = Tile("nim", "N")
GHOST = Tile("ghost", "G")

# -------------- PATH -------------------- #


class Path:
    def __init__(self, start, end, tiles):
        # a path is a list of tiles
        self.start = start
        self.end = end
        self.tiles: list[Tile] = tiles

# -------------- MAIN -------------------- #


class main:
    def __init__(self, maze):
        self.paths = [Path(Int("start_%d" % i), Int("end_%d" % i))
                      for i in range(4)]
        self.tiles = [[Int("tile_%d_%d" % (i, j))
                      for j in range(COL)] for i in range(ROW)]

        self.s = Solver()

        # Add tile constraints
        for i in range(ROW):
            for j in range(COL):
                self.s.add(Or([self.tiles[i][j] == getattr(tile, "symbol")
                           for tile in [FOOD, WALL, NIM, GHOST]]))  # this is wrong

        # Add path constraints
        self.__add_path_contraints()

    def __add_path_contraints(self):
        # Add start and end constraints for paths
        for i, path in enumerate(self.paths):
            self.s.add(self.tiles[path.tiles[0][0]][path.tiles[0][1]] == "P")
            self.s.add(self.tiles[path.tiles[1][0]][path.tiles[1][1]] == "P")
            self.s.add(self.tiles[path.tiles[0][0]]
                       [path.tiles[0][1]] != WALL.symbol)
            self.s.add(self.tiles[path.tiles[1][0]]
                       [path.tiles[1][1]] != WALL.symbol)

            # Add constraint for path to be contiguous
            for j in range(1, len(path.tiles)):
                row1, col1 = path.tiles[j - 1]
                row2, col2 = path.tiles[j]
                self.s.add(Or(
                    And(row1 == row2, abs(col1 - col2) == 1),
                    And(col1 == col2, abs(row1 - row2) == 1)
                ))

        if self.s.check() == sat:
            m = self.s.model()

            # Print solution
            for i in range(ROW):
                for j in range(COL):
                    print(m[self.tiles[i][j]], end="")
                print()

            # Print paths
            for i, path in enumerate(self.paths):
                start_row, start_col = path.tiles[0]
                end_row, end_col = path.tiles[1]
                print(f"Path {i + 1}:")
                while start_row != end_row or start_col != end_col:
                    print(f"({start_row}, {start_col}) -> ", end="")
                    if start_row < end_row:
                        start_row += 1
                    elif start_row > end_row:
                        start_row -= 1
                    elif start_col < end_col:
                        start_col += 1
                    elif start_col > end_col:
                        start_col -= 1
                print(f"({end_row}, {end_col})")
        else:
            print("Failed to find a solution.")


if __name__ == "__main__":
    p = main(MAZE)


"""
PAC-NIM
main sigs:

Positions?
Pacman path
Ghost path
Tiles (dot, superdot, empty, ghost, food, wall)


"""
