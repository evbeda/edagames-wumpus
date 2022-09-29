from application.action import Action
from application.move import Move
from application.move_and_die import MoveAndDie
from application.move_to_empty import MoveToEmpty
from application.move_to_hole import MoveToHole
from application.shoot_arrow import ShootArrow
from application.shoot_and_kill import ShootAndKill
from application.shoot_to_hole import ShootToHole
from application.shoot_to_empty_cell import ShootEmptyCell
from constans.constans import MOVE, SHOOT


def initialize_chain_responsibility(action: str) -> Action:

    if action == SHOOT:

        # initialize classes
        shoot_arrow = ShootArrow()
        shoot_and_kill = ShootAndKill()
        shoot_to_hole = ShootToHole()
        shoot_to_empty_cell = ShootEmptyCell()

        # set chain of responsability
        shoot_arrow.set_next(shoot_and_kill)
        shoot_and_kill.set_next(shoot_to_hole)
        shoot_to_hole.set_next(shoot_to_empty_cell)

        return shoot_arrow

    elif action == MOVE:

        # initialize classes
        move = Move()
        move_and_die = MoveAndDie()
        move_to_hole = MoveToHole()
        move_to_empty_cell = MoveToEmpty()

        # set chain of responsability
        move.set_next(move_and_die)
        move_and_die.set_next(move_to_hole)
        move_to_hole.set_next(move_to_empty_cell)

        return move
