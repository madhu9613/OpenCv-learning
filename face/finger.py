import cv2
import mediapipe as mp

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Function to count the number of fingers
def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Finger tip landmarks
    thumb_tip = 4  # Thumb tip landmark
    
    count = 0
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
            
    # Check thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 2].x:
        count += 1
    
    return count

# Initialize the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect hands
    result = hands.process(image_rgb)
    
    # Draw hand annotations on the image
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Count fingers
            finger_count = count_fingers(hand_landmarks)
            cv2.putText(image, f'Fingers: {finger_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (16,148,181), 2, cv2.LINE_AA)
    
    # Display the resulting frame
    cv2.imshow('Finger Count', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()

cv2.destroyAllWindows()

hands.close()