from constans.constans import (
    JOIN_ROW_BOARD,
    MAXIMUM_INVALID_MOVES,
    MOVE,
    SHOOT,
    PLAYER_1,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    PLAYER_2,
)
from constans.constants_game import (
    DIAMOND,
    GOLD,
    LARGE,
)
from constans.constants_scores import (
    SCORES,
    KILL,
    INVALID_MOVE,
    CORRECT_MOVE,
    ARROW_MISS,
    GET_ITEMS,
    TIMEOUT,
    DEATH,
    )
from game.board import Board
from game.player import Player
from game.utils import posibles_positions, translate_position
from exceptions.personal_exceptions import (
    invalidMoveException,
)


class WumpusGame():

    def __init__(self) -> None:
        self.player_1 = Player(PLAYER_1)
        self.player_2 = Player(PLAYER_2)
        self._board = Board()
        self._board.place_character_initial_pos(self.player_1.characters,
                                                INITIAL_POSITION_PLAYER_1,
                                                0)
        self._board.place_character_initial_pos(self.player_2.characters,
                                                INITIAL_POSITION_PLAYER_2,
                                                1)
        self.current_player = self.player_1
        self.game_is_active = True
        self.remaining_moves = 200

    # def initial_diamond_position(self):
    #     self._board[random.randint(0, LARGE - 1)][LARGE//2].treasures.append(
    #         Diamond())

    def change_current_player(self):
        self.current_player = self.player_2 if (
            self.current_player == self.player_1
            ) else self.player_1

    def put_danger_signal(self, parsed_cell: str, row, col):
        parsed_cell = list(parsed_cell)
        positions = posibles_positions(row, col)
        for p_row, p_col in positions:
            player_name = self._board._board[p_row][p_col].has_player
            if (
                player_name is not None
                and player_name != self.current_player.name
            ):
                parsed_cell[-1] = "+"

            if self._board._board[p_row][p_col].has_hole:
                parsed_cell[0] = "~"

        return "".join(parsed_cell)

    def modify_score(self, event, payload={}):
        '''
        Functions that modifies the score correspondingly, for players
        involved.
        Events are DEATH, GET_ITEMS, KILL, CORRECT_MOVE, INVALID_MOVE,
        TIMEOUT, ARROW_MISS. Payload is a dictionary,
        which contents varies according to event.
        For DEATH, Payload is {"character" = characterObject}, the character
        that dies.
        For GET_ITEMS, Payload is {"cell" = cellOject}, where cell is the cell
        where the character is getting into.
        For KILL, Payload is not needed, BUT, remember to call modify_score()
        with a DEATH event later, for the killed character.
        For CORRECT_MOVE or INVALID_MOVE or TIMEOUT, no payload is needed.
        '''
        if event == GET_ITEMS:
            cell = payload["cell"]
            score = cell.gold * SCORES[GOLD] + cell.diamond * SCORES[DIAMOND]
            self.current_player.update_score(score)
        elif event == DEATH:
            # it has to be removed, because this
            # functionally is done by treasure_treasure method
            char = payload["character"]
            score = (char.gold * SCORES[GOLD] +
                     char.diamond * SCORES[DIAMOND]) * -1
            char.player.update_score(score)
        elif event == KILL:
            self.current_player.update_score(SCORES[CORRECT_MOVE] + SCORES[KILL])
        elif event == CORRECT_MOVE:
            self.current_player.update_score(SCORES[CORRECT_MOVE])
        elif event == INVALID_MOVE:
            self.current_player.update_score(SCORES[INVALID_MOVE])
        elif event == TIMEOUT:
            self.current_player.update_score(SCORES[TIMEOUT])
        elif event == ARROW_MISS:
            self.current_player.update_score(SCORES[ARROW_MISS])

    def _parse_cell(self, row: int, col: int) -> str:
        parsed_cell = self._board._board[row][col].to_str(
            self.current_player.name
        )
        if '#' not in parsed_cell:
            parsed_cell = self.put_danger_signal(parsed_cell, row, col)
        return parsed_cell

    @property
    def board(self):
        user_board = list()

        for row in range(LARGE):
            buf = ''
            for col in range(LARGE):
                buf += self._parse_cell(row, col)
            user_board.append(buf)

        return JOIN_ROW_BOARD.join(user_board)

    def execute_action(self, action, from_row, from_col, direction):
        to_row, to_col = translate_position(from_row, from_col, direction)
        try:
            if action == MOVE:
                valid_message = self._board.is_valid_move(from_row, from_col,
                                                          to_row, to_col,
                                                          self.current_player)
            elif action == SHOOT:
                valid_message = self._board.shoot_arrow(from_row, from_col, direction,
                                                        self.current_player)
            self.current_player.invalid_moves_count = 0
            self.modify_score(valid_message)
        except invalidMoveException:
            self.current_player.invalid_moves_count += 1
            self.modify_score(INVALID_MOVE)

    def penalize_player(self) -> None:
        self.current_player.penalize()
        self.modify_score(TIMEOUT)
        self.check_the_limit_of_invalid()

    def generate_response(self) -> dict:
        response = {
            "board": self.board,
            # "game_status": self.is_game_active, # Add property when ready
            # "turn": self.current_turn # Add property later
            "player1": {
                "name": self.player_1.name,
                "score": self.player_1.score,
                "arrows": self.player_1.arrows,
                "characters_alive": len(self.player_1.characters),
            },
            "player2": {
                "name": self.player_2.name,
                "score": self.player_2.score,
                "arrows": self.player_2.arrows,
                "characters_alive": len(self.player_2.characters),
            }
        }
        return response

    def game_over_final_message(self):
        name_player_1, name_player_2 = self.player_1.name, self.player_2.name
        score_player_1 = self.player_1.score
        score_player_2 = self.player_2.score
        if score_player_1 == score_player_2:
            return {
                'GAME_OVER': {
                    'SCORE': {
                        name_player_1: score_player_1,
                        name_player_2: score_player_2,
                    },
                    'RESULT': 'DRAW',
                },
            }
        return {
            'GAME_OVER': {
                'SCORE': {
                    name_player_1: score_player_1,
                    name_player_2: score_player_2,
                },
                'RESULT': {
                    'WINNER': (name_player_1 if score_player_1 > score_player_2
                               else name_player_2),
                    'LOSER': (name_player_2 if score_player_2 < score_player_1
                              else name_player_1),
                }
            }
        }

    def check_the_limit_of_invalid(self) -> None:

        if self.current_player.invalid_moves_count >= MAXIMUM_INVALID_MOVES:
            self.current_player.penalizated_for_invalid_moves = True
            self.game_is_active = False

    def next_turn(self):
        self.remaining_moves -= 1
        self.change_current_player()
