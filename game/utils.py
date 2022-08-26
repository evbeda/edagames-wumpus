from constans.constants_game import LARGE
from constans.constants_utils import WEST, NORTH, SOUTH, EAST


def posibles_positions(row, col):
    positions = {
        "nort": (row - 1, col),
        "sout": (row + 1, col),
        "east": (row, col + 1),
        "west": (row, col - 1)
    }

    if row - 1 < 0:
        del (positions['nort'])
    if row + 1 >= LARGE:
        del (positions['sout'])
    if col + 1 >= LARGE:
        del (positions['east'])
    if col - 1 < 0:
        del (positions['west'])

    return list(positions.values())


def translate_direction(from_row, from_col, direction):
    if direction == NORTH:
        to_row = from_row - 1
        to_col = from_col
    elif direction == SOUTH:
        to_row = from_row + 1
        to_col = from_col
    elif direction == EAST:
        to_col = from_col + 1
        to_row = from_row
    elif direction == WEST:
        to_col = from_col - 1
        to_row = from_row
    return to_row, to_col
