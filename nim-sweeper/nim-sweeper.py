from z3 import *
import random


UNKNOWN = -1
VERBOSE = True
def generate_board(r_cnt, c_cnt, mine_cnt):
    # randomly generate a board of size r_cnt x c_cnt
    # A number represents the number of mines around it.
    # X (-1) represents an unknown on whether it is a mine or not.
    board = [[0 for _ in range(c_cnt)] for _ in range(r_cnt)]
    mines = random.sample([(r, c) for r in range(r_cnt)
                          for c in range(c_cnt)], mine_cnt)

    for row, col in mines:
        board[row][col] = UNKNOWN

    for row in range(r_cnt):
        for col in range(c_cnt):
            if board[row][col] == UNKNOWN:
                continue

            adjacents = [(row + r, col + c) for r in [-1, 0, 1]
                         for c in [-1, 0, 1] if r != 0 or c != 0]
            adj_mine_count = sum(1 for r, c in adjacents if 0 <=
                                 r < r_cnt and 0 <= c < c_cnt and board[r][c] == UNKNOWN)
            board[row][col] = adj_mine_count

    for row in range(r_cnt):
        for col in range(c_cnt):
            if board[row][col] == 0:
                board[row][col] = UNKNOWN

    return board


def main(game):

    sol = SimpleSolver()

    # Set default problem

    r = len(game)
    c = len(game[0])

    # declare variables
    mines = {}
    for i in range(r):
        for j in range(c):
            mines[(i, j)] = Int("mines %i %i" % (i, j))
            sol.add(mines[(i, j)] >= 0, mines[(i, j)] <= 1)

    # constraints
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
                # cannot be a mine if it is a number
                sol.add(mines[i, j] == 0)
            else:
              # If an unknown tile is not adjacent to a numbered tile, it must not contain a mine
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
        if VERBOSE:
          for i in range(r):
              for j in range(c):
                  print("◇", end=" ") if mod.eval(mines[(i,j)]) == 1 else print("■", end=" ")
              print()
          print()
      
        sol.add(Or([mines[i, j] != mod.eval(mines[i, j])
                for i in range(r) for j in range(c)]))
    print("num_solutions:", num_solutions)
    return num_solutions

def print_mines(mines, rows, cols):
    for i in range(rows):
        for j in range(cols):
            print(mines[i, j], end=" ")
        print()

def print_solution(mines, rows, cols):
    for i in range(rows):
        for j in range(cols):
            print(mines, end=" ")
        print()
    print()
    

def print_board(board):
    r = len(board)
    c = len(board[0])

    print("BOARD:")
    for i in range(r):
        for j in range(c):
            if board[i][j] == UNKNOWN:
                print("■", end=" ")
            else:
                print(board[i][j], end=" ")
        print()
    print()


ROWS, COLS = 16, 16
MINE_CNT = 20

if __name__ == "__main__":
    
    board = generate_board(ROWS, COLS, mine_cnt=MINE_CNT)

    print_board(board)
    num_sols = main(board)