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
        self.page = 0

    def main_screen(self, home, choose_mode):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.button_frame(105, (200, 150), (800, 150), (200, 45))  # Frames for buttons
        self.button_frame(55, (350, 350), (650, 350), (350, 295))
        self.button_frame(55, (350, 475), (650, 475), (350, 420))
        self.button_frame(55, (350, 600), (650, 600), (350, 545))
        if home:
            self.button_frame(55, (350, 725), (650, 725), (350, 670))
            self.button(100, (200, 150), (800, 150), (200, 50), "Interactive board for checkers", (185, 120),
                        BIG_FONT)  # Title
            self.button(50, (350, 350), (650, 350), (350, 300), "New game", (410, 320), BUTT_FONT)  # New game
            self.button(50, (350, 475), (650, 475), (350, 425), "Load game", (405, 445), BUTT_FONT)  # Load game
            self.button(50, (350, 600), (650, 600), (350, 550), "Information", (400, 570), BUTT_FONT)  # Info
            self.button(50, (350, 725), (650, 725), (350, 675), "Quit", (455, 700), BUTT_FONT)  # Quit
        elif choose_mode:
            self.button(100, (200, 150), (800, 150), (200, 50), "New game", (400, 120), BIG_FONT)  # Title
            self.button(50, (350, 350), (650, 350), (350, 300), "Player vs Player", (360, 320),
                        BUTT_FONT)  # Player vs Player
            self.button(50, (350, 475), (650, 475), (350, 425), "Player vs AI", (395, 445), BUTT_FONT)  # Player vs AI
            self.button(50, (350, 600), (650, 600), (350, 550), "Back", (455, 570), BUTT_FONT)  # Back
        else:
            self.button(100, (200, 150), (800, 150), (200, 50), "Interactive board for checkers", (185, 120),
                        BIG_FONT)  # Title
            pygame.draw.rect(self.win, WHITE, (245, 295, 510, 235))
            pygame.draw.rect(self.win, BLACK, (250, 300, 500, 225))
            self.draw_text("Курсова робота з курсу", FONT, WHITE, 345, 310)
            self.draw_text("\"Інженерія програмного забезпечення\"", FONT, WHITE, 260, 355)
            self.draw_text("виконали студенти групи ІО-11", FONT, WHITE, 300, 395)
            self.draw_text("Гук Дмитро Сергійович та", FONT, WHITE, 330, 435)
            self.draw_text("Домашенко Іван Сергійович", FONT, WHITE, 320, 475)
            self.button(50, (350, 600), (650, 600), (350, 550), "Back", (455, 570), BUTT_FONT)  # Back
        pygame.display.update()

    def choose_save(self, left, right, x, y, choose):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.button_frame(105, (200, 150), (800, 150), (200, 45))
        self.button(100, (200, 150), (800, 150), (200, 50), "Choose your save", (300, 120), BIG_FONT)  # Title
        pygame.draw.rect(self.win, WHITE, (145, 270, 710, 260))
        pygame.draw.rect(self.win, BLACK, (150, 275, 700, 250))
        length, pos, arr = 0, 0, [[]]
        for i in os.listdir(r"./Saved_games"):
            if length <= 20:
                arr[pos].append(i)
                length += 1
            if length == 20:
                arr.append([])
                length = 0
                pos += 1

        if right and self.page < len(arr) - 1:
            self.page += 1
        elif left and self.page > 0:
            self.page -= 1

        if self.page < len(arr) - 1:
            pygame.draw.circle(self.win, WHITE, (900, 400), 49)
            self.win.blit(RIGHT, (850, 350))
        if self.page > 0:
            pygame.draw.circle(self.win, WHITE, (100, 400), 49)
            self.win.blit(LEFT, (50, 350))

        row, col = 170, 295
        for i in arr[self.page]:
            self.draw_text(i, FONT, WHITE, row, col)
            col += 60
            if col == 535:
                row += 140
                col = 295

        row, col, save_arr = 0, 0, [[]]
        for i in arr[self.page]:
            save_arr[row].append(i)
            col += 1
            if col == 4:
                save_arr.append([])
                row += 1
                col = 0

        if x is not None and x <= len(save_arr) - 1 and y <= len(save_arr[x]) - 1:
            pygame.draw.rect(self.win, WHITE, (150 + x * 140, 275 + y * 62, 140, 10))
            pygame.draw.rect(self.win, WHITE, (150 + x * 140, 329 + y * 62, 140, 10))
            pygame.draw.rect(self.win, WHITE, (150 + x * 140, 275 + y * 62, 10, 54))
            pygame.draw.rect(self.win, WHITE, (280 + x * 140, 275 + y * 62, 10, 54))
            self.button_frame(55, (350, 600), (650, 600), (340, 545))
            self.button(50, (350, 600), (650, 600), (350, 550), "Load selected", (375, 570), BUTT_FONT)

        if choose:
            self.load_game(save_arr[x][y])
        self.button_frame(55, (350, 725), (650, 725), (340, 670))
        self.button(50, (350, 725), (650, 725), (350, 675), "Back", (450, 695), BUTT_FONT)  # Back
        pygame.display.update()

    def button(self, radius, pos1, pos2, pos3, text, text_pos, font):
        pygame.draw.circle(self.win, BLACK, pos1, radius)
        pygame.draw.circle(self.win, BLACK, pos2, radius)
        pygame.draw.rect(self.win, BLACK, (pos3[0], pos3[1], pos2[0] - pos1[0], 2 * radius))
        self.draw_text(text, font, WHITE, text_pos[0], text_pos[1])

    def button_frame(self, radius, pos1, pos2, pos3):
        pygame.draw.circle(self.win, WHITE, pos1, radius)
        pygame.draw.circle(self.win, WHITE, pos2, radius)
        pygame.draw.rect(self.win, WHITE, (pos3[0], pos3[1], pos2[0] - pos1[0], 2 * radius))

    def update(self, end):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        if end:
            if self.turn == BLACK:
                self.draw_text("WHITE WON!", FONT, WHITE, 820, 600)
            else:
                self.draw_text("BLACK WON!", FONT, BLACK, 820, 600)
        else:
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
        self.filename = "Save_" + str(len(os.listdir(r".\saved_games")))
        os.mkdir(fr".\saved_games\{self.filename}")
        numpy.save(fr".\saved_games\{self.filename}\{self.filename}.npy", self.board.board, allow_pickle=True)
        with open(fr".\saved_games\{self.filename}\{self.filename}", "w") as file:
            file.write(
                "{}\n{}\n{}\n{}\n{}\n{}".format(self.board.white_left, self.board.black_left,
                                                self.board.white_kings, self.board.black_kings, self.second_player,
                                                self.turn[0]))
        self.saved = True

    def load_game(self, saved_game):
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
        if self.selected:
            result = self._move(row, col, True)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, True)
            return True

        return False

    def _move(self, row, col, sound):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col, sound)
            print(row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        if self.selected is not None:
            for move in moves:
                row, col = move
                pygame.draw.circle(self.win, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.win.blit(img, (x, y))

    def winner(self):
        if self.board is not None:
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
        PIECE_MOVE.play()
        self.board = board
        self.change_turn()

    def two_players(self):
        self.second_player = True

    def against_ai(self):
        self.second_player = False
