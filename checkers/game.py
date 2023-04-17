import pygame.display
from .constants import *
from checkers.board import Board


class Game:
    def __init__(self, win):
        self.board = None
        self.selected = None
        self.second_player = True
        self.turn = None
        self.valid_moves = None
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win, self.second_player)
        self.draw_valid_moves(self.valid_moves)
        if self.turn == WHITE:
            self.draw_text("WHITE TURN", FONT, WHITE, 820, 600)
        else:
            self.draw_text("BLACK TURN", FONT, BLACK, 820, 600)
        self.draw_text(str(12 - self.board.white_left), FONT, WHITE, 925, 660)
        self.draw_text(str(12 - self.board.black_left), FONT, BLACK, 925, 735)
        self.draw_text("RESTART", FONT, BLACK, 845, 200)
        self.draw_text("INACTIVE!", FONT, BLACK, 840, 350)
        if self.second_player:
            self.draw_text("2 PLAYER", FONT, BLACK, 845, 500)
        else:
            self.draw_text("AI", FONT, BLACK, 890, 500)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.win.blit(img, (x, y))

    def winner(self):
        # pygame.draw.circle(self.win, BLUE, (0, 0), 100)
        # pygame.display.update()
        return self.board.winner()

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def switch_player(self):
        self.second_player = not self.second_player
