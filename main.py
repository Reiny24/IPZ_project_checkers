from checkers.constants import *
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
button = pygame.Rect(RESTART[1], RESTART[2], 100, 100)


def get_row_col_from_mouse(pos):
    x, y = pos
    if x < 801:
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col
    else:
        return x, y


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.turn == BLACK and not game.second_player:
            value, new_board = minimax(game.get_board(), DIFFICULTY, BLACK, game)
            game.ai_move(new_board)

        # if game.winner() is not None:
        #     game.board.draw_winner(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if row < 9:
                    game.select(row, col)
                elif AI[1] <= row <= AI[1] + 100 and AI[2] <= col <= AI[2] + 100:
                    game.switch_player()
                elif RESTART[1] <= row <= RESTART[1] + 100 and RESTART[2] <= col <= RESTART[2] + 100:
                    game.reset()

            # a, b = pygame.mouse.get_pos()
            # print(a, b)
            # if RESTART[1] <= a <= RESTART[1] + 100 and RESTART[2] <= b <= RESTART[2] + 100:
            #     game.board.update_button(WIN)
            #     pygame.display.update()

        game.update()

    pygame.quit()


main()
