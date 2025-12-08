import pygame
import sys
import math

# Colors
BLUE = (0, 100, 200)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
YELLOW = (255, 220, 50)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
DARK_BLUE = (20, 40, 80)
GREEN = (50, 200, 100)

# Game constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Screen dimensions
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE


class GameUI:
    """
    Handles all visual rendering and user input for Connect 4.
    Separated from game logic for modularity.
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect 4 - AI Challenge")
        self.font_large = pygame.font.SysFont("arial", 60, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 36, bold=True)
        self.font_small = pygame.font.SysFont("arial", 24)
        self.clock = pygame.time.Clock()
        
    def draw_board(self, board):
        """Draw the Connect 4 board with current piece positions."""
        # Draw blue board with holes
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(
                    self.screen, 
                    BLUE, 
                    (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
                )
                pygame.draw.circle(
                    self.screen, 
                    BLACK, 
                    (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), 
                    RADIUS
                )
        
        # Draw pieces
        # Note: board[0] is top row, board[5] is bottom row
        # Screen y increases downward, with row 0 at y=SQUARESIZE
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                piece = board[r][c]
                # Calculate y position: row 0 at top of board, row 5 at bottom
                y_pos = int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)
                x_pos = int(c * SQUARESIZE + SQUARESIZE / 2)
                
                if piece == "X":
                    pygame.draw.circle(self.screen, RED, (x_pos, y_pos), RADIUS)
                elif piece == "O":
                    pygame.draw.circle(self.screen, YELLOW, (x_pos, y_pos), RADIUS)
        
        pygame.display.update()
    
    def draw_hover_piece(self, posx, turn):
        """Draw the hovering piece above the board."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        color = RED if turn == 0 else YELLOW
        pygame.draw.circle(self.screen, color, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
    
    def clear_top(self):
        """Clear the top area of the screen."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        pygame.display.update()
    
    def show_winner(self, winner_text, color):
        """Display the winner message."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.font_large.render(winner_text, True, color)
        label_rect = label.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
        self.screen.blit(label, label_rect)
        pygame.display.update()
    
    def show_draw(self):
        """Display draw message."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.font_large.render("It's a Draw!", True, WHITE)
        label_rect = label.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
        self.screen.blit(label, label_rect)
        pygame.display.update()
    
    def get_column_from_mouse(self, posx):
        """Convert mouse x position to column index."""
        return int(math.floor(posx / SQUARESIZE))
    
    def draw_button(self, rect, text, color, text_color=WHITE, hover=False):
        """Draw a styled button."""
        button_color = tuple(min(c + 30, 255) for c in color) if hover else color
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, rect, 3, border_radius=10)
        
        text_surface = self.font_medium.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def show_main_menu(self):
        """
        Display main menu with Start Game option.
        Returns: True if Start Game is clicked, None if quit.
        """
        self.screen.fill(DARK_BLUE)
        
        # Title
        title = self.font_large.render("CONNECT 4", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("AI Challenge Edition", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Start button
        start_button = pygame.Rect(WIDTH // 2 - 150, 280, 300, 70)
        
        # Quit button
        quit_button = pygame.Rect(WIDTH // 2 - 150, 380, 300, 70)
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            start_hover = start_button.collidepoint(mouse_pos)
            quit_hover = quit_button.collidepoint(mouse_pos)
            
            # Redraw buttons
            self.draw_button(start_button, "Start Game", GREEN, WHITE, start_hover)
            self.draw_button(quit_button, "Quit", RED, WHITE, quit_hover)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        return True
                    if quit_button.collidepoint(event.pos):
                        return None
            
            self.clock.tick(60)
    
    def show_game_mode_menu(self):
        """
        Display game mode selection menu.
        Returns: 
            "pvp" for Player vs Player
            "ai" for Player vs AI
            -1 for back
            None for quit
        """
        self.screen.fill(DARK_BLUE)
        
        # Title
        title = self.font_large.render("Select Mode", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Mode buttons
        button_height = 70
        button_width = 350
        
        pvp_button = pygame.Rect(WIDTH // 2 - button_width // 2, 200, button_width, button_height)
        ai_button = pygame.Rect(WIDTH // 2 - button_width // 2, 310, button_width, button_height)
        back_button = pygame.Rect(20, HEIGHT - 70, 120, 50)
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            # Redraw background
            pygame.draw.rect(self.screen, DARK_BLUE, (0, 180, WIDTH, 250))
            
            # Draw mode buttons
            pvp_hover = pvp_button.collidepoint(mouse_pos)
            ai_hover = ai_button.collidepoint(mouse_pos)
            back_hover = back_button.collidepoint(mouse_pos)
            
            self.draw_button(pvp_button, "Player vs Player", BLUE, WHITE, pvp_hover)
            pvp_desc = self.font_small.render("Two players take turns", True, LIGHT_GRAY)
            pvp_desc_rect = pvp_desc.get_rect(center=(WIDTH // 2, pvp_button.bottom + 15))
            self.screen.blit(pvp_desc, pvp_desc_rect)
            
            self.draw_button(ai_button, "Player vs AI", GREEN, WHITE, ai_hover)
            ai_desc = self.font_small.render("Challenge the computer", True, LIGHT_GRAY)
            ai_desc_rect = ai_desc.get_rect(center=(WIDTH // 2, ai_button.bottom + 15))
            self.screen.blit(ai_desc, ai_desc_rect)
            
            self.draw_button(back_button, "Back", GRAY, WHITE, back_hover)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_button.collidepoint(event.pos):
                        return "pvp"
                    if ai_button.collidepoint(event.pos):
                        return "ai"
                    if back_button.collidepoint(event.pos):
                        return -1
            
            self.clock.tick(60)
    
    def show_difficulty_menu(self):
        """
        Display difficulty selection menu.
        Returns: difficulty level (1-4) or None if back/quit.
            1 = Easy (Random)
            2 = Normal (Greedy Heuristic)
            3 = Hard (Minimax without Alpha-Beta)
            4 = Very Hard (Minimax with Alpha-Beta)
        """
        self.screen.fill(DARK_BLUE)
        
        # Title
        title = self.font_large.render("Select Difficulty", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Difficulty buttons
        button_height = 60
        button_width = 350
        start_y = 160
        spacing = 80
        
        difficulties = [
            ("Easy", GREEN, "Random moves"),
            ("Normal", YELLOW, "Greedy heuristic"),
            ("Hard", (255, 165, 0), "Minimax (depth 4)"),
            ("Very Hard", RED, "Alpha-Beta (depth 5)")
        ]
        
        buttons = []
        for i, (name, color, desc) in enumerate(difficulties):
            btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, start_y + i * spacing, button_width, button_height)
            buttons.append((btn_rect, name, color, desc, i + 1))
        
        # Back button
        back_button = pygame.Rect(20, HEIGHT - 70, 120, 50)
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            # Redraw background for descriptions
            pygame.draw.rect(self.screen, DARK_BLUE, (0, start_y - 20, WIDTH, len(difficulties) * spacing + 100))
            
            # Draw difficulty buttons
            for btn_rect, name, color, desc, level in buttons:
                hover = btn_rect.collidepoint(mouse_pos)
                self.draw_button(btn_rect, name, color, BLACK if color == YELLOW else WHITE, hover)
                
                # Description text
                desc_surface = self.font_small.render(desc, True, LIGHT_GRAY)
                desc_rect = desc_surface.get_rect(center=(WIDTH // 2, btn_rect.bottom + 15))
                self.screen.blit(desc_surface, desc_rect)
            
            # Draw back button
            back_hover = back_button.collidepoint(mouse_pos)
            self.draw_button(back_button, "Back", GRAY, WHITE, back_hover)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn_rect, name, color, desc, level in buttons:
                        if btn_rect.collidepoint(event.pos):
                            return level
                    if back_button.collidepoint(event.pos):
                        return -1  # Signal to go back
            
            self.clock.tick(60)
    
    def show_thinking(self):
        """Show AI thinking indicator."""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.font_medium.render("AI is thinking...", True, YELLOW)
        label_rect = label.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
        self.screen.blit(label, label_rect)
        pygame.display.update()
    
    def wait(self, milliseconds):
        """Wait for specified milliseconds."""
        pygame.time.wait(milliseconds)
    
    def process_events(self):
        """
        Process pygame events.
        Returns: dict with event information or None for quit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"type": "quit"}
            if event.type == pygame.MOUSEMOTION:
                return {"type": "motion", "pos": event.pos}
            if event.type == pygame.MOUSEBUTTONDOWN:
                return {"type": "click", "pos": event.pos}
        return {"type": "none"}
    
    def quit(self):
        """Clean up pygame."""
        pygame.quit()
        sys.exit()


def main():
    """Test the UI independently."""
    ui = GameUI()
    
    # Test main menu
    result = ui.show_main_menu()
    if result is None:
        ui.quit()
    
    # Test difficulty menu
    difficulty = ui.show_difficulty_menu()
    if difficulty is None:
        ui.quit()
    
    print(f"Selected difficulty: {difficulty}")
    ui.quit()


if __name__ == "__main__":
    main()
