import sys
import numpy as np

def parse_data():
    return [line.strip() for line in sys.stdin.readlines()]

def move_position(instructions):
    x = 0
    y = 0
    def move(command, value, x, y):
        if command == 'forward':
            x += value
        elif command == 'up':
            y -= value
        elif command == 'down':
            y += value
        return x, y

    for command in instructions:
        direction, value = command.split(' ')
        x, y = move(direction, int(value), x, y)
    return x, y


def move_with_aim(instructions):
    aim = 0
    x = 0
    y = 0
    def move(command, value, x, y, aim):
        if command == 'forward':
            x += value
            y += aim * value
        elif command == 'up':
            aim -= value
        elif command == 'down':
            aim += value
        return x, y, aim
    for command in instructions:
        direction, value = command.split(' ')
        x, y, aim = move(direction, int(value), x, y, aim)
    return x, y


if __name__ == '__main__':

    data = parse_data()

    # part 1
    print(np.multiply(*move_position(data)))

    # part 2
    print(np.multiply(*move_with_aim(data)))