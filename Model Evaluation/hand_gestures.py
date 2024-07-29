import cv2
import mediapipe as mp

def is_peace_sign(hand_landmarks):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Check if the y-coordinate of the index finger tip is above the middle finger tip
    return index_tip.y < middle_tip.y

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open a video capture object (0 represents the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # If hand landmarks are detected, draw keypoints and edges
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw keypoints
            for landmark in hand_landmarks.landmark:
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            # Draw edges (connections between keypoints)
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize and print the gesture
            if is_peace_sign(hand_landmarks):
                print("Peace sign detected!")

    # Display the frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
