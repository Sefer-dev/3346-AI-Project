from connect4 import *
from ai import get_ai_move

def main():
    board = create_board()
    game_over = False
    turn = 0  # Player 1 = 0, Player 2 = 1

    print("Welcome to Connect 4!")
    print_board(board)

    while not game_over:
        if turn == 1:
            print("AI Turn:")

            col = get_ai_move(board)

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, "O")
            print_board(board)

            if winning_move(board, "O"):
                print("AI (O) wins!")
                return

            turn = 0
            continue

        # Ask for Player input
        col = input("Your turn. Choose a column (0-6): ")

        if not col.isdigit() or int(col) not in range(COLUMN_COUNT):
            print("Invalid input. Choose a number between 0 and 6.")
            continue

        col = int(col)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            piece = "X" if turn == 0 else "O"
            drop_piece(board, row, col, piece)

            print_board(board)

            if winning_move(board, piece):
                print(f"Player {turn + 1} ({piece}) wins!")
                game_over = True

            turn = (turn + 1) % 2  # Switch players
        else:
            print("Column is full! Try another.")

    print("Game Over!")

if __name__ == "__main__":
    main()
