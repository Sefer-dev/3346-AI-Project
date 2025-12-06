import random 
from connect4 import (
    ROW_COUNT,
    COLUMN_COUNT,
    is_valid_location,
    get_next_open_row,
    winning_move
)



# UTILITIES
def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def drop_temp(board, row, col, piece):
    """Return a NEW board with a move applied (used for simulation only)."""
    temp = [r[:] for r in board]
    temp[row][col] = piece
    return temp



# 1. RANDOM AI (baseline)
def ai_random_move(board):
    """Completely random valid column."""
    valid = get_valid_locations(board)
    return random.choice(valid)


# 2. HEURISTIC-BASED (NO MINIMAX)
def count_window(window, piece):
    """Score a group of 4 cells."""
    opp_piece = "O" if piece == "X" else "X"

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(" ") == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(" ") == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(" ") == 1:
        score -= 4

    return score


def score_position(board, piece):
    """Heuristic scoring function used by both greedy and minimax."""
    opp_piece = "O" if piece == "X" else "X"
    score = 0

    # Score center column
    center = COLUMN_COUNT // 2
    center_col = [board[r][center] for r in range(ROW_COUNT)]
    score += center_col.count(piece) * 3

    # Horizontal
    for r in range(ROW_COUNT):
        row_array = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += count_window(window, piece)

    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += count_window(window, piece)

    # Positive diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += count_window(window, piece)

    # Negative diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += count_window(window, piece)

    return score


def ai_greedy_move(board, ai_piece="O"):
    """
    GREEDY HEURISTIC AI:
    Looks at all possible moves and picks the one with the highest heuristic score.
    (No minimax, just one-step evaluation)
    """
    valid = get_valid_locations(board)
    best_score = -999999
    best_col = random.choice(valid)

    for col in valid:
        row = get_next_open_row(board, col)
        temp = drop_temp(board, row, col, ai_piece)
        score = score_position(temp, ai_piece)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col



# 3. MINIMAX (NO ALPHA-BETA)
def minimax(board, depth, maximizingPlayer, ai_piece):
    opp_piece = "O" if ai_piece == "X" else "X"
    valid = get_valid_locations(board)

    # Terminal checks
    if winning_move(board, ai_piece):
        return (None, 10_000_000)
    if winning_move(board, opp_piece):
        return (None, -10_000_000)
    if depth == 0 or len(valid) == 0:
        return (None, score_position(board, ai_piece))

    if maximizingPlayer:
        value = -999999
        best_col = random.choice(valid)

        for col in valid:
            row = get_next_open_row(board, col)
            temp = drop_temp(board, row, col, ai_piece)
            _, new_score = minimax(temp, depth - 1, False, ai_piece)

            if new_score > value:
                value = new_score
                best_col = col

        return best_col, value

    else:
        value = 999999
        best_col = random.choice(valid)

        for col in valid:
            row = get_next_open_row(board, col)
            temp = drop_temp(board, row, col, opp_piece)
            _, new_score = minimax(temp, depth - 1, True, ai_piece)

            if new_score < value:
                value = new_score
                best_col = col

        return best_col, value


def ai_minimax_move(board, ai_piece="O", depth=3):
    col, _ = minimax(board, depth, True, ai_piece)
    return col