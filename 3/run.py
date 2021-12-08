import sys
import numpy as np

def parse_data():
    """Parse data into a 2-D numpy array for vector calculations"""
    return np.array([_make_array(line.strip()) for line in sys.stdin.readlines()])


def gamma_rate(vector_data):
    """Return gamma rate as decimal string (rounding up 0.5 to 1)"""
    length, _ = vector_data.shape
    gamma_vector = vector_data.sum(axis=0) / length

    return ''.join([str(int(i)) for i in np.rint(np.nextafter(gamma_vector, gamma_vector + 1))])


def epsilon_rate(binary_string):
    """Return corresponding epsilon rate as binary string (bit-wise complement)"""
    return ''.join([str(int(not int(i))) for i in binary_string])


def multiply_gamma_epsilon(gamma, epsilon):
    """Return decimal product of binary strings gamma and epsilon"""
    return int(gamma, 2) * int(epsilon, 2)


def oxygen_rate(vector_data):
    position = 0
    while vector_data.shape[0] > 1:
        criterion = gamma_rate(vector_data)[position]

        # delete rows from data where bit is not matching criterion
        rows_to_delete = np.where(vector_data[:, position] != int(criterion))[0]
        vector_data = np.delete(vector_data, rows_to_delete, axis=0)
        position += 1
    return ''.join([str(int(i)) for i in vector_data[0]])


def co2_rate(vector_data):
    position = 0
    while vector_data.shape[0] > 1:
        criterion = gamma_rate(vector_data)[position]

        # delete rows from data where bit is not matching co2 criterion
        # i.e. where it is matching ox criterion
        rows_to_delete = np.where(vector_data[:, position] == int(criterion))[0]
        vector_data = np.delete(vector_data, rows_to_delete, axis=0)
        position += 1
    return ''.join([str(int(i)) for i in vector_data[0]])


def life_support_rating(vector_data):
    """Return decimal product of oxygen_rate and co2_rate binary strings"""
    ox = oxygen_rate(vector_data)
    co2 = co2_rate(vector_data)
    return int(ox, 2) * int(co2, 2)


def _make_array(string_input):
    return np.array([int(i) for i in string_input])


if __name__ == '__main__':

    data = parse_data()

    # Part 1
    gamma = gamma_rate(data)
    epsilon = epsilon_rate(gamma)

    solution = multiply_gamma_epsilon(gamma, epsilon)
    print(solution)

    # Part 2
    life_support = life_support_rating(data)
    print(life_support)
