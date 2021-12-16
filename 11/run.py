import sys
import numpy as np


def parse_data():
    """Parse data into numpy array."""
    return np.array([_make_array(line.strip()) for line in sys.stdin.readlines()])

def _make_array(string_input):
    return np.array([int(i) for i in string_input])


class Consortium:

    def __init__(self, data):
        self.octopuses = np.array(data)

    @property
    def flash_count(self):
        """Return number of flashing octopuses."""
        return np.count_nonzero(self.octopuses == 0)

    def age_one_step(self):
        """Age the consortium by one step.
        At each step:
            - each octopus has its energy level increased by 1
            - each octopus that has an energy level > 9 flashes
            - each octopus adjacent to a flashing one has its energy level
            increased by 1 and may itself become a flash
            - the step is complete when there are no new flashes
        """
        self.octopuses += 1
        # keep track of which octopus has flashed (can only flash once)
        old_flashes = []

        # find new flash locations (energy level > 9, not flashed yet)
        flash_locations = self.find_flash(self.octopuses, old_flashes)

        # repeat while there are new flashes
        while len(flash_locations) > 0:
            for x, y in flash_locations:
                self.octopuses[max(x-1,0):x+2, max(y-1,0):y+2] += 1
                old_flashes.append((x,y))
            flash_locations = self.find_flash(self.octopuses, old_flashes)

        self.octopuses[self.octopuses > 9] = 0


    def find_flash(self, data, previous):
        """Return indices of flash (> 9) not in previous as list of 2-tuples"""
        flashes = list(zip(*np.where(data > 9)))
        return [flash for flash in flashes if flash not in previous]



if __name__ == '__main__':

    data = parse_data()

    # Part 1
    consortium = Consortium(data)

    flash_count = 0
    for i in range(0, 100):
        consortium.age_one_step()
        flash_count += consortium.flash_count

    print(flash_count)


    # Part 2
    consortium = Consortium(data)

    step_count = 0
    while not np.all(consortium.octopuses == 0):
        consortium.age_one_step()
        step_count += 1

    print(step_count)

