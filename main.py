from checkers.constants import *
from checkers.game import Game
from interface.gui import GUI
from checkers.piece import Piece
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
button = pygame.Rect(RESTART[1], RESTART[2], 100, 100)


def get_row_col_from_mouse(pos, board):
    x, y = pos
    if x < 801 and board:
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col
    else:
        return x, y


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    gui = GUI(WIN)
    # Flags
    home, board, choose_mode, choose_save, info = True, False, False, False, False
    left, right = False, False
    x, y = None, None
    choose = False
    end = False
    select = False
    selected_row, selected_col = None, None
    saved = False

    while run:
        clock.tick(FPS)

        if not home and not choose_mode and not choose_save:  # Checks if game has ended
            arr = []
            for row in range(0, ROWS):
                for col in range(0, COLS):
                    if game.board.get_piece(row, col) != 0 and game.board.get_piece(row, col).color == game.turn:
                        arr.append(game.board.get_valid_moves(Piece(row, col, game.turn)))
            for i in arr:
                if i != {}:
                    end = False
                    break
                else:
                    end = True
            if game.board.white_left == 0 or game.board.black_left == 0:
                end = True

        if game.turn == BLACK and not game.second_player:
            value, new_board = minimax(game.get_board(), DIFFICULTY, BLACK, game)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos, board)

                if board:  # Game screen buttons
                    if row < 9:
                        game.select(row, col)
                        selected_row, selected_col = row, col
                        select = True
                    elif RESTART[1] <= row <= RESTART[1] + 100 and RESTART[2] <= col <= RESTART[2] + 100:
                        BUTT_PRESS.play()
                        game.reset()
                    elif HOME[1] <= row <= HOME[1] + 100 and HOME[2] <= col <= HOME[2] + 100:
                        BUTT_PRESS.play()
                        home, board = True, False
                        game.reset()
                    elif SAVE[1] <= row <= SAVE[1] + 100 and SAVE[2] <= col <= SAVE[2] + 100:
                        BUTT_PRESS.play()
                        game.save()
                        saved = True
                    else:
                        game.selected, game.valid_moves = None, None

                elif home:  # Home screen buttons
                    if 300 <= row <= 700 and 300 <= col <= 400:  # New game
                        game.reset()
                        home, choose_mode = False, True
                        BUTT_PRESS.play()
                    elif 300 <= row <= 700 and 425 <= col <= 525:  # Load game
                        home, choose_save = False, True
                        BUTT_PRESS.play()
                    elif 300 <= row <= 700 and 550 <= col <= 650:
                        home, info = False, True
                        BUTT_PRESS.play()
                    elif 300 <= row <= 700 and 675 <= col <= 775:  # Quit
                        BUTT_PRESS.play()
                        run = False

                elif choose_mode:  # New game buttons
                    if 300 <= row <= 700 and 300 <= col <= 400:  # Player vs Player
                        game.two_players()
                        choose_mode, board = False, True
                        BUTT_PRESS.play()
                    elif 300 <= row <= 700 and 425 <= col <= 525:  # Player vs AI
                        game.against_ai()
                        choose_mode, board = False, True
                        BUTT_PRESS.play()
                    elif 300 <= row <= 700 and 550 <= col <= 650:  # Back
                        home, choose_mode = True, False
                        BUTT_PRESS.play()

                elif choose_save:  # Choose save buttons
                    if 300 <= row <= 700 and 675 <= col <= 775:  # Back
                        home, choose_save = True, False
                        x, y = None, None
                        BUTT_PRESS.play()
                    elif 850 <= row <= 950 and 350 <= col <= 450:  # Right arrow
                        right, left = True, False
                        x, y = None, None
                        BUTT_PRESS.play()
                    elif 50 <= row <= 150 and 350 <= col <= 450:  # Left arrow
                        right, left = False, True
                        x, y = None, None
                        BUTT_PRESS.play()
                    elif 150 <= row < 850 and 275 <= col < 525:  # Save select
                        x, y = (row - 150) // 140, (col - 275) // 62
                    elif 350 <= row <= 650 and 550 <= col <= 650 and x is not None:  # Start game
                        choose, board, choose_save = True, True, True
                        BUTT_PRESS.play()

                elif info:  # Info buttons
                    if 300 <= row <= 700 and 550 <= col <= 650:  # Back
                        home, info = True, False
                        BUTT_PRESS.play()

        if home or choose_mode or info:  # Main screen and mode select screen
            gui.main_screen(home, choose_mode)
        elif choose_save:  # Choose save screen
            gui.choose_save(game.get_saves(), game.get_saved_matrix(gui.get_page()), left, right, x, y)
            left, right = False, False
            if choose:
                game.load_game(gui.get_page(), x, y)
                choose_save, choose = False, False
                x = None
        else:  # Board screen
            if select:
                gui.update(game.get_board_to_draw(), game.get_board(), game.get_valid_moves(), game.get_turn(), game.get_selected(), end,
                           selected_row, selected_col, saved, game.get_filename())
            else:
                gui.update(game.get_board_to_draw(), game.get_board(), game.get_valid_moves(), game.get_turn(), game.get_selected(), end, None,
                           None, saved, game.get_filename())
            saved = False

    pygame.quit()


main()
