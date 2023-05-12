# Nim-Sweeper

- Orion Bloomfield, Bisheshank Aryal, Daniel Liu

## Overview

- Our final project is Nim-Sweeper, a Minesweeper implementation using the z3 solver to
  generate boards with variable mine placement and solutions to user-interactive boards.
  You can run the program in the terminal to get grid outputs in the terminal, or you can
  run the visualizer to interact with a board with different functions such as "designing"
  the board, solving the board at its current state, and playing Minesweeper normally.

- Nim-Sweeper has two main parts;

  - nimsweeper.py, which contains the solver, terminal
    functionality, and various computations.

  - visualize.py, which uses pygame to display an interactive
    board with buttons. It handles user events and uses
    nimsweeper funcitonality to update the visuals accordingly.

- run.py handles functionality to either run the visualizer or
  to run Nim-Sweeper in the terminal alongside custom flags that
  determine solver constraints.

## Goals

- Our interactive solver proves questions about Nim-Sweeper such as:

  - How many solutions are there to a general ** row by ** column board with \_\_
    amount of mines?

  - Is there a solution to the current state of my board?

  - What is the next best move, one that reveals a truth (i.e. where a cell is
    100% a mine or where a cell is 100% not a mine) given an intermediate state of the board
    (solvability)?

## Design Choices

- Tradeoffs included using z3 instead of Forge, which we wanted to delve further into
  alongside a good project idea. Originally, our group chose to model Pac-Man, but given the
  limitations of z3 and game modeling, we decided that Minesweeper in z3 would be the perfect fit.
  While we have support for running through the terminal, we wanted to create a robust visualizer
  that allowed for interaction and genuine variability in intermediate game states for our solver
  to process, so we relied on pygame for visualizer foundations.

- Our model is computationally limited given board inputs that do not give anough information
  for the solver to narrow down on a solution; in these cases, the solver presents an astronomical
  amount of solutions; thus, we limit the number of solutions to the first 1000 solutions. This
  limitation restricts the solutions to be "favored" towards the top half of each board, but
  the breadth of the solver's analysis was significant enough to warrant the limit. We deemed long
  runtime for minimal benefit given a nigh-infinite sample size to be unfruitful, and thus stuck
  with 1000 solutions max.

- In our proposal, we set custom visualization as a reach goal, and did not even consider
  user interaction with the game/solver. However, pygame greatly facilitated visual developement
  and we opted for the design choice of integration between the interactive visual aspects
  of Nim-Sweeper and the "back-end" z3 solver to provide solutions or generate models to play
  with.

## Visual Guide

- In the visualizer, our model appears as a grid of cells with Minesweeper-esque icons with
  buttons at the bottom to perform specific functions. Cells can either be unknown (gray box),
  empty (gray square), a mine (mine image), deadly (frown face), safe (smile), unconfirmed flag
  (red flag), confirmed flag (green flag).
