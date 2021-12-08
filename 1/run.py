import sys
import numpy as np

def parse_data():
    return [int(line.strip()) for line in sys.stdin.readlines()]

def count_increases(values):
    diffs = np.diff(values)
    return sum(diffs > 0)

def count_increases_sliding_window(values, window_shape=3):
    summed = np.convolve(values, np.ones(window_shape, dtype=int), 'valid')
    return count_increases(summed)


if __name__ == '__main__':

    data = parse_data()

    # part 1
    print(count_increases(data))

    # part 2
    print(count_increases_sliding_window(data))