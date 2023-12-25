import numpy as np
#import pandas as pd

class Game:

    def __init__(self, players=1) -> None:
        self.players = players
        self.boards = []

        for player in range(self.players):
            self.boards.append(Board())

        np.random.seed(32)

        return
    
    def __str__(self):

        lines = ''
        for i, player in enumerate(range(self.players)):
            lines += f"Player {i + 1}'s board:\n"
            lines += print(self.boards[i])
            lines += '\n'

        return
    
    def roll_dice(self):

        # roll dice
        dice = {'w1' : None, 'w2': None, 'red' : None, 'yellow': None, 'green': None, 'blue': None}
        values = np.random.randint(low=1, high=6, size=len(dice))
        for i, die in enumerate(dice.items()):
            dice[die[0]] = values[i]

        # compute moves
        moves = {}
        wild = dice['w1'] + dice['w2']
        moves['wild'] = wild
        moves['reds'] = list(set([dice['w1'] + dice['red'], dice['w2'] + dice['red'], wild]))
        moves['yellows'] = list(set([dice['w1'] + dice['yellow'], dice['w2'] + dice['yellow'], wild]))
        moves['blues'] = list(set([dice['w1'] + dice['blue'], dice['w2'] + dice['blue'], wild]))
        moves['greens'] = list(set([dice['w1'] + dice['green'], dice['w2'] + dice['green'], wild]))

        return moves

class Color:

    def __init__(self, color) -> None:

        self.color = color
        
        if (color == 'red') or (color == 'yellow'):
            self.values = np.arange(2,13,1) # ascending 2 to 12
        else:
            self.values = np.arange(12,1,-1) # descending 12 to 2
        
        self.values = np.append(self.values, 0)  # use 0 for the "key" cell
        self.status = np.array([False] * len(self.values), dtype=bool)

        self.update_max_checked_index()
        self.get_color_score()

    def update_max_checked_index(self):

        if np.sum(self.status) > 0:
            i_max = np.argmax(self.status)
        else:
            i_max = -1

        self.i_max = i_max
        
        return
    
    def get_color_score(self):

        scores = {0:0, 1:1, 2:3, 3:6, 4:10, 5:15, 6:21, 7:28, 8:36, 9:45, 10:55, 11:66, 12:72}

        self.score = scores[np.sum(self.status)]

        return
    
    def check_cell(self, value):
        
        move_index = np.argwhere(self.values == value)[0][0]
        self.status[move_index] = True
        self.get_color_score()
    
    def __str__(self) -> str:

        values = ''
        for i, v in enumerate(self.values):
            if self.status[i]:
                s = 'x'
            else:
                s = ' '
            val_status = f'{v}{s}'
            values = values + f' {val_status:<3}'
        line1 = f'{self.color:<8}|{values} | {self.score:<3}\n'

        return line1

class Board:

    def __init__(self) -> None:

        self.colors = ['reds', 'yellows', 'greens', 'blues']
        for color in self.colors:  # initialize the colors
            self.__setattr__(color, Color(color[:-1]))
        
        self.xs = 0  # initialize the x's
        self.get_board_score()

    def get_valid_moves(self, moves, wild_only=False):

        valid_moves = []
        for color in self.colors:
            for value in moves[color]:
                move_index = np.argwhere(self.__getattribute__(color).values == value)
                if move_index > self.__getattribute__(color).i_max:
                    valid_moves.append([color, value])

        return valid_moves
    
    def get_board_score(self):

        score = 0
        for color in self.colors:
            score += self.__getattribute__(color).score
        score += (self.xs * -5)

        self.score = score

        return
    
    def check_cell(self, color, value):

        print(f'Marking {color} {value}')

        self.__getattribute__(f'{color}s').check_cell(value)
        self.get_board_score()

        return
    
    def __str__(self):

        lines = ''
        for color in self.colors:
            color_lines = str(self.__getattribute__(color))
            lines += color_lines
        x_line = f"x's: {self.xs}"
        lines += f'{x_line:>57} | {self.xs * -5:<3}\n'
        lines += f"{'Score':>57} | {self.score}"

        return lines

board = Board()



# def roll_dice():

#     dice = {'w1' : None, 'w2': None, 'red' : None, 'yellow': None, 'green': None, 'blue': None}
#     np.random.seed(32)

#     values = np.random.randint(low=1, high=6, size=len(dice))
#     for i, die in enumerate(dice.items()):
#         dice[die[0]] = values[i]

#     return dice

game = Game()

p1_board = game.boards[0]

print(p1_board)

p1_board.check_cell('red', 5)
p1_board.check_cell('red', 6)
p1_board.check_cell('red', 11)
p1_board.check_cell('red', 12)
p1_board.check_cell('red', 0)
print(p1_board)

moves = game.roll_dice()
p1_board.get_valid_moves(moves)
    