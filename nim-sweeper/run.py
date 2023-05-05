import argparse
import visualize as vz
import nimsweeper as ns

if __name__ == "__main__":
    """
    Nimsweeper will be run from this file.
    """
    parser = argparse.ArgumentParser("NIMSWEEPER", "Help nim sweep the mines!")

    parser.add_argument("-m", "--mine_count", default=5, type=int,
                        help="Number of mines to be included with the minesweeper.")
    parser.add_argument("-t", "--terminal", action='store_true',
                        help="Basic nimsweeper with terminal. This only provides solutions to random boards.")

    args = parser.parse_args()
    mine_count = args.mine_count
    flag = args.terminal

    if flag:
        # TODO
        print("terminal")
    else:
        # TODO
        print("visualize")
