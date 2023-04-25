from .constants import *
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0
        self.temp = None
        self.triple_jump = None
        self.counter = 0
        self.create_board()

    def evaluate(self):
        """Returns possible position for AI"""
        return self.black_left - self.white_left + (self.black_kings * 0.5 - self.white_kings * 0.5)

    def get_all_pieces(self, color):
        """Returns list of all pieces"""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col, sound):
        """Moves the piece"""
        if type(piece) != int:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][
                piece.col]
            piece.move(row, col)

            if row == ROWS - 1 or row == 0:
                piece.make_king()
                if piece.color == BLACK:
                    self.black_kings += 1
                else:
                    self.white_kings += 1

            if sound:
                PIECE_MOVE.play()

    def get_piece(self, row, col):
        """Returns piece in given position"""
        return self.board[row][col]

    def create_board(self):
        """Creates the board"""
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def remove(self, pieces):
        """Removes pieces"""
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        """Returns winner of the game"""
        if self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE
        return None


    def get_valid_moves(self, piece):
        """Returns available moves for selected chess"""
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, left, False))
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, right, True))
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse(row + 1, min(row + 3, ROWS), 1, piece.color, left, False))
            moves.update(self._traverse(row + 1, min(row + 3, ROWS), 1, piece.color, right, True))
        self.counter = 0

        return moves

    def _traverse(self, start, stop, step, color, pos, side, skipped=None):
        """Checks valid moves on the diagonals, side = False -> Left, side = True -> Right"""
        if skipped is None:
            skipped = []
        moves = {}
        last = []
        for r in range(start, stop, step):
            if not side and pos < 0 or side and pos >= COLS:
                break

            current = self.board[r][pos]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, pos)] = last + skipped
                else:
                    moves[(r, pos)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    if color == WHITE and start == 3:
                        self.counter += 1
                        self.temp = moves
                        if self.triple_jump is None:
                            self.triple_jump = last
                        if not side:
                            moves.update(
                                self._traverse(r + step, row - 2, step, color, pos + 1, True, skipped=last))
                            moves.update(
                                self._traverse(r + step, row - 2, step, color, pos - 1, False, skipped=last))
                        else:
                            moves.update(
                                self._traverse(r + step, row - 2, step, color, pos - 1, False, skipped=last))
                            moves.update(
                                self._traverse(r + step, row - 2, step, color, pos + 1, True, skipped=last))
                    else:
                        self.counter += 1
                        self.temp = moves
                        if self.triple_jump is None:
                            self.triple_jump = last
                        if not side:
                            moves.update(self._traverse(r + step, row, step, color, pos + 1, True, skipped=last))
                            moves.update(self._traverse(r + step, row, step, color, pos - 1, False, skipped=last))
                        else:
                            moves.update(
                                self._traverse(r + step, row, step, color, pos - 1, False, skipped=last))
                            moves.update(
                                self._traverse(r + step, row, step, color, pos + 1, True, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            if not side:
                pos -= 1
            else:
                pos += 1

        if self.temp == moves and self.counter == 3:
            moves[(stop - 1, pos)] = last + skipped + self.triple_jump
            self.counter = 0

        return moves

    def get_board(self):
        return self.board
