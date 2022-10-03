from constans.constans import EAST, NORTH, SOUTH, WEST, LARGE
from game.board import Board
from game.character import Character
from game.player import Player


def is_a_player_character(row, col, current_player: Player, board: Board) -> bool:
    cell = board.get_cell(row, col)
    character: Character = cell.character
    if character:
        return character.player.side == current_player.side
    return False


def is_frendly_fire(row, col, direction, current_player: Player, board: Board) -> bool:
    target_row, target_col = target_position_within_bounds(row, col, direction)
    target_cell = board.get_cell(target_row, target_col)
    if target_cell.character:
        return target_cell.character.player.side == current_player.side
    return False


def there_are_arrows_available(current_player: Player) -> bool:
    return current_player.arrows > 0


def target_position_within_bounds(row: int, col: int, direction: str) -> "tuple[int, int]":
    directions = {
        EAST: (0, 1),
        SOUTH: (1, 0),
        WEST: (0, -1),
        NORTH: (-1, 0)
    }
    target_row = row + directions[direction][0]
    target_col = col + directions[direction][1]
    if (
        target_row < 0 or target_row > LARGE - 1
        or target_col < 0 or target_col > LARGE - 1
    ):
        return False
    return (target_row, target_col)
