import numpy as np
import secrets

from players import *

class Game:

    def __init__(self, players=4, seed=None) -> None:
        
        self.colors = ['reds', 'yellows', 'greens', 'blues']
        self.colors_ended = {}
        for color in self.colors:
            self.colors_ended[color] = False

        # seed random numbers
        if seed == None:
            self.dice_seed = secrets.randbits(128)  
        else:
            self.dice_seed = seed
        self.dice_rng = np.random.default_rng(self.dice_seed)
        print(f'started game with seed {self.dice_seed}') 

        self.players = players
        self.boards = []
        for i, player in enumerate(range(self.players)):
            if i == 0:
                self.boards.append(Board(colors=self.colors, player=userPlayer(f'User - P{i+1}')))
            else:
                self.boards.append(Board(colors=self.colors, player=randomPlayer(f'Random - P{i+1}')))
        print(f'initialized game with {self.players} boards')
        
        # set first turn to first player (0 index)
        self.turn = 0  

        # set graphics

        # initialize some null moves
        null_nothing = [['null', 'do', 'nothing']]
        null_x = [['null', 'take', 'x']]

        # start while loop
        self.game_end = False
        while self.game_end == False:
            # active player rolls the dice
            for roll_board in self.boards:
                # print(chr(27) + "[2J")  # Clear Terminal
                self.roll_dice()
                self.compute_moves()

                for play_board in self.boards:
                    print("-"*80)
                    print(play_board)
                    print(f'rolled dice: {self.dice}')
                    wild_moves, color_moves = play_board.get_valid_moves(moves=self.moves)

                    if play_board == roll_board:  # rolling dice player
                        
                        print(f'ACTIVE PLAYER:{play_board.player.name} -- (the one who rolled the dice)')
                        if len(wild_moves + color_moves) > 0:
                            selected_move = play_board.player.choose_move(game=self, valid_moves=wild_moves + color_moves + null_x)
                            if selected_move[0] == 'null': # rolling dice player can choose to take an x 
                                play_board.take_x()
                                print(play_board)
                            elif selected_move[0] == 'color':
                                play_board.check_cell(color = selected_move[1], value=int(selected_move[2]))
                                print(play_board)
                            elif selected_move[0] == 'wild':
                                play_board.check_cell(color = selected_move[1], value=int(selected_move[2]))
                                print(play_board)
                                print(f'rolled dice: {self.dice}')
                                wild_moves, color_moves = play_board.get_valid_moves(moves=self.moves)  # update list of valid moves
                                selected_move = play_board.player.choose_move(game=self, valid_moves=color_moves + null_nothing)
                                if selected_move[0] == 'color':
                                    play_board.check_cell(color = selected_move[1], value=int(selected_move[2]))
                                    print(play_board)
                        else:  # rolling dice player has to take an x if no moves available
                            play_board.take_x()

                    else:  # non dice-rolling player
                        print(f'PASSIVE PLAYER: {play_board.player.name} -- (the one who did NOT roll the dice)')
                        selected_move = play_board.player.choose_move(game=self, valid_moves=wild_moves + null_nothing)
                        if selected_move[0] != 'null':
                            play_board.check_cell(color = selected_move[1], value=int(selected_move[2]))
                            print(play_board)
                        
                    self.check_game_end()
                    self.turn += 1

        print(f'=============================== Final Boards ========================')
        for board in self.boards:
            print(board)
            print('---------------------------------------------------------------------')

        return
    
    def __str__(self):

        lines = ''
        for i, player in enumerate(range(self.players)):
            lines += f"Player {i + 1}'s board:\n"
            lines += print(self.boards[i])
            lines += '\n'

        return
    
    def next_turn(self):

        self.turn = (self.turn + 1) % (self.players - 1)

    def check_game_end(self):

        game_end = False

        for i, board in enumerate(self.boards):
            if board.xs >= 4:
                self.game_end = True
                print(f"Game ended because Player {i+1} racked up 4 x's")
            for color in self.colors:
                if board.__getattribute__(color).status[-1]:  # check to see if last index is checked
                    self.colors_ended[color] = True

        if sum(self.colors_ended.values()) >= 2:
            self.game_end = True
            print(f'Game ended because 2 or more colors are completed:\n{self.colors_ended}')
            

        return game_end
    
    def roll_dice(self):

        dice = {'w1' : None, 'w2': None, 'red' : None, 'yellow': None, 'green': None, 'blue': None}
        values = self.dice_rng.integers(low=1, high=6, size=len(dice))
        for i, die in enumerate(dice.items()):
            dice[die[0]] = values[i]

        self.dice = dice

    def compute_moves(self):

        moves = {}
        d = self.dice
        wild = d['w1'] + d['w2']
        moves['wild'] = [wild]
        moves['reds'] = list(set([d['w1'] + d['red'], d['w2'] + d['red']]))
        moves['yellows'] = list(set([d['w1'] + d['yellow'], d['w2'] + d['yellow']]))
        moves['blues'] = list(set([d['w1'] + d['blue'], d['w2'] + d['blue']]))
        moves['greens'] = list(set([d['w1'] + d['green'], d['w2'] + d['green']]))

        self.moves = moves

        return moves

class Board:

    def __init__(self, colors, player) -> None:

        self.colors = colors
        for color in self.colors:  # initialize the colors
            self.__setattr__(color, Color(color[:-1]))
        
        self.xs = 0  # initialize the x's
        self.get_board_score()
        self.player = player

    def select_move(self):

        self.player.select_move()

        return

    def get_valid_moves(self, moves):

        wild_moves = []
        color_moves = []

        for color in self.colors:
            if np.sum(self.__getattribute__(color).status) >= 5:
                max_index = 10 # can go up to the 2 / 12
            else:
                max_index = 9  # can only go up to the 3 / 11

            for value in moves['wild']:
                move_index = np.argwhere(self.__getattribute__(color).values == value)[0][0]
                if (move_index > self.__getattribute__(color).max_checked) & (move_index <= max_index):
                    wild_moves.append(['wild', color, value])

            for value in moves[color]:
                move_index = np.argwhere(self.__getattribute__(color).values == value)[0][0]
                if (move_index > self.__getattribute__(color).max_checked) & (move_index <= max_index):
                    color_moves.append(['color', color, value])

        return wild_moves, color_moves

    
    def get_board_score(self):

        score = 0
        for color in self.colors:
            score += self.__getattribute__(color).score
        score += (self.xs * -5)

        self.score = score

        return
    
    def check_cell(self, color, value):

        print(f'Marking {color} {value}')

        self.__getattribute__(f'{color}').check_cell(value)
        self.get_board_score()

        return
    
    
    def take_x(self):

        print(f'Taking an x...')
        self.xs += 1
        self.get_board_score()

        return
    
    def __str__(self):

        lines = f'Board: {self.player.name}\n'
        for color in self.colors:
            color_lines = str(self.__getattribute__(color))
            lines += color_lines
        x_line = f"x's: {self.xs}"
        lines += f'{x_line:>57} | {self.xs * -5:<3}\n'
        lines += f"{'Score':>57} | {self.score}"

        return lines

class Color:

    def __init__(self, color) -> None:

        self.color = color
        
        if (color == 'red') or (color == 'yellow'):
            self.values = np.arange(2,13,1) # ascending 2 to 12
        else:
            self.values = np.arange(12,1,-1) # descending 12 to 2
        
        self.values = np.append(self.values, 0)  # use 0 for the "key" cell
        self.status = np.array([False] * len(self.values), dtype=bool)
        self.completed = False

        self.update_imax()
        self.get_color_score()

    def update_imax(self):

        if np.sum(self.status) > 0:
            max_checked = np.max(np.argwhere(self.status == True))
        else:
            max_checked = -1

        self.max_checked = max_checked
        
        return
    
    def get_color_score(self):

        scores = {0:0, 1:1, 2:3, 3:6, 4:10, 5:15, 6:21, 7:28, 8:36, 9:45, 10:55, 11:66, 12:72}

        self.score = scores[np.sum(self.status)]

        return
    
    def check_cell(self, value):
        
        move_index = np.argwhere(self.values == value)[0][0]
        self.status[move_index] = True
        if move_index == 10:
            self.status[11] = True
            self.completed = True
        self.update_imax()
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

if __name__ == "__main__":
    game=Game(seed=42)
