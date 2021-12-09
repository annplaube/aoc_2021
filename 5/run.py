import sys
import numpy as np
import pandas as pd

def parse_data() -> pd.DataFrame:
    """Parse data"""
    instructions = []
    for line in sys.stdin.readlines():
        data = line.strip()
        pair_1, pair_2 = data.split(' -> ')
        x1, y1 = pair_1.split(',')
        x2, y2 = pair_2.split(',')
        instructions.append(
            {'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2)}
        )
    return pd.DataFrame(instructions)


class Field:
    def __init__(self, data, no_diagonal=True):
        if no_diagonal:
            data = self._filter_diagonal(data)
        self.field = self._fill_field(data)

    @property
    def danger_score(self) -> int:
        """Return count of points where field has value > 1 (> 2 lines intersect)"""
        return len(np.where(self.field > 1)[0])

    def _filter_diagonal(self, data: pd.DataFrame) -> pd.DataFrame:
        """Only retain horizontal and vertical lines (where x1 == x2 or y1 == y2)"""
        return data[(data.x1 == data.x2) | (data.y1 == data.y2)]

    def _fill_field(self, data: pd.DataFrame) -> np.ndarray:
        """Initialise field with zeros, then add lines"""
        field = self._initialise_field(data)
        lines = data.apply(self._make_line_indices, axis=1)
        for point_x, point_y in [item for sublist in lines.values for item in sublist]:
            field[point_y, point_x] += 1
        return field

    def _initialise_field(self, data: pd.DataFrame) -> np.ndarray:
        """Initialise field of zeros of max(x) and max(y) dimension"""
        horizontal_dim = data[["x1", "x2"]].max().max() + 1
        vertical_dim = data[["y1", "y2"]].max().max() + 1
        return np.zeros((vertical_dim, horizontal_dim))

    def _make_line_indices(self, row: pd.Series) -> list:
        """Generate list of indices from one row of input data"""
        sign_x = self._sign(row.x1, row.x2)
        sign_y = self._sign(row.y1, row.y2)
        if row.x1 == row.x2:
            return [(row.x1, i) for i in range(row.y1, row.y2 + sign_y, sign_y)]
        if row.y1 == row.y2:
            return [(i, row.y1) for i in range(row.x1, row.x2 + sign_x, sign_x)]
        return [(i, j) for i, j in zip(
            range(row.x1, row.x2 + sign_x, sign_x),
            range(row.y1, row.y2 + sign_y, sign_y))]

    def _sign(self, v1: int, v2: int) -> int:
        """Determine sign for ranges to go back-/forwards as necessary"""
        if v1 > v2:
            return -1
        return 1


if __name__ == '__main__':

    data = parse_data()

    # Part 1
    field = Field(data, no_diagonal=True)
    print(field.danger_score)

    # Part 2
    field = Field(data, no_diagonal=False)
    print(field.danger_score)
