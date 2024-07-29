import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("WIN_20240108_16_48_00_Pro.mp4")
preds = []
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      break

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    height, width, _ = image.shape
    if results.pose_landmarks:
      # Center point
      center_width = ((results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x
              + (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x)/2)/3 * width)
      center_height = ((results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[12].y
              + (results.pose_landmarks.landmark[23].y + results.pose_landmarks.landmark[24].y)/2)/3 * height)
    cv2.circle(image, (int(center_width), int(center_height)), 1, (0, 255, 0), -1)
    preds.append([center_width, center_height])
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow("image", image)
    cv2.waitKey(1)
image = cv2.imread("Screenshot 2024-01-08 165027.png")
image = cv2.resize(image, (width, height))
for pred in preds:
    cv2.circle(image, (int(pred[0]), int(pred[1])), 1, (0, 255, 0), -1)
with mp_pose.Pose(
  min_detection_confidence=0.5,
  min_tracking_confidence=0.5) as pose:
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    height, width, _ = image.shape 
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imshow("image", image)
cv2.waitKey(0)
