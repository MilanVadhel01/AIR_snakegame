import pygame
import random
import argparse
import sys

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
BLUE = (50, 150, 255)

# Game speed
FPS = 5

# Parse arguments
parser = argparse.ArgumentParser(description='Snake Game with optional gesture control')
parser.add_argument('--gesture', action='store_true', help='Enable hand gesture control')
args = parser.parse_args()

# Initialize gesture control if enabled
gesture_mode = args.gesture
cap = None
detector = None
gesture = None

if gesture_mode:
    try:
        import cv2
        from hand_tracking import HandDetector
        from gesture_controller import GestureController
        
        cap = cv2.VideoCapture(0)
        detector = HandDetector()
        gesture = GestureController()
        print("🖐️ Gesture mode enabled! Use your hand to control the snake.")
    except ImportError as e:
        print(f"Warning: Could not import gesture modules: {e}")
        print("Falling back to keyboard mode.")
        gesture_mode = False
    except Exception as e:
        print(f"Warning: Could not initialize camera: {e}")
        print("Falling back to keyboard mode.")
        gesture_mode = False

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
title = "🐍 Snake Game - Gesture Control" if gesture_mode else "🐍 Snake Game - Arrow Keys"
pygame.display.set_caption(title)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def reset_game():
    """Reset game to initial state"""
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # Moving right initially
    food = spawn_food(snake)
    score = 0
    return snake, direction, food, score

def spawn_food(snake):
    """Spawn food at random position not on snake"""
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food

def draw_game(snake, food, score, game_over, current_gesture=None):
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
    
    # Draw mode indicator
    if gesture_mode:
        mode_text = small_font.render("🖐️ Gesture Mode", True, BLUE)
        screen.blit(mode_text, (WINDOW_WIDTH - 130, 10))
        
        # Show current gesture direction
        if current_gesture:
            gesture_text = small_font.render(f"Direction: {current_gesture}", True, WHITE)
            screen.blit(gesture_text, (WINDOW_WIDTH - 130, 35))
    
    # Draw game over screen
    if game_over:
        game_over_text = font.render("GAME OVER! R=Restart, Q=Quit", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
    
    # Update display
    pygame.display.flip()

def main():
    """Main game loop"""
    global cap, detector, gesture
    
    snake, direction, food, score = reset_game()
    game_over = False
    running = True
    current_gesture = None
    
    while running:
        # Handle gesture input
        if gesture_mode and cap and not game_over:
            success, frame = cap.read()
            if success:
                import cv2
                frame = cv2.flip(frame, 1)  # Mirror the image
                frame, landmarks = detector.find_hands(frame)
                
                if landmarks:
                    finger_pos = detector.get_finger_positions(landmarks)
                    gesture_dir = gesture.get_direction(finger_pos)
                    current_gesture = gesture_dir
                    
                    # Map gesture to direction
                    if gesture_dir == 'UP' and direction != (0, 1):
                        direction = (0, -1)
                    elif gesture_dir == 'DOWN' and direction != (0, -1):
                        direction = (0, 1)
                    elif gesture_dir == 'LEFT' and direction != (1, 0):
                        direction = (-1, 0)
                    elif gesture_dir == 'RIGHT' and direction != (-1, 0):
                        direction = (1, 0)
                
                # Show webcam feed
                cv2.imshow('Hand Tracking - Press Q to quit', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    running = False
        
        # Handle keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        snake, direction, food, score = reset_game()
                        game_over = False
                        current_gesture = None
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    # Arrow key controls (always available as fallback)
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
        draw_game(snake, food, score, game_over, current_gesture)
        
        # Cap frame rate
        clock.tick(FPS)
    
    # Cleanup
    if gesture_mode and cap:
        import cv2
        cap.release()
        detector.release()
        cv2.destroyAllWindows()
    
    pygame.quit()

if __name__ == "__main__":
    main()
