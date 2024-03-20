import inquirer
import numpy as np

class Player():

    def __init__(self) -> None:

        self.board = super() #'foo' # super()            # board creates the player class
        self.game = 'bar' # self.board.super()  # game creates the board class


class userPlayer(Player):

    def __init__(self, name):

        super().__init__()
        self.name = name # input("Enter Player Name: \n")

        return

    def choose_move(self, game, valid_moves):

        valid_move_strings = []
        for m in valid_moves:
            valid_move_strings.append(f'{m[0]} - {m[1]} {m[2]}')

        move_options = [inquirer.List("move", message="Select a Move", choices=valid_move_strings)]
        selected_move = inquirer.prompt(move_options)
        return_list = selected_move['move'].split()
        return_list.pop(1)

        return return_list
    
    def _compute_expected_value(self, move):
 
        color = move[1]
        value = move[2]

        checked_now = sum(self.board.__getattribute__(color).status)
        move_index = np.argwhere(self.board.__getattribute__(color).values == value)[0][0]

        if move_index < 10:
            val_move = checked_now + 1  # the 2nd check adds 2 points, 3rd adds 3, ... 9th adds 9.
        else:  # move_index == 10 is the last cell (2 or 12), need the score of the second as well.
            val_move = (checked_now + 1) + (checked_now + 2)  


        ev = val_move + val_remaining

        return ev


class randomPlayer(Player):

    def __init__(self, name):
        self.name = name

    def choose_move(self, game, valid_moves):

        selected_move = valid_moves[np.random.randint(0, len(valid_moves))]
        print(selected_move)

        return selected_move

