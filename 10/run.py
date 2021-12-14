import sys
import numpy as np

def parse_data():
    return [line.strip() for line in sys.stdin.readlines()]


Matcher = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

Score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

IncompleteScore = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4

}

def score_corrupted_line(line):
    # keep track of which brackets to close next
    to_close = []
    for character in line:
        if character in ['(', '[', '{', '<']:
            to_close.append(character)
        elif character == Matcher[to_close[-1]]:
            # remove closed bracket from end of buffer
            to_close.pop(-1)
        else:
            # non-matching bracket determines score
            return Score[character]
    # line incomplete, but not corrupted, no score
    return 0


def score_incomplete_line(line):
    # keep track of which brackets to close next
    to_close = []
    for character in line:
        if character in ['(', '[', '{', '<']:
            to_close.append(character)
        elif character == Matcher[to_close[-1]]:
            # remove closed bracket from end of buffer
            to_close.pop(-1)
        else:
            # corrupted line gets no auto-complete score
            return np.nan
    score = 0
    # minimum number of brackets to close are those in reverse order of to_close
    # save one lookup by assigning scores to opening instead of closing brackets.
    for character in to_close[::-1]:
        score = score * 5 + IncompleteScore[character]
    return score



if __name__ == '__main__':

    data = parse_data()

    # Part 1
    print(sum([score_corrupted_line(line) for line in data]))


    # Part 2
    print(np.nanmedian([score_incomplete_line(line) for line in data]))

