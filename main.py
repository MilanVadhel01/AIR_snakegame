import pygame
import random

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 30 cells
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE # 30 cells

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 50, 50)

# Game speed
FPS = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🐍 Snake Game - Arrow Keys")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def reset_game():
    """Reset game to initial state"""
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # Moving right initially
    food = spawn_food(snake)
    score = 0
    return snake, direction, food, score

def quit_game():
    pygame.quit()
    sys.exit()

def spawn_food(snake):
    """Spawn food at random position not on snake"""
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food

def draw_game(snake, food, score, game_over):
    """Draw all game elements"""
    # Clear screen
    screen.fill(BLACK)
    
    # Draw snake
    for i, segment in enumerate(snake):
        rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                           GRID_SIZE - 2, GRID_SIZE - 2)
        color = GREEN if i == 0 else DARK_GREEN  # Head is brighter
        pygame.draw.rect(screen, color, rect)
    
    # Draw food
    food_rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE,
                            GRID_SIZE - 2, GRID_SIZE - 2)
    pygame.draw.rect(screen, RED, food_rect)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw game over screen
    if game_over:
        game_over_text = font.render("GAME OVER! R=Restart, Q=Quit", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
    
    # Update display
    pygame.display.flip()

def main():
    """Main game loop"""
    snake, direction, food, score = reset_game()
    game_over = False
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        snake, direction, food, score = reset_game()
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    # Arrow key controls
                    if event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)
        
        if not game_over:
            # Move snake
            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])
            
            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                game_over = True
            
            # Check self collision
            elif new_head in snake:
                game_over = True
            
            else:
                # Add new head
                snake.insert(0, new_head)
                
                # Check if food eaten
                if new_head == food:
                    score += 1
                    food = spawn_food(snake)
                else:
                    snake.pop()  # Remove tail
        
        # Draw everything
        draw_game(snake, food, score, game_over)
        
        # Cap frame rate
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
