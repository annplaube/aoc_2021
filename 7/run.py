import sys
import numpy as np


def parse_data() -> np.ndarray:
    return np.array([int(i) for i in sys.stdin.readlines()[0].strip().split(',')])


def total_fuel_consumed_simple(data: np.ndarray) -> float:
    """Return total fuel consumed.
    Total fuel consumed is the sum of the absolute deviations from the median"""
    median = np.median(data)
    return sum([abs(i - median) for i in data])


def total_fuel_consumed_series(data: np.ndarray) -> float:
    """Minimise total_fuel_per_position"""
    search_range = range(min(data), max(data))
    consumption = [total_fuel_per_position(val, data) for val in search_range]
    return min(consumption)


def total_fuel_per_position(value: float, data: np.ndarray) -> float:
    """Return total fuel consumption for a given position.
    Fuel metric for a sub at distance x from desired location:
    0.5 * x * (x + 1)
    From sum of arithmetic series. x = abs(pos - value).
    """
    return 0.5 * sum((abs(data - value) + 1) * (abs(data - value)))


if __name__ == '__main__':


    data = parse_data()

    # Part 1
    fuel = total_fuel_consumed_simple(data)
    print(fuel)


    # Part 2
    print(total_fuel_consumed_series(data))