import math
import random
from connect4 import (
    ROW_COUNT,
    COLUMN_COUNT,
    get_next_open_row,
    is_valid_location,
    winning_move,
    drop_piece
)

AI_PIECE = "O"
PLAYER_PIECE = "X"
EMPTY = " "

WINDOW_LENGTH = 4


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score


def score_position(board, piece):
    score = 0

    center_col = COLUMN_COUNT // 2
    center_vals = [board[r][center_col] for r in range(ROW_COUNT)]
    score += center_vals.count(piece) * 6

    for r in range(ROW_COUNT):
        row = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row[c:c + 4]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col[r:r + 4]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]


def is_terminal(board):
    return (
        winning_move(board, PLAYER_PIECE) or
        winning_move(board, AI_PIECE) or
        len(get_valid_locations(board)) == 0
    )


def minimax(board, depth, alpha, beta, maximizing):
    valid_cols = get_valid_locations(board)
    terminal = is_terminal(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE):
                return (None, 99999999)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -99999999)
            else:
                return (None, 0)

        return (None, score_position(board, AI_PIECE))

    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_cols)

        for col in valid_cols:
            row = get_next_open_row(board, col)
            temp_board = [row.copy() for row in board]
            drop_piece(temp_board, row, col, AI_PIECE)

            _, new_score = minimax(temp_board, depth - 1, alpha, beta, False)

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_cols)

        for col in valid_cols:
            row = get_next_open_row(board, col)
            temp_board = [row.copy() for row in board]
            drop_piece(temp_board, row, col, PLAYER_PIECE)

            _, new_score = minimax(temp_board, depth - 1, alpha, beta, True)

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return best_col, value


def get_ai_move(board, depth=4):
    col, _ = minimax(board, depth, -math.inf, math.inf, True)
    return col
