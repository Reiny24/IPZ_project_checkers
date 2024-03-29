import pygame.display

from checkers.constants import *


class GUI:
    def __init__(self, win):
        self.win = win
        self.delay = 0
        self.page = 0
        self.saved = False

    def __button(self, radius, pos1, pos2, pos3, text, text_pos, font, color):
        pygame.draw.circle(self.win, color, pos1, radius)
        pygame.draw.circle(self.win, color, pos2, radius)
        pygame.draw.rect(self.win, color, (pos3[0], pos3[1], pos2[0] - pos1[0], 2 * radius))
        if text is not None:
            self.__draw_text(text, font, WHITE, text_pos[0], text_pos[1])

    def __draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.win.blit(img, (x, y))

    def __draw_valid_moves(self, moves, selected, board_list, x, y):
        if selected is not None:
            piece = None
            for move in moves:
                row, col = move
                pygame.draw.circle(self.win, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
                piece = board_list[x][y]
            if piece is not None:
                self.draw_piece(self.win, selected, piece.x, piece.y, piece.color, piece.king)

    @staticmethod
    def __draw_squares(win):
        """Marks the playing field into squares"""
        win.fill(BROWN)
        win.blit(BACKGROUND, (800, 0))
        win.blit(RESTART[0], (RESTART[1], RESTART[2]))
        win.blit(HOME[0], (HOME[1], HOME[2]))
        win.blit(SAVE[0], (SAVE[1], SAVE[2]))

        pygame.draw.rect(win, GRAY, (800, 600, 200, 200))
        pygame.draw.circle(win, WHITE, (875, 675), 25)
        pygame.draw.circle(win, BLACK, (875, 750), 25)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def main_screen(self, home, choose_mode):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.__button(105, (200, 150), (800, 150), (200, 45), None, None, None, WHITE)  # Frames for buttons
        self.__button(55, (350, 350), (650, 350), (350, 295), None, None, None, WHITE)
        self.__button(55, (350, 475), (650, 475), (350, 420), None, None, None, WHITE)
        self.__button(55, (350, 600), (650, 600), (350, 545), None, None, None, WHITE)
        if home:
            self.__button(55, (350, 725), (650, 725), (350, 670), None, None, None, WHITE)
            self.__button(100, (200, 150), (800, 150), (200, 50), "Interactive board for checkers", (185, 120),
                          BIG_FONT, BLACK)  # Title
            self.__button(50, (350, 350), (650, 350), (350, 300), "New game", (410, 320), BUTT_FONT,
                          BLACK)  # New game
            self.__button(50, (350, 475), (650, 475), (350, 425), "Load game", (405, 445), BUTT_FONT,
                          BLACK)  # Load game
            self.__button(50, (350, 600), (650, 600), (350, 550), "Information", (400, 570), BUTT_FONT,
                          BLACK)  # Info
            self.__button(50, (350, 725), (650, 725), (350, 675), "Quit", (455, 700), BUTT_FONT, BLACK)  # Quit
        elif choose_mode:
            self.__button(100, (200, 150), (800, 150), (200, 50), "New game", (400, 120), BIG_FONT, BLACK)  # Title
            self.__button(50, (350, 350), (650, 350), (350, 300), "Player vs Player", (360, 320), BUTT_FONT,
                          BLACK)  # Player vs Player
            self.__button(50, (350, 475), (650, 475), (350, 425), "Player vs AI", (395, 445), BUTT_FONT,
                          BLACK)  # Player vs AI
            self.__button(50, (350, 600), (650, 600), (350, 550), "Back", (455, 570), BUTT_FONT, BLACK)  # Back
        else:
            self.__button(100, (200, 150), (800, 150), (200, 50), "Interactive board for checkers", (185, 120),
                          BIG_FONT, BLACK)  # Title
            pygame.draw.rect(self.win, WHITE, (245, 295, 510, 235))
            pygame.draw.rect(self.win, BLACK, (250, 300, 500, 225))
            self.__draw_text("Курсова робота з курсу", FONT, WHITE, 345, 310)
            self.__draw_text("\"Інженерія програмного забезпечення\"", FONT, WHITE, 260, 355)
            self.__draw_text("виконали студенти групи ІО-11", FONT, WHITE, 300, 395)
            self.__draw_text("Гук Дмитро Сергійович та", FONT, WHITE, 330, 435)
            self.__draw_text("Домашенко Іван Сергійович", FONT, WHITE, 320, 475)
            self.__button(50, (350, 600), (650, 600), (350, 550), "Back", (455, 570), BUTT_FONT, BLACK)  # Back
        pygame.display.update()

    def choose_save(self, saves, matrix, left, right, x, y):
        self.win.blit(HOME_BACKGROUND[0], (HOME_BACKGROUND[1], HOME_BACKGROUND[2]))  # Background
        self.__button(105, (200, 150), (800, 150), (200, 45), None, None, None, WHITE)
        self.__button(100, (200, 150), (800, 150), (200, 50), "Choose your save", (300, 120), BIG_FONT,
                      BLACK)  # Title
        pygame.draw.rect(self.win, WHITE, (145, 270, 710, 260))
        pygame.draw.rect(self.win, BLACK, (150, 275, 700, 250))

        if right and self.page < len(saves) - 1:
            self.page += 1
        elif left and self.page > 0:
            self.page -= 1

        if self.page < len(saves) - 1:
            pygame.draw.circle(self.win, WHITE, (900, 400), 49)
            self.win.blit(RIGHT, (850, 350))
        if self.page > 0:
            pygame.draw.circle(self.win, WHITE, (100, 400), 49)
            self.win.blit(LEFT, (50, 350))

        row, col = 170, 295
        for i in saves[self.page]:
            self.__draw_text(i, FONT, WHITE, row, col)
            col += 60
            if col == 535:
                row += 140
                col = 295

        if x is not None and x <= len(matrix) - 1 and y <= len(matrix[x]) - 1:
            pygame.draw.rect(self.win, WHITE, (150 + x * 140, 275 + y * 62, 140, 10))
            pygame.draw.rect(self.win, WHITE, (150 + x * 140, 329 + y * 62, 140, 10))
            pygame.draw.rect(self.win, WHITE, (150 + x * 140, 275 + y * 62, 10, 54))
            pygame.draw.rect(self.win, WHITE, (280 + x * 140, 275 + y * 62, 10, 54))
            self.__button(55, (350, 600), (650, 600), (340, 545), None, None, None, WHITE)
            self.__button(50, (350, 600), (650, 600), (350, 550), "Load selected", (375, 570), BUTT_FONT, BLACK)

        self.__button(55, (350, 725), (650, 725), (340, 670), None, None, None, WHITE)
        self.__button(50, (350, 725), (650, 725), (350, 675), "Back", (450, 695), BUTT_FONT, BLACK)  # Back

        pygame.display.update()

    def draw(self, win, board):
        """Draws the board"""
        self.__draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != 0:
                    self.draw_piece(win, False, piece.x, piece.y, piece.color, piece.king)

    def update(self, draw, board, valid_moves, turn, selected, end, row, col, saved, filename):
        self.draw(self.win, draw)
        if selected is not None and valid_moves:
            self.__draw_valid_moves(valid_moves, selected, draw, row, col)
        if end:
            if turn == BLACK:
                self.__draw_text("WHITE WON!", FONT, WHITE, 820, 600)
            else:
                self.__draw_text("BLACK WON!", FONT, BLACK, 820, 600)
        else:
            if turn == WHITE:
                self.__draw_text("WHITE TURN", FONT, WHITE, 820, 600)
            else:
                self.__draw_text("BLACK TURN", FONT, BLACK, 820, 600)
        self.__draw_text(str(12 - board.white_left), FONT, WHITE, 925, 660)
        self.__draw_text(str(12 - board.black_left), FONT, BLACK, 925, 735)
        self.__draw_text("RESTART", FONT, BLACK, 845, 200)
        self.__draw_text("HOME", FONT, BLACK, 865, 350)
        if saved:
            self.saved = True
        if not self.saved:
            self.__draw_text("SAVE GAME", FONT, BLACK, 830, 500)
        else:
            self.__draw_text("SAVED AS", FONT, BLACK, 840, 500)
            self.__draw_text(str(filename), FONT, BLACK, 855, 540)
            self.delay += 1
            if self.delay == 300:
                self.delay = 0
                self.saved = False
        pygame.display.update()

    def get_page(self):
        return self.page

    @staticmethod
    def draw_piece(win, selected, x, y, color, king):
        if selected is not None and selected is not False:
            pygame.draw.circle(win, GREEN, (x, y), RADIUS + OUTLINE)
        else:
            pygame.draw.circle(win, GRAY, (x, y), RADIUS + OUTLINE)
        pygame.draw.circle(win, color, (x, y), RADIUS)
        if king:
            win.blit(CROWN, (x - CROWN.get_width() // 2, y - CROWN.get_height() // 2))
