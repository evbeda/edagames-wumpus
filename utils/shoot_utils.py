from game.player import Player


def shoot_arrow(player: Player, position, direction):
    if player.arrows < 1:
        raise Exception("INVALID MOVE")
