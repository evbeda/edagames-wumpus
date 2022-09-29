from constans.constants_game import LARGE
from constans.constans import (
    PLAYER_1,
    PLAYER_2,
    NAME_USER_1,
    NAME_USER_2,
)
from game.cell import Cell
from game.character import Character
from game.player import Player
from game.diamond import Diamond
from game.gold import Gold


def board_friendly_fire_player_1():
    FRIENDLY_FIRE_BOARD = [
        [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

    player_1 = Player(PLAYER_1, NAME_USER_1)
    character1 = Character(player_1)
    character2 = Character(player_1)
    character3 = Character(player_1)
    FRIENDLY_FIRE_BOARD[0][0].character = character1
    FRIENDLY_FIRE_BOARD[0][1].character = character2
    FRIENDLY_FIRE_BOARD[0][8].character = character3
    return FRIENDLY_FIRE_BOARD


def board_friendly_fire_player_2():
    FRIENDLY_FIRE_BOARD_P2 = [
        [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]
    player_2 = Player(PLAYER_2, NAME_USER_2)
    character1 = Character(player_2)
    character2 = Character(player_2)
    character3 = Character(player_2)
    FRIENDLY_FIRE_BOARD_P2[0][16].character = character1
    FRIENDLY_FIRE_BOARD_P2[0][15].character = character2
    FRIENDLY_FIRE_BOARD_P2[8][16].character = character3
    return FRIENDLY_FIRE_BOARD_P2


def board_kill_opp_player():
    KILL_OP_BOARD_1 = [
        [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

    player_1 = Player(PLAYER_1, NAME_USER_1)
    character1_p1 = Character(player_1)
    character2_p1 = Character(player_1)
    character3_p1 = Character(player_1)

    character3_p1.treasures.append(Diamond())
    character3_p1.treasures.append(Gold())
    character3_p1.treasures.append(Gold())

    player_1.characters.append(character1_p1)
    player_1.characters.append(character2_p1)
    player_1.characters.append(character3_p1)

    player_2 = Player(PLAYER_2, NAME_USER_2)
    character1_p2 = Character(player_2)
    character2_p2 = Character(player_2)
    character3_p2 = Character(player_2)

    player_2.characters.append(character1_p2)
    player_2.characters.append(character2_p2)
    player_2.characters.append(character3_p2)

    character1_p2.treasures.append(Gold())
    character1_p2.treasures.append(Gold())

    KILL_OP_BOARD_1[0][15].character = character1_p1
    KILL_OP_BOARD_1[16][0].character = character2_p1
    KILL_OP_BOARD_1[8][14].character = character3_p1
    KILL_OP_BOARD_1[0][16].character = character1_p2
    KILL_OP_BOARD_1[16][16].character = character2_p2
    KILL_OP_BOARD_1[8][15].character = character3_p2
    return KILL_OP_BOARD_1


def shoot_arrow_board():
    SHOOT_ARROW = [
        [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

    player_1 = Player(PLAYER_1, NAME_USER_1)
    character1 = Character(player_1)
    character2 = Character(player_1)
    character3 = Character(player_1)

    player_1.characters.append(character1)
    player_1.characters.append(character2)
    player_1.characters.append(character3)

    player_2 = Player(PLAYER_2, NAME_USER_2)
    character1_p2 = Character(player_2)
    character2_p2 = Character(player_2)
    character3_p2 = Character(player_2)

    player_2.characters.append(character1_p2)
    player_2.characters.append(character2_p2)
    player_2.characters.append(character3_p2)

    SHOOT_ARROW[0][4].character = character1
    SHOOT_ARROW[8][10].character = character2
    SHOOT_ARROW[15][5].character = character3
    SHOOT_ARROW[0][5].has_hole = True
    SHOOT_ARROW[0][16].character = character1_p2
    SHOOT_ARROW[5][6].character = character2_p2
    SHOOT_ARROW[15][6].character = character3_p2

    return SHOOT_ARROW


# shoot to hole
def board_shoot_hole_player_1():
    SHOOT_H0LE_BOARD_1 = [[Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

    player_1 = Player(PLAYER_1, NAME_USER_1)
    character1 = Character(player_1)
    character2 = Character(player_1)
    character3 = Character(player_1)

    player_1.characters.append(character1)
    player_1.characters.append(character2)
    player_1.characters.append(character3)

    SHOOT_H0LE_BOARD_1[0][7].character = character1
    SHOOT_H0LE_BOARD_1[7][10].character = character2
    SHOOT_H0LE_BOARD_1[15][14].character = character3
    SHOOT_H0LE_BOARD_1[6][10].has_hole = True
    SHOOT_H0LE_BOARD_1[16][14].has_hole = True

    return SHOOT_H0LE_BOARD_1


# shoot to hole
def board_shoot_hole_player_2():
    SHOOT_H0LE_BOARD_2 = [
        [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

    player_2 = Player(PLAYER_2, NAME_USER_2)
    character1 = Character(player_2)
    character2 = Character(player_2)
    character3 = Character(player_2)

    player_2.characters.append(character1)
    player_2.characters.append(character2)
    player_2.characters.append(character3)

    SHOOT_H0LE_BOARD_2[0][16].character = character1
    SHOOT_H0LE_BOARD_2[5][6].character = character2
    SHOOT_H0LE_BOARD_2[13][2].character = character3
    SHOOT_H0LE_BOARD_2[5][7].has_hole = True
    SHOOT_H0LE_BOARD_2[13][1].has_hole = True

    return SHOOT_H0LE_BOARD_2


def board_empty_cell():
    SHOOT_EMPTY_CELL = [
        [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)]

    player_1 = Player(PLAYER_1, NAME_USER_1)
    character1 = Character(player_1)
    character2 = Character(player_1)
    character3 = Character(player_1)

    player_1.characters.append(character1)
    player_1.characters.append(character2)
    player_1.characters.append(character3)

    SHOOT_EMPTY_CELL[0][4].character = character1
    SHOOT_EMPTY_CELL[7][10].character = character2
    SHOOT_EMPTY_CELL[13][5].character = character3

    return SHOOT_EMPTY_CELL
