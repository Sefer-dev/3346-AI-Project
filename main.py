from connect4 import *

def main():
    board = create_board()
    game_over = False
    turn = 0  # Player 1 = 0, Player 2 = 1

    print("Welcome to Connect 4!")
    print_board(board)

    while not game_over:
        # Ask for Player input
        col = input(f"Player {turn + 1} ({'X' if turn == 0 else 'O'}), choose a column (0-6): ")

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
