class GestureController:
    """Gesture recognition controller for snake direction."""
    
    def __init__(self):
        self.prev_direction = None
        
    def get_direction(self, finger_positions):
        """Determine direction based on index finger position relative to wrist."""
        if not finger_positions:
            return self.prev_direction
        
        index = finger_positions['index']
        wrist = finger_positions['wrist']
        
        # Calculate relative position
        dx = index[0] - wrist[0]
        dy = index[1] - wrist[1]
        
        # Determine direction based on dominant axis
        if abs(dx) > abs(dy):
            # Horizontal movement
            if dx > 50:
                self.prev_direction = 'RIGHT'
            elif dx < -50:
                self.prev_direction = 'LEFT'
        else:
            # Vertical movement
            if dy > 50:
                self.prev_direction = 'DOWN'
            elif dy < -50:
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
