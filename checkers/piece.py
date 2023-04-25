from .constants import *
import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def is_king(self):
        return self.king

    def draw(self, win, selected):
        if selected:
            pygame.draw.circle(win, GREEN, (self.x, self.y), RADIUS + OUTLINE)
        else:
            pygame.draw.circle(win, GRAY, (self.x, self.y), RADIUS + OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), RADIUS)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
