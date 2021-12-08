import sys
import numpy as np

def parse_data():
    """Parse data, return tuple of list (floats) and list (Board objects)"""
    data = sys.stdin.readlines()
    bingo = [float(i) for i in data[0].strip().split(',')]
    board_data = [line.strip() for line in data[2:]]
    boards = []
    board = []
    for line in board_data:
        if line == '':
            boards.append(np.array(board))
            board = []
        else:
            board.append([float(i) for i in line.split(" ") if i != ""])
    return bingo, [Board(board) for board in boards]


class Board:
    """Bingo board class"""
    def __init__(self, data):
        self.board = data
        self.win = False

    @property
    def score(self):
        """Return sum of board"""
        return np.nansum(self.board)

    def play_move(self, number):
        """Replace number on board by np.nan if it exists.
        Win == True if either one row or one column is all np.nan"""
        self.board[self.board == number] = np.nan

        row_nan = np.all(np.isnan(self.board), axis=1)
        col_nan = np.all(np.isnan(self.board), axis=0)
        self.win = np.any(row_nan) or np.any(col_nan)


def play_bingo_to_win(numbers, boards):
    """Find first board to win and return winning number * residual sum on board"""
    n = 0
    winning_board = None
    while not any([board.win for board in boards]):
        for board in boards:
            board.play_move(numbers[n])
            if board.win:
                winning_board = board
        n += 1

    return int(numbers[n-1] * winning_board.score)


def play_bingo_to_lose(numbers, boards):
    """Find last board to win and return winning number * residual sum on board"""
    n = 0
    last_winning_board = None
    while not all([board.win for board in boards]):
        for board in boards:
            if board.win:
                continue
            board.play_move(numbers[n])
            if board.win:
                last_winning_board = board
        n += 1
    return int(numbers[n-1] * last_winning_board.score)


if __name__ == '__main__':

    bingo, boards = parse_data()

    # part 1
    result = play_bingo_to_win(bingo, boards)
    print(result)

    # part 2
    last = play_bingo_to_lose(bingo, boards)
    print(last)

