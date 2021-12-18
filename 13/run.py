import sys
import numpy as np


def parse_data():
    """Parse data into "sheet" array and fold_instructions"""
    indices = []
    fold_instructions = []
    for line in sys.stdin.readlines():
        line = line.strip()
        try:
            indices.append((int(line.split(',')[1]), int(line.split(',')[0])))
        except (IndexError, ValueError):
            if line != '':
                axis, pos = (line.split(' ')[-1]).split('=')
                fold_instructions.append((axis, int(pos)))
    field = np.zeros(np.array(indices).max(axis=0)+1)
    for i in indices:
        field[i] = 1
    return field, fold_instructions


def fold_field(data, axis, position):
    """
    Return array after folding along axis located at given position.
    axis = 'x' folds along axis 1 to the left.
    axis = 'y' folds along axis 0 up.
    Padding is necessary to be able to use array addition; fold may occur
    off-centre.
    Where addition yields > 1, value capped to 1.
    """

    if axis == 'x':
        trunc = data[:, :position]
        to_add = data[:, (position+1):]
        pad = np.zeros([trunc.shape[0], position - to_add.shape[1]])
        flip_axis = 1

    if axis == 'y':
        trunc = data[:position, :]
        to_add = data[(position+1):, :]
        pad = np.zeros([position - to_add.shape[0], trunc.shape[1]])
        flip_axis = 0

    add = np.concatenate([to_add, pad], axis=flip_axis)
    folded = trunc + np.flip(add, flip_axis)
    folded[folded > 0] = 1

    return folded


def count_dots(field):
    """Return number of non-zero elements in field array."""
    return np.count_nonzero(field)


if __name__ == '__main__':

    # Part 1
    field, instructions = parse_data()

    after_one_fold = fold_field(field, *instructions[0])
    print(count_dots(after_one_fold))


    # Part 2
    for ins in instructions:
        field = fold_field(field, *ins)
    print(field.shape)
    # The ones spell out 8 letters, so split into 8 and read off output
    for letter in np.array_split(field, 8, axis=1):
        print(letter)
        print()

