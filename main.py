from connect4 import *
from ai import ai_random_move, ai_minimax_move

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


def ai_turn(board, ai_piece="O"):
    #col = ai_random_move(board)                             #random AI
    #col = ai_greedy_move(board, ai_piece="O")               #Greedy Hurestic 
    col = ai_minimax_move(board, ai_piece="O", depth=3)      #MinMax     
    print(f"AI chooses column {col}")
    return col


def run_game(vs_ai=False):
    board = create_board()
    game_over = False
    turn = 0  # 0 = Player 1 (X), 1 = Player 2 or AI (O)

    print("\nWelcome to Connect 4!")
    print_board(board)

    while not game_over:
        if turn == 0:  
            # Human player's turn
            col = player_turn(board, turn)
            if col is None:
                continue
            piece = "X"
        else:
            # Either AI or Player 2
            if vs_ai:
                col = ai_turn(board, ai_piece="O")
            else:
                col = player_turn(board, turn)
                if col is None:
                    continue
            piece = "O"

        # Place the piece
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)

        print_board(board)

        # Check for win
        if winning_move(board, piece):
            if turn == 1 and vs_ai:
                print("AI wins!")
            else:
                print(f"Player {turn + 1} ({piece}) wins!")
            game_over = True
            break

        # Check for draw
        if all(board[0][c] != " " for c in range(COLUMN_COUNT)):
            print("It's a draw!")
            game_over = True
            break

        # Switch turns
        turn = (turn + 1) % 2


def main():
    print("1. Player vs Player")
    print("2. Player vs AI")
    choice = input("Choose a mode (1/2): ")

    if choice == "2":
        run_game(vs_ai=True)
    else:
        run_game(vs_ai=False)


if __name__ == "__main__":
    main()
