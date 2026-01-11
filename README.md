# 🐍 AI Snake Game - Python

A classic Snake Game built with **Python** and **Pygame** featuring **Hand Gesture Control** using **OpenCV** and **MediaPipe** for finger tracking.

---

## 📁 Project Structure

```
AIR_snakegame/
├── main.py                  # Main game file with all logic
├── hand_tracking.py         # Hand detection module (to be created)
├── gesture_controller.py    # Gesture recognition for directions (to be created)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🎮 Features

- **Hand Gesture Controls**: Move snake using finger movements ✋
- **Arrow Key Controls**: Move snake using ↑ ↓ ← → keys (fallback)
- **Real-time Hand Tracking**: Using MediaPipe for accurate detection
- **Score Tracking**: Points increase when eating food
- **Collision Detection**: Game ends on wall/self collision
- **Clean Graphics**: Simple and colorful game interface

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Programming language |
| **Pygame** | Game rendering and controls |
| **OpenCV** | Webcam capture and image processing |
| **MediaPipe** | Hand landmark detection |

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pygame-ce>=2.5.0 opencv-python>=4.8.0 mediapipe>=0.10.0
```

---

## 🚀 How to Run

### Keyboard Mode (Default)
```bash
python main.py
```

### Hand Gesture Mode
```bash
python main.py --gesture
```

---

## 📋 Controls

### Keyboard Controls

| Key | Action |
|-----|--------|
| ↑ Arrow Up | Move Up |
| ↓ Arrow Down | Move Down |
| ← Arrow Left | Move Left |
| → Arrow Right | Move Right |

### ✋ Hand Gesture Controls

| Gesture | Action |
|---------|--------|
| ☝️ Point Up (Index finger up) | Move Up |
| 👇 Point Down | Move Down |
| 👈 Point Left | Move Left |
| 👉 Point Right | Move Right |
| ✊ Fist | Pause Game |

---

## 🖐️ Hand Gesture Implementation Steps

### Step 1: Update `requirements.txt`

```txt
pygame-ce>=2.5.0
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
```

---

### Step 2: Create `hand_tracking.py`

```python
import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, frame, draw=True):
        """Detect hands and return landmarks"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                
                # Extract landmark positions
                hand_lms = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_lms.append((id, cx, cy))
                landmarks.append(hand_lms)
        
        return frame, landmarks
    
    def get_finger_positions(self, landmarks):
        """Get fingertip positions (index=8, middle=12, ring=16, pinky=20, thumb=4)"""
        if not landmarks:
            return None
        
        hand = landmarks[0]
        return {
            'thumb': hand[4][1:],
            'index': hand[8][1:],
            'middle': hand[12][1:],
            'ring': hand[16][1:],
            'pinky': hand[20][1:],
            'wrist': hand[0][1:]
        }
```

---

### Step 3: Create `gesture_controller.py`

```python
class GestureController:
    def __init__(self):
        self.prev_direction = None
        
    def get_direction(self, finger_positions):
        """Determine direction based on index finger position relative to wrist"""
        if not finger_positions:
            return None
        
        index = finger_positions['index']
        wrist = finger_positions['wrist']
        
        # Calculate relative position
        dx = index[0] - wrist[0]
        dy = index[1] - wrist[1]
        
        # Determine direction based on dominant axis
        if abs(dx) > abs(dy):
            # Horizontal movement
            if dx > 50:
                return 'RIGHT'
            elif dx < -50:
                return 'LEFT'
        else:
            # Vertical movement
            if dy > 50:
                return 'DOWN'
            elif dy < -50:
                return 'UP'
        
        return self.prev_direction
    
    def fingers_up(self, landmarks):
        """Check which fingers are up"""
        if not landmarks:
            return []
        
        hand = landmarks[0]
        fingers = []
        
        # Thumb (compare x position)
        if hand[4][1] < hand[3][1]:
            fingers.append('thumb')
        
        # Other fingers (compare y position - tip vs pip)
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]
        names = ['index', 'middle', 'ring', 'pinky']
        
        for tip, pip, name in zip(tip_ids, pip_ids, names):
            if hand[tip][2] < hand[pip][2]:  # tip.y < pip.y means finger is up
                fingers.append(name)
        
        return fingers
```

---

### Step 4: Integrate with `main.py`

Add these imports and modifications:

```python
import cv2
import argparse
from hand_tracking import HandDetector
from gesture_controller import GestureController

# Add argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--gesture', action='store_true', help='Enable hand gesture control')
args = parser.parse_args()

# Initialize hand tracking if gesture mode
if args.gesture:
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    gesture = GestureController()
```

Add gesture detection in the game loop:

```python
# Inside main game loop, before event handling:
if args.gesture and not game_over:
    success, frame = cap.read()
    if success:
        frame = cv2.flip(frame, 1)  # Mirror the image
        frame, landmarks = detector.find_hands(frame)
        
        if landmarks:
            fingers = gesture.fingers_up(landmarks)
            finger_pos = detector.get_finger_positions(landmarks)
            gesture_dir = gesture.get_direction(finger_pos)
            
            # Map gesture to direction
            if gesture_dir == 'UP' and direction != (0, 1):
                direction = (0, -1)
            elif gesture_dir == 'DOWN' and direction != (0, -1):
                direction = (0, 1)
            elif gesture_dir == 'LEFT' and direction != (1, 0):
                direction = (-1, 0)
            elif gesture_dir == 'RIGHT' and direction != (-1, 0):
                direction = (1, 0)
        
        # Show webcam feed (optional)
        cv2.imshow('Hand Tracking', frame)
```

---

### Step 5: Hand Landmark Reference

MediaPipe provides 21 landmarks per hand:

```
        8   12  16  20    ← Fingertips
        |   |   |   |
        7   11  15  19
        |   |   |   |
        6   10  14  18
        |   |   |   |
        5   9   13  17
         \  |   |   /
          4 |   |  /      ← Thumb tip
           \|   | /
            3   |/
            |   1
            2  /
            | /
            0             ← Wrist
```

| Landmark ID | Description |
|-------------|-------------|
| 0 | Wrist |
| 4 | Thumb tip |
| 8 | Index finger tip |
| 12 | Middle finger tip |
| 16 | Ring finger tip |
| 20 | Pinky tip |

---

## 🎯 Gesture Detection Flow

```
┌─────────────────────────────────────────────┐
│         GESTURE DETECTION LOOP              │
├─────────────────────────────────────────────┤
│ 1. Capture frame from webcam                │
│ 2. Flip frame (mirror effect)               │
│ 3. Detect hand landmarks using MediaPipe    │
│ 4. Extract finger positions                 │
│ 5. Calculate direction from finger angle    │
│ 6. Map direction to snake movement          │
│ 7. Update game state                        │
└─────────────────────────────────────────────┘
```

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

- [x] Create `requirements.txt`
- [x] Set up constants and colors
- [x] Initialize Pygame window
- [x] Implement arrow key controls
- [x] Implement snake movement
- [x] Add collision detection
- [x] Add food and scoring
- [x] Add game over screen

---

Happy Coding! 🎮🐍
