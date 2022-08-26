from game.cell import Cell
from game.game import WumpusGame
from game.player import Player
from constans.constans import PLAYER_1, PLAYER_2
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
    reveal_cell(row, col, game)


def reveal_cell(row, col, game: WumpusGame):

    if game.current_player.name == PLAYER_1:
        game._board[row][col].is_discover_by_player_1 = True

    if game.current_player.name == PLAYER_2:
        game._board[row][col].is_discover_by_player_2 = True
