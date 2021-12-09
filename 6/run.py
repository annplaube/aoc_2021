import sys
import numpy as np
from collections import Counter

def parse_data():
    """
    Return list (len 9) of number of fish by due date.

    I.e. list[0] represents the number of fish spawning the next day,
    list[5] represents the number of fish spawning in 6 days.
    """
    fish = sys.stdin.readlines()[0].strip()
    fish = [int(i) for i in fish.split(',')]
    counter = Counter(fish)
    return [counter[i] for i in range(9)]


def age_n_days(school, days):
    """
    Age school by the number of days.

    Each day, the number of fish due in n days becomes the number of fish due
    in n+1 days (roll by -1). The "parents" are added to the "due in 7 days" index.
    """
    for i in range(days):
        school = np.roll(school, -1)
        school[6] += school[8]
    return school


if __name__ == '__main__':


    data = parse_data()
    print(data)

    # Part 1
    fish_by_due_day = age_n_days(data, 80)

    total = sum(fish_by_due_day)
    print(total)

    # Part 2
    fish_by_due_day = age_n_days(data, 256)
    print(sum(fish_by_due_day))