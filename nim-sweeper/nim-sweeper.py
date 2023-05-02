import random
from typing import List, Tuple, Dict
from z3 import *

# from visualization import visualize

# ------------------ CONSTANTS -------------------- #
ROWS: int = 10
COLS: int = 10
MINE_CNT: int = 5
BLANKS_HAVE_NO_NEW_INFO: bool = True
VERBOSE: bool = True
UNKNOWN: int = -1
PRINT_ALL: bool = False

# -------------- GAME BOARD GENERATOR ---------------- #


def generate_board(rows: int, cols: int, mine_cnt: int) -> List[List[int]]:
    """
    Generate a board of size rows x cols with mine_cnt mines randomly placed
    """
    # randomly generate a board of size rows x cols
    # A number represents the number of mines around it.
    # X (-1) represents an unknown on whether it is a mine or not.

    # Initialize the board
    board = [[0 for _ in range(cols)] for _ in range(rows)]

    # Sample of indices for the mines
    mine_indices = random.sample([(r, c) for r in range(rows)
                                  for c in range(cols)], mine_cnt)

    # Place the mines in the board
    for row, col in mine_indices:
        board[row][col] = UNKNOWN

    # Place the numbers according to the mines placed
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == UNKNOWN:
                continue

            adjacents = [(row + r, col + c) for r in [-1, 0, 1]
                         for c in [-1, 0, 1] if r != 0 or c != 0]
            adj_mine_count = sum(1 for r, c in adjacents if 0 <=
                                 r < rows and 0 <= c < cols and board[r][c] == UNKNOWN)
            board[row][col] = adj_mine_count

    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                board[row][col] = UNKNOWN

    return board


# ----------------- MINESWEEPER ------------------ #

def main(game: List[List[int]]) -> int:
    # Using the z3 solver
    sol = Solver()

    # Set default values of rows and columns
    r = len(game)
    c = len(game[0])

    # Declare variables
    mines = {}
    for i in range(r):
        for j in range(c):
            mines[(i, j)] = Int(f"mines_{i}{j}")
            sol.add(mines[(i, j)] >= 0, mines[(i, j)] <= 1)

    # Constraints
    adj = [-1, 0, 1]
    for i in range(r):
        for j in range(c):
            if game[i][j] > UNKNOWN:
                sol.add(
                    game[i][j] == Sum([mines[i+a, j+b]
                                       for a in adj for b in adj
                                       if i + a > UNKNOWN and
                                       j + b > UNKNOWN and
                                       i + a < r and
                                       j + b < c])
                )
                # Cannot be a mine if it is a number
                sol.add(mines[i, j] == 0)
            elif BLANKS_HAVE_NO_NEW_INFO:
                # else:
                # If an unknown tile is not adjacent to a numbered tile,
                # it must not contain a mine
                if all(game[i+a][j+b] == UNKNOWN
                       for a in adj for b in adj
                       if i + a > UNKNOWN and
                       j + b > UNKNOWN and
                       i + a < r and
                       j + b < c):
                    sol.add(mines[(i, j)] == 0)

    num_solutions = 0
    print("Solution(s):")
    while sol.check() == sat:
        num_solutions += 1
        mod = sol.model()
        # Print the found solution
        if VERBOSE:
            print_boards(board, mines, mod, True, PRINT_ALL)

        # Finding more solutions by excluding the current solution
        sol.add(Or([mines[i, j] != mod.eval(mines[i, j])
                for i in range(r) for j in range(c)]))
    print("num_solutions:", num_solutions)
    return num_solutions


# ------------- BOARD PRINTING ---------------- #

def print_boards(
        game: List[List[int]],
        mines: Dict[Tuple[int, int], int] = {},
        mod: any = None,
        completed: bool = False,
        print_all: bool = True):
    """
    Prints a given game board with mines.

    Args:
    - game (List[List[int]]): the initial game board
    - mines (Dict[Tuple[int, int], int]): a dictionary representing the solved minesweeper board, where the keys are
    - mod (any : z3 class)
    - completed (bool): true if the game is completed
    - print-all (bool): true if all the numbers also are being completed
    """
    rows = len(game)
    cols = len(game[0])

    if not completed:
        print("BOARD:")
    for i in range(rows):
        for j in range(cols):
            if completed and mod.eval(mines[(i, j)]) == 1:
                print("◇", end=" ")
            else:
                if print_all:
                    print("■", end=" ") if game[i][j] == UNKNOWN else print(
                        game[i][j], end=" ")
                else:
                    print("■", end=" ")
        print()
    print()

    # visualize.draw_board(game, mines, completed)


if __name__ == "__main__":
    board = generate_board(ROWS, COLS, mine_cnt=MINE_CNT)
    print_boards(board)
    num_sols = main(board)
