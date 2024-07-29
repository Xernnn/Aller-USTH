import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
threshold_horizontal = 0
threshold_vertical = -0.2
font = cv2.FONT_HERSHEY_SIMPLEX 

image_path = "P_20240129_123739.jpg"
image = cv2.imread(image_path)
indices = [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
test = []
image = cv2.resize(image, (640,480))


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

print(height, width)
# print(test)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.putText(image, "23", (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
cv2.imshow("image", image)
cv2.waitKey(0)