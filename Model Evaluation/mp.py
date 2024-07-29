import cv2
import mediapipe as mp
import keyboard as kb
import time
import numpy as np
import socket

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
bool = False
threshold_clap = 0.08
threshold_horizontal = 0
threshold_vertical = -0.2
prev_frame_width = 0
prev_frame_height = 0
prev_frame_time = 0
new_frame_time = 0

# UDP setup
UDP_IP = "127.0.0.1"
UDP_PORT = 7101
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# For webcam input:
cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    height, width, _ = image.shape

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:
      center_width = int((results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x
              + (results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x)/2)/3 * width)
      center_height = int((results.pose_landmarks.landmark[11].y + results.pose_landmarks.landmark[12].y
              + (results.pose_landmarks.landmark[23].y + results.pose_landmarks.landmark[24].y)/2)/3 * height)
      cv2.circle(image, (center_width,center_height), radius=10, color=(0, 0, 255), thickness=-1)
      if prev_frame_width == 0 and prev_frame_height:
        prev_frame_width = center_width
        prev_frame_height = center_height
      if bool == False:
        left = int(results.pose_landmarks.landmark[11].x * width)
        cv2.line(image, (left, 0), (left, height), (255, 0, 0), 2)
        right = int(results.pose_landmarks.landmark[12].x * width)
        cv2.line(image, (right, 0), (right, height), (255, 0, 0), 2)
        left_fixed = int(left + (left - right) * threshold_horizontal)
        right_fixed = int(right - (left - right) * threshold_horizontal)

        upper = int(results.pose_landmarks.landmark[12].y * height)
        cv2.line(image, (0, upper), (width, upper), (255, 0, 0), 2)
        lower = int(results.pose_landmarks.landmark[24].y * height)
        cv2.line(image, (0, lower), (width, lower), (255, 0, 0), 2)
        upper_fixed = int(upper - (lower - upper) * threshold_vertical)
        lower_fixed = int(lower + (lower - upper) * threshold_vertical)

      width_clap_l = int(results.pose_landmarks.landmark[19].x * width)
      cv2.line(image, (width_clap_l, 0), (width_clap_l, height), (255, 0, 0), 2)
      width_clap_r = int(results.pose_landmarks.landmark[20].x * width)
      cv2.line(image, (width_clap_r, 0), (width_clap_r, height), (255, 0, 0), 2)      
      if (width_clap_l - width_clap_r)/width < threshold_clap and bool == False:
        bool = True
        print("locked")
        kb.send("space")
      if bool:
        cv2.line(image, (left_fixed, 0), (left_fixed, height), (255, 0, 0), 2)
        cv2.line(image, (right_fixed, 0), (right_fixed, height), (255, 0, 0), 2)
        cv2.line(image, (0, upper_fixed), (width, upper_fixed), (255, 0, 0), 2)
        cv2.line(image, (0, lower_fixed), (width, lower_fixed), (255, 0, 0), 2)

        if center_width <= right_fixed and prev_frame_width > right_fixed:
          print("right")
          kb.send("right")
        if center_width >= left_fixed and prev_frame_width < left_fixed:
          print("left")
          kb.send("left")
        if center_width > right_fixed and prev_frame_width <= right_fixed:
          print("left")
          kb.send("left")
        if center_width < left_fixed and prev_frame_width >= left_fixed: 
          print("right")
          kb.send("right")
        if center_height <= upper_fixed and prev_frame_height > upper_fixed:
          print("jump")
          kb.send("up")
        if center_height >= lower_fixed and prev_frame_height < lower_fixed:
          print("crouch")
          kb.send("down")

        data = f"{center_width},{center_height}"
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent data: {data}")

      prev_frame_width = center_width
      prev_frame_height = center_height

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    image = cv2.flip(image, 1)

    font = cv2.FONT_HERSHEY_SIMPLEX 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = int(fps) 
    fps = str(fps) 
    cv2.putText(image, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
