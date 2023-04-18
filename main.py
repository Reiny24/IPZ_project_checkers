from checkers.constants import *
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
button = pygame.Rect(RESTART[1], RESTART[2], 100, 100)


def get_row_col_from_mouse(pos, home, choose_mode):
    x, y = pos
    if x < 801 and not home and not choose_mode:
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col
    else:
        return x, y


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    home = True
    choose_mode = False

    while run:
        clock.tick(FPS)
        if game.turn == BLACK and not game.second_player:
            value, new_board = minimax(game.get_board(), DIFFICULTY, BLACK, game)
            game.ai_move(new_board)

        if game.winner() is not None and not home:
            game.board.draw_winner(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos, home, choose_mode)
                if not home and not choose_mode:
                    if row < 9:
                        game.select(row, col)
                    # elif AI[1] <= row <= AI[1] + 100 and AI[2] <= col <= AI[2] + 100:
                    #     game.switch_player()
                    elif RESTART[1] <= row <= RESTART[1] + 100 and RESTART[2] <= col <= RESTART[2] + 100:
                        game.reset()
                    elif HOME[1] <= row <= HOME[1] + 100 and HOME[2] <= col <= HOME[2] + 100:
                        home = True
                    elif SAVE[1] <= row <= SAVE[1] + 100 and SAVE[2] <= col <= SAVE[2] + 100:
                        game.save()
                else:
                    if home:
                        if 300 <= row <= 700 and 300 <= col <= 400:  # New game
                            game.reset()
                            home = False
                            choose_mode = True
                        elif 300 <= row <= 700 and 675 <= col <= 775:  # Quit
                            run = False
                    elif choose_mode:  # New game
                        if 300 <= row <= 700 and 300 <= col <= 400:
                            game.two_players()
                            choose_mode = False
                        elif 300 <= row <= 700 and 425 <= col <= 525:
                            game.against_ai()
                            choose_mode = False
                        elif 300 <= row <= 700 and 550 <= col <= 650:
                            home = True
                            choose_mode = False

        pygame.display.update()
        if home:
            game.main_screen()
        elif choose_mode:
            game.choose_mode()
        else:
            game.update()

    pygame.quit()


main()
