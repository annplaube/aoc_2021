import sys
import numpy as np
from scipy.signal import argrelextrema
from skimage.segmentation import flood

def parse_data():
    """Parse data into numpy array."""
    return np.array([_make_array(line.strip()) for line in sys.stdin.readlines()])


def _make_array(string_input):
    return np.array([int(i) for i in string_input])


class Field:

    def __init__(self, data):
        self.field = data

    def valleys(self):
        """Return valley indices.
        Find 1-D valleys for each axis independently, then return intersection.
        Padding with max value to treat edge cases."""
        padded = np.pad(self.field, pad_width=1, mode='constant', constant_values=9)
        x_valleys = set(zip(*argrelextrema(padded, np.less, axis=1)))
        y_valleys = set(zip(*argrelextrema(padded, np.less, axis=0)))
        return [(i-1, j-1) for (i, j) in x_valleys.intersection(y_valleys)]

    @property
    def risk(self):
        """Return risk factor, defined as sum of (values at valley + 1)"""
        return sum([self.field[i, j] + 1 for (i, j) in self.valleys()])

    @property
    def basin_score(self):
        """Return product of the sizes of the three largest basins in the field"""
        basins = self.basins()
        return np.prod(sorted(basins)[-3:])

    def basins(self):
        """Return sizes of basis found by flooding the field.
        After thresholding the field at 9, skimage.segmentation.flood finds
        the basin around a seed point and returns a binary mask of it.
        """
        thresh = self.field.copy()
        thresh[thresh < 9] = 0
        return [flood(thresh, valley, connectivity=1).sum() for valley in self.valleys()]


if __name__ == '__main__':

    data = parse_data()

    # Part 1
    field = Field(data)
    print(field.risk)

    # Part 2
    print(field.basin_score)
