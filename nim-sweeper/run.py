import argparse
import visualize as vz
import nimsweeper as ns

if __name__ == "__main__":
    """
    Nimsweeper will be run from this file.
    """
    parser = argparse.ArgumentParser("NIMSWEEPER", "Help nim sweep the mines!")

    parser.add_argument("-r", "--rows", default=ns.ROWS, type=int,
                        help="Number of rows for the game board.")
    parser.add_argument("-c", "--cols", default=ns.COLS, type=int,
                        help="Number of columns for the game board.")
    parser.add_argument("-nv", "--not_verbose", action='store_false',
                        help="Default shows all solution game boards, this flag only prints the number of solutions.")
    parser.add_argument("-m", "--mine_count", default=ns.MINE_CNT, type=int,
                        help="Number of mines to be included with the minesweeper.")
    parser.add_argument("-t", "--terminal", action='store_true',
                        help="Basic nimsweeper with terminal. This only provides solutions to random boards.")

    args = parser.parse_args()
    rows = args.rows
    cols = args.cols
    nv = args.not_verbose
    mine_count = args.mine_count
    flag = args.terminal

    if flag:
        # TODO
        print("terminal")
        ns.run(rows, cols, mine_count, nv)
    else:
        # TODO
        print("visualize")
        vz.run(mine_count)
