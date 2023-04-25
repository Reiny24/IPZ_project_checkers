import pygame

pygame.init()

# Board properties
WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = 100
DIFFICULTY = 4

# Piece properties
PADDING = 20
OUTLINE = 5
RADIUS = SQUARE_SIZE // 2 - PADDING

# RGB colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (222, 200, 170)
BLACK = (0, 0, 0)
BROWN = (79, 42, 15)
BLUE = (0, 0, 255)
GRAY = (140, 140, 140)
GREEN = (0, 255, 0)

# Fonts
BUTT_FONT = pygame.font.SysFont("Arial", 45, bold=True)
FONT = pygame.font.SysFont("Arial", 30, bold=True)
BIG_FONT = pygame.font.SysFont("Arial", 55, bold=True)

# Images
CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (44, 25))
RESTART = (pygame.transform.scale(pygame.image.load("assets/restart.png"), (100, 100)), 850, 100)
HOME = (pygame.transform.scale(pygame.image.load("assets/home.png"), (100, 100)), 850, 250)
AI = (pygame.transform.scale(pygame.image.load("assets/AI.png"), (100, 100)), 850, 400)
PLAYER = (pygame.transform.scale(pygame.image.load("assets/second_player.png"), (100, 100)), 850, 400)
BACKGROUND = pygame.transform.scale(pygame.image.load("assets/background.png"), (200, 800))
HOME_BACKGROUND = (pygame.transform.scale(pygame.image.load("assets/home_background.png"), (1000, 800)), 0, 0)
SAVE = (pygame.transform.scale(pygame.image.load("assets/save.png"), (100, 100)), 850, 400)
RIGHT = pygame.transform.scale(pygame.image.load("assets/arrow.png"), (100, 100))
LEFT = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/arrow.png"), (100, 100)), 180)

# Sounds
PIECE_MOVE = pygame.mixer.Sound("assets/sounds/piece_move.mp3")
BUTT_PRESS = pygame.mixer.Sound("assets/sounds/button_press.mp3")
CONGRATS = pygame.mixer.Sound("assets/sounds/Congratulations.mp3")
