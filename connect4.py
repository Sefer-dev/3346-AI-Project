ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = [[" " for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    return board

def print_board(board):
    # Print from top row down
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("  " + "   ".join(str(i) for i in range(COLUMN_COUNT)))

def is_valid_location(board, col):
    return board[0][col] == " "

def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negative diagonal
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False
