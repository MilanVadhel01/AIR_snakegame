# 🐍 Snake Game - Python

A classic Snake Game built with **Python** and **Pygame** that uses **arrow keys** for movement.

---

## 📁 Project Structure

```
AIR_snakegame/
├── main.py              # Main game file with all logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🎮 Features

- **Arrow Key Controls**: Move snake using ↑ ↓ ← → keys
- **Score Tracking**: Points increase when eating food
- **Collision Detection**: Game ends on wall/self collision
- **Clean Graphics**: Simple and colorful game interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Programming language |
| **Pygame** | Game rendering and controls |

---

## 📦 Installation

### Step 1: Install Dependencies
```bash
pip install pygame
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```
Or

```bash
python -m pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python main.py
```

---

## 📋 Controls

| Key | Action |
|-----|--------|
| ↑ Arrow Up | Move Up |
| ↓ Arrow Down | Move Down |
| ← Arrow Left | Move Left |
| → Arrow Right | Move Right |

---

## 🛠️ Implementation Steps

### Step 1: Create `requirements.txt`
```txt
pygame>=2.1.0
```

---

### Step 2: Set Up Game Constants

```python
# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 30 cells
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE # 30 cells

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game speed
FPS = 10
```

---

### Step 3: Initialize Pygame

```python
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
```

---

### Step 4: Snake Variables

```python
# Snake starting position (center of screen)
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = (1, 0)  # Moving right initially

# Food position
food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

# Score
score = 0
```

---

### Step 5: Arrow Key Handler

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and direction != (0, 1):
            direction = (0, -1)
        elif event.key == pygame.K_DOWN and direction != (0, -1):
            direction = (0, 1)
        elif event.key == pygame.K_LEFT and direction != (1, 0):
            direction = (-1, 0)
        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
            direction = (1, 0)
```

> **Note**: Conditions prevent snake from reversing into itself.

---

### Step 6: Snake Movement

```python
# Get new head position
head = snake[0]
new_head = (head[0] + direction[0], head[1] + direction[1])

# Add new head
snake.insert(0, new_head)

# Remove tail (unless eating food)
if new_head == food:
    score += 1
    food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
else:
    snake.pop()
```

---

### Step 7: Collision Detection

```python
# Wall collision
if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
    game_over = True

# Self collision
if new_head in snake[1:]:
    game_over = True
```

---

### Step 8: Drawing Functions

```python
# Clear screen
screen.fill(BLACK)

# Draw snake
for segment in snake:
    rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                       GRID_SIZE - 2, GRID_SIZE - 2)
    pygame.draw.rect(screen, GREEN, rect)

# Draw food
food_rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE,
                        GRID_SIZE - 2, GRID_SIZE - 2)
pygame.draw.rect(screen, RED, food_rect)

# Update display
pygame.display.flip()
```

---

## 🎯 Game Loop Flow

```
┌─────────────────────────────────────────┐
│            GAME LOOP                    │
├─────────────────────────────────────────┤
│ 1. Handle Events (Arrow Keys)           │
│ 2. Update Direction                     │
│ 3. Move Snake (add head, remove tail)   │
│ 4. Check Collisions                     │
│    - Wall → Game Over                   │
│    - Self → Game Over                   │
│ 5. Check Food Eaten → Grow + Score      │
│ 6. Draw Everything                      │
│ 7. Update Display                       │
│ 8. Tick Clock (FPS)                     │
└─────────────────────────────────────────┘
```

---

## 📝 Complete Code Structure

```python
# main.py structure

import pygame
import random

# Constants
# ... (window size, colors, speed)

# Initialize Pygame
# ... 

# Game variables
# ... (snake, direction, food, score)

# Main game loop
running = True
while running:
    # 1. Event handling (arrow keys)
    # 2. Move snake
    # 3. Check collisions
    # 4. Check food eaten
    # 5. Draw everything
    # 6. Update display
    clock.tick(FPS)

pygame.quit()
```

---

## 🔧 Customization

| Setting | Default | Description |
|---------|---------|-------------|
| `WINDOW_WIDTH` | 600 | Game window width |
| `WINDOW_HEIGHT` | 600 | Game window height |
| `GRID_SIZE` | 20 | Size of each cell |
| `FPS` | 10 | Game speed |

---

## 📋 Development Checklist

- [ ] Create `requirements.txt`
- [ ] Set up constants and colors
- [ ] Initialize Pygame window
- [ ] Implement arrow key controls
- [ ] Implement snake movement
- [ ] Add collision detection
- [ ] Add food and scoring
- [ ] Add game over screen

---

Happy Coding! 🎮🐍
