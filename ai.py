import random 
from connect4 import (
    ROW_COUNT,
    COLUMN_COUNT,
    is_valid_location,
    get_next_open_row,
    winning_move
)


#RANDOM AI:
def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def ai_random_move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations)


# 2. SCORING HEURISTIC — Used by minimax
def score_position(board, piece):
    """
    Basic scoring for making better decisions:
    + Favor center column
    + Favor moves that create 2 or 3 in a row
    + Try to block opponent
    """
    
    score = 0
    opponent_piece = "O" if piece == "X" else "X"

    # Score center column (AI plays generically better)
    center_col = [board[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
    center_count = center_col.count(piece)
    score += center_count * 3

    return score



#MINIMAX AI 
def minimax(board, depth, maximizingPlayer, ai_piece):
    player_piece = "O" if ai_piece == "X" else "X"

    valid_locations = get_valid_locations(board)

    # Terminal state check
    if winning_move(board, ai_piece):
        return None, 999999
    if winning_move(board, player_piece):
        return None, -999999
    if depth == 0 or len(valid_locations) == 0:
        return None, score_position(board, ai_piece)

    if maximizingPlayer:
        best_score = -1e10
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)

            # Copy board
            temp_board = [row[:] for row in board]
            temp_board[row][col] = ai_piece

            _, new_score = minimax(temp_board, depth - 1, False, ai_piece)

            if new_score > best_score:
                best_score = new_score
                best_col = col

        return best_col, best_score

    else:
        best_score = 1e10
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)

            # Copy board
            temp_board = [row[:] for row in board]
            temp_board[row][col] = player_piece

            _, new_score = minimax(temp_board, depth - 1, True, ai_piece)

            if new_score < best_score:
                best_score = new_score
                best_col = col

        return best_col, best_score


def ai_minimax_move(board, depth=3, ai_piece="O"):
    col, _ = minimax(board, depth, True, ai_piece)
    return col