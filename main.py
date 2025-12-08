"""
Connect 4 - AI Challenge Edition
Main game controller that integrates UI, game logic, and AI.

This module serves as the entry point and game loop controller,
connecting the GameUI for rendering, connect4 for game rules,
and ai module for computer opponents.
"""

from connect4 import (
    create_board,
    print_board,
    is_valid_location,
    get_next_open_row,
    drop_piece,
    winning_move,
    COLUMN_COUNT
)
from ai import ai_random_move, ai_greedy_move, ai_minimax_move, ai_minimax_ab_move
from GameUI import GameUI, RED, YELLOW, WHITE


class Connect4Game:
    """
    Main game controller class that manages game state and coordinates
    between UI, game logic, and AI components.
    """
    
    def __init__(self):
        self.ui = GameUI()
        self.board = None
        self.game_over = False
        self.turn = 0  # 0 = Player 1 (X/Red), 1 = Player 2 or AI (O/Yellow)
        self.difficulty = 1
        self.vs_ai = True  # True for Player vs AI, False for Player vs Player
        
    def reset_game(self):
        """Reset game state for a new game."""
        self.board = create_board()
        self.game_over = False
        self.turn = 0
    
    def get_ai_move(self):
        """
        Get AI move based on selected difficulty.
        
        Difficulty levels:
            1 - Easy: Random moves
            2 - Normal: Greedy heuristic evaluation
            3 - Hard: Minimax without alpha-beta (depth 4)
            4 - Very Hard: Minimax with alpha-beta pruning (depth 5)
        """
        if self.difficulty == 1:
            return ai_random_move(self.board)
        elif self.difficulty == 2:
            return ai_greedy_move(self.board, "O")
        elif self.difficulty == 3:
            return ai_minimax_move(self.board, "O", depth=4)
        else:  # difficulty == 4
            return ai_minimax_ab_move(self.board, "O", depth=5)
    
    def check_draw(self):
        """Check if the game is a draw (board full)."""
        return all(self.board[0][c] != " " for c in range(COLUMN_COUNT))
    
    def make_move(self, col, piece):
        """
        Attempt to make a move.
        Returns: True if move was valid, False otherwise.
        """
        if not is_valid_location(self.board, col):
            return False
        
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, piece)
        return True
    
    def run_game(self):
        """
        Main game loop for a single game.
        Handles player input, AI moves, and win/draw conditions.
        """
        self.reset_game()
        self.ui.screen.fill((0, 0, 0))
        self.ui.draw_board(self.board)
        
        while not self.game_over:
            event = self.ui.process_events()
            
            if event["type"] == "quit":
                return "quit"
            
            # Player 1's turn (Red/X)
            if self.turn == 0:
                if event["type"] == "motion":
                    self.ui.draw_hover_piece(event["pos"][0], self.turn)
                
                if event["type"] == "click":
                    col = self.ui.get_column_from_mouse(event["pos"][0])
                    
                    if self.make_move(col, "X"):
                        print_board(self.board)  # Console output for debugging
                        self.ui.draw_board(self.board)
                        
                        if winning_move(self.board, "X"):
                            self.ui.show_winner("Player 1 Wins!", RED)
                            self.game_over = True
                        elif self.check_draw():
                            self.ui.show_draw()
                            self.game_over = True
                        else:
                            self.turn = 1
            
            # Player 2 or AI's turn (Yellow/O)
            else:
                if self.vs_ai:
                    # AI turn
                    self.ui.show_thinking()
                    self.ui.wait(300)  # Brief pause for visual feedback
                    
                    col = self.get_ai_move()
                    self.make_move(col, "O")
                    
                    print(f"AI chooses column {col}")
                    print_board(self.board)
                    
                    self.ui.clear_top()
                    self.ui.draw_board(self.board)
                    
                    if winning_move(self.board, "O"):
                        self.ui.show_winner("AI Wins!", YELLOW)
                        self.game_over = True
                    elif self.check_draw():
                        self.ui.show_draw()
                        self.game_over = True
                    else:
                        self.turn = 0
                else:
                    # Player 2 turn
                    if event["type"] == "motion":
                        self.ui.draw_hover_piece(event["pos"][0], self.turn)
                    
                    if event["type"] == "click":
                        col = self.ui.get_column_from_mouse(event["pos"][0])
                        
                        if self.make_move(col, "O"):
                            print_board(self.board)
                            self.ui.draw_board(self.board)
                            
                            if winning_move(self.board, "O"):
                                self.ui.show_winner("Player 2 Wins!", YELLOW)
                                self.game_over = True
                            elif self.check_draw():
                                self.ui.show_draw()
                                self.game_over = True
                            else:
                                self.turn = 0
        
        # Wait after game ends
        self.ui.wait(3000)
        return "complete"
    
    def run(self):
        """
        Main application loop.
        Handles menu navigation and game sessions.
        """
        while True:
            # Show main menu
            result = self.ui.show_main_menu()
            if result is None:
                break
            
            # Show game mode selection
            while True:
                game_mode = self.ui.show_game_mode_menu()
                
                if game_mode is None:
                    self.ui.quit()
                    return
                
                if game_mode == -1:  # Back button
                    break
                
                self.vs_ai = (game_mode == "ai")
                
                if self.vs_ai:
                    # Show difficulty selection for AI mode
                    while True:
                        difficulty = self.ui.show_difficulty_menu()
                        
                        if difficulty is None:
                            self.ui.quit()
                            return
                        
                        if difficulty == -1:  # Back button
                            break
                        
                        self.difficulty = difficulty
                        
                        # Run the game
                        game_result = self.run_game()
                        
                        if game_result == "quit":
                            self.ui.quit()
                            return
                        
                        # After game, go back to difficulty selection for rematch
                else:
                    # Player vs Player - go straight to game
                    game_result = self.run_game()
                    
                    if game_result == "quit":
                        self.ui.quit()
                        return
                    
                    # After game, go back to game mode selection
        
        self.ui.quit()


def player_turn_console(board, turn):
    """Console-based player turn for testing without UI."""
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


def ai_turn_console(board, ai_piece, mode):
    """Console-based AI turn for testing."""
    if mode == "1":
        col = ai_random_move(board)
    elif mode == "2":
        col = ai_greedy_move(board, ai_piece)
    elif mode == "3":
        col = ai_minimax_move(board, ai_piece, depth=4)
    else:
        col = ai_minimax_ab_move(board, ai_piece, depth=5)

    print(f"AI chooses column {col}")
    return col


def run_console_game(vs_ai=False, ai_mode="3"):
    """Run game in console mode (for testing without pygame)."""
    board = create_board()
    game_over = False
    turn = 0

    print("\nWelcome to Connect 4!")
    print_board(board)

    while not game_over:
        if turn == 0:
            col = player_turn_console(board, turn)
            if col is None:
                continue
            piece = "X"
        else:
            if vs_ai:
                col = ai_turn_console(board, "O", ai_mode)
            else:
                col = player_turn_console(board, turn)
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


def main_console():
    """Console-based menu for testing."""
    print("1. Player vs Player (Console)")
    print("2. Player vs AI (Console)")
    print("3. Player vs AI (GUI)")
    choice = input("Choose a mode (1/2/3): ")

    if choice == "1":
        run_console_game(vs_ai=False)
    elif choice == "2":
        print("\nChoose AI difficulty:")
        print("1. Easy (Random)")
        print("2. Normal (Greedy Heuristic)")
        print("3. Hard (Minimax)")
        print("4. Very Hard (Minimax + Alpha-Beta)")
        ai_mode = input("Select (1/2/3/4): ")
        if ai_mode not in ("1", "2", "3", "4"):
            ai_mode = "4"
        run_console_game(vs_ai=True, ai_mode=ai_mode)
    else:
        # Launch GUI version
        game = Connect4Game()
        game.run()


def main():
    """Main entry point - launches GUI version."""
    game = Connect4Game()
    game.run()


if __name__ == "__main__":
    main()
