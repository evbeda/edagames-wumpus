import random
from constans.constans import (
    FORBIDDEN_HOLE_CELLS,
    INITIAL_POSITIONS,
    JOIN_ROW_BOARD,
    PLAYER_1,
    INITIAL_POSITION_PLAYER_1,
    INITIAL_POSITION_PLAYER_2,
    PLAYER_2
)
from constans.constants_game import (
    DIAMOND,
    GOLD,
    GOLD_QUANTITY,
    HOLE,
    HOLE_QUANTITY,
    LARGE,
    MIDDLE
)
from constans.constants_scores import (
    SCORES,
    KILL,
    INVALID_MOVE,
    CORRECT_MOVE,
    ARROW_MISS,
    GET_ITEMS,
    TIMEOUT,
    DEATH

    )
from constans.constants_utils import MOVE, NORTH, SHOOT, SOUTH, EAST, WEST

from game.cell import Cell
from game.character import Character
from game.diamond import Diamond
from game.gold import Gold
from game.player import Player
from game.utils import posibles_positions, translate_position
from exceptions.personal_exceptios import (moveToYourOwnCharPositionException,
                                           notYourCharacterException,
                                           noPossibleMoveException,
                                           noArrowsAvailableException,
                                           friendlyFireException,
                                           shootOutOfBoundsException,
                                           invalidMoveException)


class WumpusGame():

    def __init__(self) -> None:

        self._board = [
            [Cell(i, j) for j in range(LARGE)] for i in range(LARGE)
        ]

        self.player_1 = Player(PLAYER_1)
        self.player_2 = Player(PLAYER_2)
        self.place_items(GOLD, GOLD_QUANTITY)
        self.place_items(HOLE, HOLE_QUANTITY)
        self.place_character_initial_pos(
            self.player_1,
            Character(self.player_1),
            Character(self.player_1),
            Character(self.player_1)
        )
        self.place_character_initial_pos(
            self.player_2,
            Character(self.player_2),
            Character(self.player_2),
            Character(self.player_2)
        )
        self.current_player = self.player_1

    def move_to_own_character_position(self, player_game, row_to, col_to):
        ch = self._board[row_to][col_to].character
        if ch and ch.player == player_game:
            self.modify_score(INVALID_MOVE)
            raise moveToYourOwnCharPositionException()

    def place_character_initial_pos(
        self,
        player: Player,
        character1: Character,
        character2: Character,
        character3: Character
    ) -> None:
        list_positions = INITIAL_POSITION_PLAYER_1 if (
            player.name == PLAYER_1
            ) else INITIAL_POSITION_PLAYER_2

        character_positions = {
            list_positions[0]: character1,
            list_positions[1]: character2,
            list_positions[2]: character3
        }

        for (row, col), character in character_positions.items():
            self._board[row][col].character = character
            if player.name == PLAYER_1:
                self._board[row][col].is_discover[0] = True
            else:
                self._board[row][col].is_discover[1] = True

    def place_items(self, item, item_quantity):
        fisrt_half = (0, MIDDLE-1)
        second_half = (MIDDLE + 1, LARGE - 1)

        for start, end in [fisrt_half, second_half]:
            for _ in range(item_quantity//2):
                self.place_items_in_free_position(start, end, item)

    def place_items_in_free_position(self, start: int, end: int, item):

        while True:  # busca hasta encontrar una posicion libre
            row = random.randint(0, LARGE - 1)
            col = random.randint(start, end)
            if self._is_valid(row, col, item):
                if item == GOLD:
                    self._board[row][col].treasures.append(Gold())
                elif item == HOLE:
                    self._board[row][col].has_hole = True
                break

    def _is_valid(self, row, col, item) -> bool:
        valid = ((row, col) not in INITIAL_POSITIONS
                 and self._board[row][col].empty)
        if item == HOLE and valid:
            valid = self._valid_hole(row, col)
        return valid

    def initial_diamond_position(self):
        self._board[random.randint(0, LARGE - 1)][LARGE//2].treasures.append(
            Diamond())

    def _valid_hole(self, row: int, col: int) -> bool:

        if (row, col) not in FORBIDDEN_HOLE_CELLS:

            self._board[row][col].has_hole = True
            golds = self._gold_positions()
            for row_player, col_player in INITIAL_POSITIONS:
                return self._player_can_find_gold(row_player, col_player,
                                                  golds)
        else:
            return False

    def _player_can_find_gold(self, row, col, golds):
        for gold_position in golds:
            if not self._can_find_gold(row, col, gold_position, []):
                self._board[row][col].has_hole = False
                return False
        return True

    def _can_find_gold(self, row, col, gold_position, visited):
        visited.append((row, col,))

        if (row, col) == gold_position:
            return True
        possible_moves = posibles_positions(row, col)

        for row_next, col_next in possible_moves:

            if (
                (row_next, col_next) not in visited and
                not self._board[row_next][col_next].has_hole and
                self._can_find_gold(row_next, col_next,
                                    gold_position, visited)
            ):
                return True
        return False

    def discover_cell(self, row, col):
        cell = self._board[row][col]
        if self.current_player == self.player_1:
            cell.is_discover[0] = True
        else:
            cell.is_discover[1] = True

    def _gold_positions(self) -> 'list[tuple]':
        return [
            (row, col)
            for row in range(LARGE)
            for col in range(LARGE)
            if self._board[row][col].gold > 0
        ]

    def change_current_player(self):
        self.current_player = self.player_2 if (
            self.current_player == self.player_1
            ) else self.player_1

    def is_valid_move(self, from_row, from_col, to_row, to_col, player_game):
        coordinates = (to_row, to_col)
        if not self.is_a_player_character(from_row, from_col, player_game):
            self.modify_score(INVALID_MOVE)
            raise notYourCharacterException()
        if (coordinates not in posibles_positions(from_row, from_col)):
            self.modify_score(INVALID_MOVE)
            raise noPossibleMoveException()
        self.move_to_own_character_position(player_game, to_row, to_col)
        dictionary = {
            "from_row": from_row,
            "from_col": from_col,
            "to_row": to_row,
            "to_col": to_col,
            "player": player_game,
        }
        self.filter_move(dictionary)

    def is_a_player_character(self, row, col, player_game):
        result = self._board[row][col].character.player == player_game
        return result

    def put_danger_signal(self, parsed_cell: str, row, col):

        parsed_cell = list(parsed_cell)
        positions = posibles_positions(row, col)
        for p_row, p_col in positions:

            player_name = self._board[p_row][p_col].has_player
            if (
                player_name is not None
                and player_name != self.current_player.name
            ):
                parsed_cell[-1] = "+"

            if self._board[p_row][p_col].has_hole:
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
            self.current_player.update_score(SCORES[KILL])
        elif event == CORRECT_MOVE:
            self.current_player.update_score(SCORES[CORRECT_MOVE])
        elif event == INVALID_MOVE:
            self.current_player.update_score(SCORES[INVALID_MOVE])
        elif event == TIMEOUT:
            self.current_player.update_score(SCORES[TIMEOUT])
        elif event == ARROW_MISS:
            self.current_player.update_score(SCORES[ARROW_MISS])

    def make_move(self, dictionary):
        from_row = dictionary["from_row"]
        from_col = dictionary["from_col"]
        to_row = dictionary["to_row"]
        to_col = dictionary["to_col"]
        new_cell: Cell = self._board[to_row][to_col]
        old_cel = self._board[from_row][from_col]
        self.modify_score(CORRECT_MOVE)
        character: Character = self._board[from_row][from_col].character
        character.player.arrows += new_cell.arrow
        new_cell.transfer_tresaure(character)
        new_cell.arrow = 0
        new_cell.character = character
        old_cel.character = None
        self.discover_cell(to_row, to_col)

    def filter_move(self, dictionary):
        cell_to = self._board[dictionary["to_row"]][dictionary["to_col"]]
        player_dic = dictionary["player"]
        character_cel = cell_to.character
        if cell_to.has_hole or (character_cel and
                                character_cel.player.name != player_dic):
            cell = self._board[dictionary["from_row"]][dictionary["from_col"]]
            char = cell.character
            char.transfer_tresaure(cell)
        else:
            self.make_move(dictionary)

    def shoot_arrow(self, row, col, direction):

        if self.current_player.arrows < 1:
            raise noArrowsAvailableException()

        target_row, target_col = self.target_position(row, col, direction)
        target_cell = self._board[target_row][target_col]

        if (target_cell.character is not None and
           target_cell.character.player.name == self.current_player.name):
            self.current_player.arrows -= 1
            raise friendlyFireException()

        if (target_cell.character is not None and
           target_cell.character.player.name != self.current_player.name):
            self.kill_opp(target_row, target_col)
            return

        if target_cell.has_hole:
            self.shoot_hole(target_row, target_col)
            return

        if target_cell.character is None:
            self.shoot_miss(target_row, target_col)
            return

    def target_position(self, row, col, direction):
        directions = {EAST: (0, 1), SOUTH: (1, 0),
                      WEST: (0, -1), NORTH: (-1, 0)}
        target_row = row + directions[direction][0]
        target_col = col + directions[direction][1]
        if (target_row < 0 or target_row > LARGE - 1
           or target_col < 0 or target_col > LARGE - 1):
            self.modify_score(INVALID_MOVE)
            raise shootOutOfBoundsException()
        return (target_row, target_col)

    def kill_opp(self, row, col):
        self.current_player.arrows -= 1
        cell = self._board[row][col]
        character_to_kill = cell.character
        character_to_kill.transfer_tresaure(cell)
        self.modify_score(DEATH,
                          {"character": character_to_kill})
        self.modify_score(KILL)
        cell.character = None
        self.discover_cell(row, col)

    def shoot_miss(self, row, col):
        self.discover_cell(row, col)
        self.current_player.arrows -= 1
        self._board[row][col].arrow += 1
        self.modify_score(ARROW_MISS)

    def shoot_hole(self, row, col):
        self.discover_cell(row, col)
        self.current_player.arrows -= 1
        self.modify_score(CORRECT_MOVE)

    def _parse_cell(self, row: int, col: int) -> str:
        parsed_cell = self._board[row][col].to_str(self.current_player.name)
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

    def action_manager(self, action, from_row, from_col, direction):
        to_row, to_col = translate_position(from_row, from_col, direction)
        try:
            if action == MOVE:
                self.is_valid_move(
                    from_row,
                    from_col,
                    to_row,
                    to_col,
                    self.current_player)

            elif action == SHOOT:
                self.shoot_arrow(from_row, from_col, direction)

            self.current_player.invalid_moves_count = 0

        except invalidMoveException:
            self.current_player.invalid_moves_count += 1

    def generate_response(self) -> dict:
        response = {
            "board": self.board,
            # "game_status": self.is_game_active, # Add property when ready
            # "turn": self.current_turn # Add property when ready
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
