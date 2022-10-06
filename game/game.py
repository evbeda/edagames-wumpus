from application.action import Action
from application.initialize_chain_responsibility import initialize_chain_responsibility

from constants.constants import (
    CORRECT_MOVE,
    DEATH,
    DIAMOND,
    GET_ITEMS,
    GAME_OVER_MESSAGE_1,
    GAME_OVER_MESSAGE_2,
    GAME_OVER_MESSAGE_3,
    GAME_OVER_MESSAGE_4,
    GAME_OVER_MESSAGE_5,
    GAME_OVER_MESSAGE_6,
    GAME_OVER_MESSAGE_7,
    GAME_OVER_NOT_MET,
    GOLD,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    INVALID_ACTION,
    JOIN_ROW_BOARD,
    KILL,
    LARGE,
    MAXIMUM_INVALID_MOVES,
    PLAYER_1,
    PLAYER_2,
    SCORES,
    TIMEOUT_SC,
    VALID_ACTION,
)
import uuid
from game.board import Board
from game.player import Player
from game.utils import posibles_positions
from exceptions.personal_exceptions import (
    invalidMoveException,
)
import random


class WumpusGame():

    def __init__(self, users_names) -> None:
        self.game_id = str(uuid.uuid1())
        random.shuffle(users_names)
        self.player_1 = Player(PLAYER_1, users_names[0])
        self.player_2 = Player(PLAYER_2, users_names[1])
        self._board = Board()
        self._board.place_character_initial_pos(self.player_1.characters,
                                                INITIAL_POSITION_PLAYER_1,
                                                0)
        self._board.place_character_initial_pos(self.player_2.characters,
                                                INITIAL_POSITION_PLAYER_2,
                                                1)
        self.current_player = self.player_1
        self.inactive_player = self.player_2
        self.game_is_active = True
        self.remaining_moves = 200

    # def initial_diamond_position(self):
    #     self._board[random.randint(0, LARGE - 1)][LARGE//2].treasures.append(
    #         Diamond())

    def change_current_player(self):
        self.current_player = self.player_2 if (
            self.current_player == self.player_1
        ) else self.player_1
        self.inactive_player = self.player_1 if (
            self.current_player == self.player_2
        ) else self.player_2

    def put_danger_signal(self, parsed_cell: str, row, col):
        parsed_cell = list(parsed_cell)
        positions = posibles_positions(row, col)
        for p_row, p_col in positions:
            player_name = self._board._board[p_row][p_col].has_player
            if (
                player_name is not None
                and player_name != self.current_player.side
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
        For CORRECT_MOVE or INVALID_MOVE or TIMEOUT, or ARROW_MISS
        no payload is needed.
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
        else:
            self.current_player.update_score(SCORES[event])

    def _parse_cell(self, row: int, col: int) -> str:
        parsed_cell = self._board._board[row][col].to_str(
            self.current_player.side
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

    def execute_action(self, action: str, from_row: int, from_col: int, direction: str):
        try:
            action: Action = initialize_chain_responsibility(action)
            valid_message = action.execute(
                from_row,
                from_col,
                direction,
                self.current_player,
                self._board
            )
            self.current_player.invalid_moves_count = 0
            self.modify_score(valid_message)
            return VALID_ACTION
        except invalidMoveException:
            self.penalize_player()
            return INVALID_ACTION

    def penalize_player(self) -> None:
        self.current_player.penalize()
        self.modify_score(TIMEOUT_SC)
        self.check_the_limit_of_invalid()

    def generate_data(self) -> dict:
        return {
            "player_2": self.player_2.user_name,
            "player_1": self.player_1.user_name,
            "score_1": self.player_1.score,
            "score_2": self.player_2.score,
            "arrows_1": self.player_1.arrows,
            "arrows_2": self.player_2.arrows,
            "board": self.board,
            "remaining_turns": self.remaining_moves,
            "game_id": self.game_id,
            "side": self.current_player.side,
        }

    def generate_response(self):
        game_over_data = self.is_game_over()
        if not game_over_data[0]:
            return self.generate_data()
        else:
            final_message = self.game_over_final_message()
            return final_message

    def game_over_final_message(self):
        name_player_1, name_player_2 = self.player_1.user_name, self.player_2.user_name
        score_player_1 = self.player_1.score
        score_player_2 = self.player_2.score
        message = self.generate_data()

        if score_player_1 == score_player_2 and self.player_1.score == self.player_2.score:
            result = {
                "result": "DRAW"
            }
            message.update(result)

        else:
            result = {
                "result": {
                    'WINNER': (name_player_1 if score_player_1 > score_player_2
                               else name_player_2),
                    'LOSER': (name_player_2 if score_player_2 < score_player_1
                              else name_player_1),
                }
            }
            message.update(result)
        return message

    def check_the_limit_of_invalid(self) -> None:
        if self.current_player.invalid_moves_count >= MAXIMUM_INVALID_MOVES:
            self.current_player.penalizated_for_invalid_moves = True
            self.game_is_active = False

    def next_turn(self):
        self.remaining_moves -= 1
        self.change_current_player()

    def get_game_over_conditions_status(self) -> dict:
        game_over_conditions = {
            GAME_OVER_MESSAGE_4: len(self.player_1.characters) == 0,
            GAME_OVER_MESSAGE_5: len(self.player_2.characters) == 0,
            GAME_OVER_MESSAGE_3: (self.remaining_moves == 0 and
                                  self.player_1.score == self.player_2.score),
            GAME_OVER_MESSAGE_1: (self.player_1.invalid_moves_count) >= 5,
            GAME_OVER_MESSAGE_2: (self.player_2.invalid_moves_count) >= 5,
            GAME_OVER_MESSAGE_6: (self.remaining_moves == 0 and
                                  self.player_1.score > self.player_2.score),
            GAME_OVER_MESSAGE_7: (self.remaining_moves == 0 and
                                  self.player_1.score < self.player_2.score),
        }
        return game_over_conditions

    def is_game_over(self):
        '''
        Return a Tuple with (Boolean, String), where the first element
        is indicates if a Game Over condition has been met, and the second
        indicates the corresponding message. E.g.:
        (True, "GAME OVER - Player 1 has no living Characters...") indicates
        that a Game should end now, because player1 has no living Characters.
        '''
        dictionary = self.get_game_over_conditions_status()
        for key in dictionary:
            if dictionary[key]:
                return (True, key)
        return (False, GAME_OVER_NOT_MET)

    def get_current_player_name(self) -> str:
        if self.remaining_moves > 0 and self.game_is_active and self.all_player_have_characters():
            return self.current_player.user_name
        else:
            return ''

    def all_player_have_characters(self):
        return self.player_1.characters and self.player_2.characters
