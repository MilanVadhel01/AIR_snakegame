class GestureController:
    """Gesture recognition controller for snake direction."""
    
    def __init__(self):
        self.prev_direction = None
        self.prev_finger_pos = None  # Track previous finger position
        self.movement_threshold = 30  # Minimum movement to register a swipe
        
    def get_direction(self, finger_positions):
        """Determine direction based on finger MOVEMENT (swipe), not position."""
        if not finger_positions:
            return self.prev_direction
        
        index = finger_positions['index']
        
        # First frame - just store position
        if self.prev_finger_pos is None:
            self.prev_finger_pos = index
            return self.prev_direction
        
        # Calculate movement delta (how much finger moved since last frame)
        dx = index[0] - self.prev_finger_pos[0]
        dy = index[1] - self.prev_finger_pos[1]
        
        # Update previous position
        self.prev_finger_pos = index
        
        # Determine direction based on dominant movement axis
        if abs(dx) > self.movement_threshold or abs(dy) > self.movement_threshold:
            if abs(dx) > abs(dy):
                # Horizontal swipe
                if dx > 0:
                    self.prev_direction = 'RIGHT'
                else:
                    self.prev_direction = 'LEFT'
            else:
                # Vertical swipe
                if dy > 0:
                    self.prev_direction = 'DOWN'
                else:
                    self.prev_direction = 'UP'
        
        return self.prev_direction
    
    def fingers_up(self, landmarks):
        """Check which fingers are up."""
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
    
    def is_fist(self, landmarks):
        """Check if hand is making a fist gesture (no fingers up)."""
        fingers = self.fingers_up(landmarks)
        return len(fingers) == 0
