from constans.constans import LARGE


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
