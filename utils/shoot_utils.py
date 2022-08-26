from game.cell import Cell
from game.game import WumpusGame
from game.player import Player
from constans.constants_game import LARGE
from constans.constants_utils import NORTH, SOUTH, EAST, WEST


def shoot_arrow(player: Player, row, col, direction, game: WumpusGame):

    if player.arrows < 1:
        raise Exception("INVALID MOVE - no arrows available")

    player.arrows -= 1

    target_row, target_col = target_position(row, col, direction)
    target_cell: Cell = game._board[target_row][target_col]

    if (target_cell.character is not None and
       target_cell.character.player.name == player.name):
        raise Exception("INVALID MOVE - Friendly fire")

    if (target_cell.character is not None and
       target_cell.character.player.name != player.name):
        kill_opp(row, col, game)

    if target_cell.character is None:
        shoot_miss(row, col, game)


def target_position(row, col, direction):
    directions = {EAST: (0, -1), SOUTH: (1, 0), WEST: (0, 1), NORTH: (-1, 0)}
    target_row = row + directions[direction][0]
    target_col = col + directions[direction][1]
    if (target_row < 0 or target_row > LARGE - 1
       or target_col < 0 or target_col > LARGE - 1):
        raise Exception("INVALID MOVE - Shoot out of bounds")
    return (target_row, target_col)


def kill_opp(row, col, game: WumpusGame):
    # leave opp items in the cell
    # remove opp from the cell
    game.drop_items(row, col)
    # TODO decrease opp score
    # TODO increase player score
    # reveal cell to the player
    game.discover_cell(row, col)


def shoot_miss(row, col, game: WumpusGame):
    game.discover_cell(row, col)
    game.current_player.arrows -= 1
    game._board[row][col].arrow += 1
