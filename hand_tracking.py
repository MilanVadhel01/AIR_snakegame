import cv2
import mediapipe as mp


class HandDetector:
    """Hand detection class using MediaPipe for gesture-based control."""
    
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
        """Detect hands and return landmarks."""
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
        """Get fingertip positions (index=8, middle=12, ring=16, pinky=20, thumb=4)."""
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
    
    def release(self):
        """Release MediaPipe resources."""
        self.hands.close()
