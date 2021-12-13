import sys
import numpy as np
import pandas as pd


def parse_data():
    """Return DataFrame with clues and values.
    Clues are assigned where possible (1, 4, 7 and 8), others stored in placeholders.
    Sort strings alphabetically.
    """
    def _index(string):
        return ''.join(sorted(string))

    data = [line.strip() for line in sys.stdin.readlines()]
    data = [line.split(' | ') for line in data]
    pattern, value = zip(*data)
    pattern = [item.split(' ') for item in pattern]
    value = [item.split(' ') for item in value]
    df_clue = pd.DataFrame(data=[sorted(p, key=len) for p in pattern], columns=['1', '7', '4', '5d1', '5d2', '5d3', '6d1', '6d2', '6d3', '8'])
    df = pd.DataFrame(data=value, columns=['val_1', 'val_2', 'val_3', 'val_4'])
    full_df = pd.concat([df_clue, df], axis=1)
    return full_df.apply(np.vectorize(_index))


def number_items_of_length(values):
    """Return count of elements that have length 2, 3, 4 or 7"""
    values = values.apply(np.vectorize(len))
    total = 0
    for num in [2, 3, 4, 7] :
        total += (values == num).values.sum()
    return total


def decode(row):
    """Return decoded 4-digit values.

    Strategy:
        1, 4, 7, 8 are known by unique lengths (2, 4, 3 and 9).
        6-digit values:
            contains all of 4 -> 9
            contains all of 7 but not 4 -> 0
            other -> 6
        5 digit values:
            contains 1 -> 3
            shares 3 letters with 4 -> 5
            other -> 2
    """
    keys = {
        row['1']: 1,
        row['4']: 4,
        row['7']: 7,
        row['8']: 8
    }
    for item in row[['6d1', '6d2', '6d3']]:
        if set(row['4']).issubset(set(item)):
            keys[item] = 9
        elif set(row['7']).issubset(set(item)):
            keys[item] = 0
        else:
            keys[item] = 6
    for item in row[['5d1', '5d2', '5d3']]:
        if set(row['1']).issubset(set(item)):
            keys[item] = 3
        elif len(set(item).intersection(set(row['4']))) == 3:
            keys[item] = 5
        else:
            keys[item] = 2
    decoded = [keys[row[j]] for j in ['val_1', 'val_2', 'val_3', 'val_4']]

    return (np.array([1000, 100, 10, 1]) * np.array(decoded)).sum()




if __name__ == '__main__':

    values = parse_data()

    # Part 1
    # could do this with the decoded dataframe as well, but this is quick
    print(number_items_of_length(values[['val_1', 'val_2', 'val_3', 'val_4']]))


    # Part 2
    print(values.apply(decode, axis=1).sum())

