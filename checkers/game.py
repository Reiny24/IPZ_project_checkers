import numpy
import pygame.display
from .constants import *
from checkers.board import Board
import os


class Game:
    def __init__(self, win):
        self.board = None
        self.selected = None
        self.second_player = True
        self.turn = None
        self.valid_moves = None
        self._init()
        self.win = win
        self.saved = False
        self.filename = None
        self.delay = 0

    def main_screen(self):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.button(100, (200, 150), (800, 150), (200, 50), "Interactive board for checkers", (325, 130))  # Title
        self.button(50, (350, 350), (650, 350), (350, 300), "New game", (445, 330))  # New game
        self.button(50, (350, 475), (650, 475), (350, 425), "Load game", (435, 455))  # Load game
        self.button(50, (350, 600), (650, 600), (350, 550), "Information (Inactive)", (435, 580))  # Information
        self.button(50, (350, 725), (650, 725), (350, 675), "Quit", (470, 705))  # Quit
        pygame.display.update()

    def choose_mode(self):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.button(100, (200, 150), (800, 150), (200, 50), "New game", (445, 130))  # Title
        self.button(50, (350, 350), (650, 350), (350, 300), "Player vs Player", (405, 330))  # Player vs Player
        self.button(50, (350, 475), (650, 475), (350, 425), "Player vs AI", (425, 455))  # Player vs AI
        self.button(50, (350, 600), (650, 600), (350, 550), "Back", (470, 580))  # Back
        pygame.display.update()

    def choose_save(self):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        pygame.draw.rect(self.win, BLACK, (200, 200, 600, 330))
        row = 220
        col = 220
        for i in os.listdir(r"./saved_games"):
            self.draw_text(i, FONT, WHITE, row, col)
            col += 50
            if col == 520:
                row += 150
                col = 220
            if row == 820:
                pygame.draw.circle(self.win, WHITE, (900, 400), 49)
                self.win.blit(RIGHT, (850, 350))

        self.button(50, (350, 600), (650, 600), (350, 550), "Back", (470, 580))  # Back
        pygame.display.update()

    def button(self, radius, pos1, pos2, pos3, text, text_pos):
        pygame.draw.circle(self.win, BLACK, pos1, radius)
        pygame.draw.circle(self.win, BLACK, pos2, radius)
        pygame.draw.rect(self.win, BLACK, (pos3[0], pos3[1], pos2[0] - pos1[0], 2 * radius))
        self.draw_text(text, FONT, WHITE, text_pos[0], text_pos[1])

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        if self.turn == WHITE:
            self.draw_text("WHITE TURN", FONT, WHITE, 820, 600)
        else:
            self.draw_text("BLACK TURN", FONT, BLACK, 820, 600)
        self.draw_text(str(12 - self.board.white_left), FONT, WHITE, 925, 660)
        self.draw_text(str(12 - self.board.black_left), FONT, BLACK, 925, 735)
        self.draw_text("RESTART", FONT, BLACK, 845, 200)
        self.draw_text("HOME", FONT, BLACK, 865, 350)
        if not self.saved:
            self.draw_text("SAVE GAME", FONT, BLACK, 830, 500)
        else:
            self.draw_text("SAVED AS", FONT, BLACK, 840, 500)
            self.draw_text(str(self.filename), FONT, BLACK, 855, 540)
            self.delay += 1
            if self.delay == 300:
                self.saved = False
                self.delay = 0
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def save(self):
        import numpy
        self.filename = "Save_" + str(len(os.listdir(r".\saved_games")))
        os.mkdir(fr".\saved_games\{self.filename}")
        numpy.save(fr".\saved_games\{self.filename}\{self.filename}.npy", self.board.board, allow_pickle=True)
        with open(fr".\saved_games\{self.filename}\{self.filename}", "w") as file:
            file.write(
                "{}\n{}\n{}\n{}\n{}\n{}".format(self.board.white_left, self.board.black_left,
                                                self.board.white_kings, self.board.black_kings, self.second_player,
                                                self.turn[0]))
        self.saved = True

    def load_game(self):
        if len(os.listdir(r".\saved_games")) > 0:
            self.filename = "Save_" + str(len(os.listdir(r".\saved_games")) - 1)
            print(self.filename)
            with open(fr".\saved_games\{self.filename}\{self.filename}", "r") as file:
                data = file.read().split("\n")

            self.board.board = numpy.load(fr".\saved_games\{self.filename}\{self.filename}.npy", allow_pickle=True)
            self.board.white_left = int(data[0])
            self.board.black_left = int(data[1])
            self.board.white_kings = int(data[2])
            self.board.black_kings = int(data[3])
            self.second_player = data[4] in ["True"]
            print(self.second_player)
            if data[5] == "255":
                self.turn = WHITE
            else:
                self.turn = BLACK

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

    def two_players(self):
        self.second_player = True

    def against_ai(self):
        self.second_player = False
