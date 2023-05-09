import random
from typing import List, Tuple, Dict
from z3 import *


# Properties to find
# is it possible to solve from an intermediate state
# best possible move? to know more info or to find a mine
# opening up?
# solvability?

# ------------------ CONSTANTS -------------------- #
ROWS: int = 10
COLS: int = 10
MINE_CNT: int = 10
CONSTRAIN_CORRECT_MINE_COUNT: bool = False
BLANKS_HAVE_NO_NEW_INFO: bool = True
VERBOSE: bool = True
UNKNOWN: int = -1
MINE: int = -2
KEEP_MINES_KNOWN: bool = False
PRINT_ALL: bool = False

LIMIT_SOL_SPACE: bool = True
SOL_LIMIT: int = 1000

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
    print(mine_indices)

    # Place the mines in the board
    for row, col in mine_indices:
        board[row][col] = MINE

    # Place the numbers according to the mines placed
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == UNKNOWN or board[row][col] == MINE:
                continue

            adjacents = [(row + r, col + c) for r in [-1, 0, 1]
                         for c in [-1, 0, 1] if r != 0 or c != 0]
            adj_mine_count = sum(1 for r, c in adjacents if 0 <=
                                 r < rows and 0 <= c < cols and board[r][c] == MINE)
            board[row][col] = adj_mine_count

    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                board[row][col] = UNKNOWN
            if board[row][col] == MINE and not KEEP_MINES_KNOWN:
                board[row][col] = UNKNOWN

    return board


# ----------------- MINESWEEPER ------------------ #

def likely_mines(solutions: List[List[List[int]]]) -> Tuple[List[Tuple[int, int]], float]:
    mine_counts = {}
    total_solutions = len(solutions)
    for solution in solutions:
        for i, row in enumerate(solution):
            for j, cell in enumerate(row):
                if cell == MINE:
                    mine_counts[(i, j)] = mine_counts.get((i, j), 0) + 1

    sorted_mines = sorted(mine_counts.items(), key=lambda x: -x[1])
    if len(sorted_mines) == 0:
        return [], 1
    top_count = sorted_mines[0][1]
    # get all the mines that are most likely (same top count)
    most_likely_mines = [mine for mine,
                         count in sorted_mines if count == top_count]
    percentage_likelihood = top_count / total_solutions

    return most_likely_mines, percentage_likelihood


def likely_safe(solutions: List[List[List[int]]],
                init_board: List[List[int]]) -> Tuple[List[Tuple[int, int]], float]:
    safe_counts = {}
    total_solutions = len(solutions)
    for solution in solutions:
        for i, row in enumerate(solution):
            for j, cell in enumerate(row):
                if cell != MINE and init_board[i][j] == UNKNOWN:
                    safe_counts[(i, j)] = safe_counts.get((i, j), 0) + 1

    sorted_safe = sorted(safe_counts.items(), key=lambda x: -x[1])
    if len(sorted_safe) == 0:
        return [], 1
    top_count = sorted_safe[0][1]
    # get all the mines that are most likely (same top count)
    most_likely_safe = [safe for safe,
                        count in sorted_safe if count == top_count]
    percentage_likelihood = top_count / total_solutions

    return most_likely_safe, percentage_likelihood


def solve(game: List[List[int]],
          mine_cnt: int = MINE_CNT,
          blanks_no_adj: bool = BLANKS_HAVE_NO_NEW_INFO,
          constrain_mines: bool = CONSTRAIN_CORRECT_MINE_COUNT,
          limit_sols: bool = LIMIT_SOL_SPACE
          ) -> int:
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
            if game[i][j] == MINE:
                sol.add(mines[(i, j)] == 1)
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
            elif blanks_no_adj:
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

    if constrain_mines:  # Constrain the number of mines to match the game
        sol.add(Sum([mines[i, j] for i in range(r)
                for j in range(c)]) == mine_cnt)

    num_solutions = 0
    solutions = []
    while sol.check() == sat and (num_solutions <= SOL_LIMIT or not limit_sols):
        num_solutions += 1
        mod = sol.model()
        solutions.append(solution_board(game, mines, mod))

        # Finding more solutions by excluding the current solution
        sol.add(Or([mines[i, j] != mod.eval(mines[i, j])
                for i in range(r) for j in range(c)]))
    print("num_solutions:", num_solutions) if num_solutions < 100 else print(
        "num_solutions: 100+")
    return num_solutions, solutions


# ------------- BOARD PRINTING ---------------- #

def solution_board(game, mines, mod):
    """
    Returns a solved board given the game board and the mines
    """
    rows = len(game)
    cols = len(game[0])
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if mod.eval(mines[(i, j)]) == 1:
                board[i][j] = MINE
            else:
                board[i][j] = game[i][j]
    print(mines)
    return board


def print_boards(boards: List[List[List[int]]]):
    """
    Prints a list of boards
    """
    print("BOARD:")
    for board in boards:
        print_board(board, completed=True)


def print_board(
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
            if completed and mod and mod.eval(mines[(i, j)]) == 1 or game[i][j] == MINE:
                print("◇", end=" ")
            else:
                if print_all:
                    print("■", end=" ") if game[i][j] == UNKNOWN else print(
                        game[i][j], end=" ")
                else:
                    print("■", end=" ")
        print()
    print()


def run(rows=ROWS, cols=COLS, mine_cnt=MINE_CNT, v=VERBOSE):
    board = generate_board(rows, cols, mine_cnt)
    print_board(board)
    num_sols, sols = solve(board, mine_cnt, blanks_no_adj=v)

    print("Solution(s):")
    print_boards(sols)


# if __name__ == "__main__":
#     board = generate_board(ROWS, COLS, mine_cnt=MINE_CNT)
#     print_board(board)
#     num_sols, sols = solve(board, mine_cnt=MINE_CNT)

#     if VERBOSE:
#         print("Solution(s):")
#         print_boards(sols)
