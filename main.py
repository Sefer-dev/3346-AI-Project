from connect4 import *
from ai import ai_random_move, ai_greedy_move, ai_minimax_move

def player_turn(board, turn):
    piece = "X" if turn == 0 else "O"
    col = input(f"Player {turn + 1} ({piece}), choose a column (0-6): ")

    if not col.isdigit() or int(col) not in range(COLUMN_COUNT):
        print("Invalid input. Choose a number between 0 and 6.")
        return None

    col = int(col)
    if not is_valid_location(board, col):
        print("Column full! Try another.")
        return None

    return col


def ai_turn(board, ai_piece, mode):
    if mode == "1":
        col = ai_random_move(board)
    elif mode == "2":
        col = ai_greedy_move(board, ai_piece)
    else:
        col = ai_minimax_move(board, ai_piece, depth=4)

    print(f"AI chooses column {col}")
    return col


def run_game(vs_ai=False, ai_mode="3"):
    board = create_board()
    game_over = False
    turn = 0

    print("\nWelcome to Connect 4!")
    print_board(board)

    while not game_over:
        if turn == 0:
            col = player_turn(board, turn)
            if col is None:
                continue
            piece = "X"
        else:
            if vs_ai:
                col = ai_turn(board, "O", ai_mode)
            else:
                col = player_turn(board, turn)
                if col is None:
                    continue
            piece = "O"

        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)

        print_board(board)

        if winning_move(board, piece):
            if turn == 1 and vs_ai:
                print("AI wins!")
            else:
                print(f"Player {turn + 1} ({piece}) wins!")
            game_over = True
            break

        if all(board[0][c] != " " for c in range(COLUMN_COUNT)):
            print("It's a draw!")
            game_over = True
            break

        turn = (turn + 1) % 2


def main():
    print("1. Player vs Player")
    print("2. Player vs AI")
    choice = input("Choose a mode (1/2): ")

    if choice == "2":
        print("\nChoose AI difficulty:")
        print("1. Random")
        print("2. Greedy Heuristic")
        print("3. Minimax (Hardest)")
        ai_mode = input("Select (1/2/3): ")
        if ai_mode not in ("1", "2", "3"):
            ai_mode = "3"
        run_game(vs_ai=True, ai_mode=ai_mode)
    else:
        run_game(vs_ai=False)


if __name__ == "__main__":
    main()
