#! /usr/bin/env python
#
# Author: Somesh Bhandarkar
# UID: 116715843
# This program is written as a project for the course
##
# The program uses z3 SMT solver https://github.com/Z3Prover/z3
# I have taken a few references for this approach
#
# https://yurichev.com/writings/SAT_SMT_by_example.pdf
# http://www.hakank.org/z3/
#
# The sum will look something like this
#
# 00000000000
#        01234567890
# 02-width--0
# 03 l      0
# 04 e      0
# 05 n      0
# 06 g      0
# 07 t      0
# 08 h      0
# 09		   0
# 00000000000
#
# The 0 is where the border is and the value inside it will
#   always be 0, as there is no possibility of a mine being there
#
# The program uses a binary 0/1 approach for the mine placement
# The program uses a list of list/matrix entry to store the boolean
# The main unknown here is whether there is a mine in the unknown grid
# I have solved this problem by feeding constraints to the SMT Solver
# and checking satisfiability
#
#
#
#
#
from z3 import *
import sys
from itertools import product, starmap

s = Solver()
grids = []


def initial_config(length, width):
    s = Solver()
    # blocks = []
    for r in range(0,  length+2):
        t = []
        for c in range(0,  width+2):
            t += [Int('(%d %d)' % (r, c))]
        grids.append(t)

    for c in range(width+2):
        # s.add(grids[length+1][c]==0)
        for r in range(length+2):
            if r == 0 or c == 0:
                s.add(grids[r][c] == 0)

            if r == length+2:
                s.add(grids[r][c] == 0)

            if c == width+2:
                s.add(grids[r][c] == 0)

    return grids

# def place_mine(grids):
# s = Solver()
# for r in range (1, length +1):
# for c in range (1, width +1):
# s.add(grids[r][c]==0,grids[r][c]==1)


def neighbours(r, c):
    neigh = []
    l1 = (-1, 0, +1)
    l2 = (-1, 0, +1)
    neigh = ([r+a, c+b] for a in l1 for b in l2)
    return (list(neigh))
    # return(neighbors(r, c))


def add_mine(row, col):
    s = Solver()

    for r in range(1, length + 1):
        for c in range(1, width + 1):
            S = [-1, 0, 1]

            temp = the_game[r - 1][c - 1]
            if temp in "012345678":
                s.add(grids[r][c] == 0)

                listing = neighbours(r, c)
                temp_i, temp_j = listing[0]

                express = grids[temp_i][temp_j]

                for i, j in listing[1:]:
                    express += grids[i][j]
                # add += grids[r+a,c+b] for a in S for b in S
                # if r + a >= 0 and c + b >= 0 and r + a < length+1 and c + b < width+1
                const = express == int(temp)
                # print express
                # print "\n", listing
                # sys.exit(0)
                s.add(const)

    s.add(grids[row][col] == 1)

    # if s.check==sat:
    # print "There may be a bomb at {} {}".format(row,col)
    if s.check() == unsat:
        print("Safe to play {} {}".format(row, col))


def main():
    global width
    global length
    global the_game
    the_problem = sys.argv[1]
    print("The Problem is from:", the_problem)
    the_game = read_problem(the_problem)
    width = len(the_game[0])
    length = len(the_game)
    print_problem(the_game)
    # just_checking()
    # print "w:", width, "l:", length
    # print the_game
    grids = initial_config(length, width)
    # print grids
    for r in range(1, length + 1):
        for c in range(1, width + 1):
            if the_game[r-1][c-1] == "X":
                # place_mine(grids)
                # print r,c
                add_mine(r, c)


def print_problem(listing):
    print("The grid is:")
    print("\n")
    for i in listing:
        print("\t", i)
    print("\n")


def read_problem(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()
        lst = []
    for items in lines:
        items = items.rstrip("\n")
        lst.append(items)
    return lst


def just_checking():
    print("w:", width, "l:", length)
    print(the_game)


if __name__ == "__main__":
    main()
