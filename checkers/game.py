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

    def main_screen(self):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.button(100, (200, 150), (800, 150), (200, 50), "Interactive board for checkers", (325, 130))  # Title
        self.button(50, (350, 350), (650, 350), (350, 300), "New game", (445, 330))  # New game
        self.button(50, (350, 475), (650, 475), (350, 425), "Load game (Inactive)", (435, 455))  # Load game
        self.button(50, (350, 600), (650, 600), (350, 550), "Information (Inactive)", (435, 580))  # Information
        self.button(50, (350, 725), (650, 725), (350, 675), "Quit", (470, 705))  # Quit
        pygame.display.update()

    def choose_mode(self):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.button(100, (200, 150), (800, 150), (200, 50), "New game", (445, 130))  # Title
        self.button(50, (350, 350), (650, 350), (350, 300), "Player vs Player", (405, 330))  # New game
        self.button(50, (350, 475), (650, 475), (350, 425), "Player vs AI", (425, 455))  # Load game
        self.button(50, (350, 600), (650, 600), (350, 550), "Back", (470, 580))  # Information
        pygame.display.update()

    def button(self, radius, pos1, pos2, pos3, text, text_pos):
        pygame.draw.circle(self.win, BLACK, pos1, radius)
        pygame.draw.circle(self.win, BLACK, pos2, radius)
        pygame.draw.rect(self.win, BLACK, (pos3[0], pos3[1], pos2[0] - pos1[0], 2 * radius))
        self.draw_text(text, FONT, WHITE, text_pos[0], text_pos[1])

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
        self.draw_text("HOME", FONT, BLACK, 865, 350)
        self.draw_text("SAVE GAME", FONT, BLACK, 830, 500)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def save(self):
        with open("saved_game.txt", "w") as file:
            file.write(
                "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(self.board.board, self.board.white_left, self.board.black_left,
                                                    self.board.white_kings, self.board.black_kings, self.second_player,
                                                    self.turn))

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
