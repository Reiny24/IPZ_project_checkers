import os

import numpy

from checkers.board import Board
from .constants import *


class Game:
    def __init__(self):
        self.board = None
        self.selected = None
        self.second_player = True
        self.turn = None
        self.valid_moves = None
        self.__init()
        self.filename = None

    def __init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def __move(self, row, col, sound):
        """Moves pieces on the game board"""
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col, sound)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.__change_turn()
            self.selected = None
        else:
            return False

        return True

    def __change_turn(self):
        """Change turn of the game"""
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def reset(self):
        """Restarts the game"""
        self.__init()

    def save(self):
        """Saves current game"""
        self.filename = "Save_" + str(len(os.listdir(r".\Saved_games")))
        os.mkdir(fr".\saved_games\{self.filename}")
        numpy.save(fr".\saved_games\{self.filename}\{self.filename}.npy", self.board.board, allow_pickle=True)
        with open(fr".\saved_games\{self.filename}\{self.filename}", "w") as file:
            file.write(
                "{}\n{}\n{}\n{}\n{}\n{}".format(self.board.white_left, self.board.black_left,
                                                self.board.white_kings, self.board.black_kings, self.second_player,
                                                self.turn[0]))

    def load_game(self, page, x, y):
        """Load selected game"""
        saved_game = self.get_saved_matrix(page)[x][y]
        print(saved_game)
        if len(os.listdir(r".\saved_games")) > 0:

            with open(fr".\saved_games\{saved_game}\{saved_game}", "r") as file:
                data = file.read().split("\n")

            self.board.board = numpy.load(fr".\saved_games\{saved_game}\{saved_game}.npy", allow_pickle=True)
            self.board.white_left = int(data[0])
            self.board.black_left = int(data[1])
            self.board.white_kings = int(data[2])
            self.board.black_kings = int(data[3])
            self.second_player = data[4] in ["True"]
            if data[5] == "255":
                self.turn = WHITE
            else:
                self.turn = BLACK

    def select(self, row, col):
        """Calculates selected piece"""
        if self.selected:
            result = self.__move(row, col, True)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def winner(self):
        """Returns winner of the game"""
        if self.board is not None:
            return self.board.winner()

    def get_board(self):
        """Returns the game board"""
        return self.board

    def get_selected(self):
        """Returns selected piece"""
        return self.selected

    def get_turn(self):
        """Returns current turn"""
        return self.turn

    def get_valid_moves(self):
        """Returns valid moves of the game"""
        return self.valid_moves

    def get_filename(self):
        """Returns filename to save/load"""
        return self.filename

    def get_board_to_draw(self):
        """Returns the board for GUI"""
        return self.board.get_board()

    def ai_move(self, board):
        """Makes a move if selected mode with AI"""
        PIECE_MOVE.play()
        self.board = board
        self.__change_turn()

    def two_players(self):
        """Sets game mode to 'Two players'"""
        self.second_player = True

    def against_ai(self):
        """Sets game mode to 'Against AI'"""
        self.second_player = False

    def get_saved_matrix(self, page):
        """Returns available saves on the page"""
        row, col, save_arr = 0, 0, [[]]
        for i in self.get_saves()[page]:
            save_arr[row].append(i)
            col += 1
            if col == 4:
                save_arr.append([])
                row += 1
                col = 0
        return save_arr

    @staticmethod
    def get_saves():
        """Returns all available saves"""
        length, pos, arr = 0, 0, [[]]
        for i in os.listdir(r"./Saved_games"):
            if length <= 20:
                arr[pos].append(i)
                length += 1
            if length == 20:
                arr.append([])
                length = 0
                pos += 1
        return arr
