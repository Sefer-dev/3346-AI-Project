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