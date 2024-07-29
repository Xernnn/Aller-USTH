import cv2
import mediapipe as mp
import numpy as np
import ctypes
import socket

HOST = '127.0.0.1'
PORT = 5052

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)

        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        fixed_width = screen_width // 4
        fixed_height = screen_height // 4
        window_x = 0
        window_y = 0

        cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
        cv2.moveWindow('MediaPipe Pose', window_x, window_y)
        cv2.resizeWindow('MediaPipe Pose', fixed_width, fixed_height)

        cv2.setWindowProperty('MediaPipe Pose', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('MediaPipe Pose', cv2.WND_PROP_TOPMOST, 1)

        hwnd = ctypes.windll.user32.FindWindowW(None, "MediaPipe Pose")
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, ctypes.windll.user32.GetWindowLongW(hwnd, -16) & ~0x00800000)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000 | 0x20)

        opacity = 255
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, opacity, 0x2)

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        mp_hands = mp.solutions.hands

        bool_locked = False
        threshold_clap = 0.08
        threshold_horizontal = 0
        threshold_vertical = -0.2
        prev_frame_width = 0
        prev_frame_height = 0

        left_fixed = 0
        right_fixed = 0
        upper_fixed = 0
        lower_fixed = 0

        selected_landmarks = [0, 16, 14, 12, 11, 13, 15, 24, 23]

        prev_hand_x, prev_hand_y = 0, 0

        def detection(image, pose, hands):
            global bool_locked, prev_frame_width, prev_frame_height, left_fixed, right_fixed, upper_fixed, lower_fixed, prev_hand_x, prev_hand_y
            height, width, _ = image.shape
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            fullbody_output = "[]"
            hand_output = "(0, 0)"
            pose_output = "()"
            move = 0

            # Pose detection
            pose_results = pose.process(image_rgb)
            if pose_results.pose_landmarks:
                center_x = int((pose_results.pose_landmarks.landmark[11].x + pose_results.pose_landmarks.landmark[12].x
                                + pose_results.pose_landmarks.landmark[23].x + pose_results.pose_landmarks.landmark[24].x) / 4 * width)
                center_y = int((pose_results.pose_landmarks.landmark[11].y + pose_results.pose_landmarks.landmark[12].y
                                + pose_results.pose_landmarks.landmark[23].y + pose_results.pose_landmarks.landmark[24].y) / 4 * height)
                cv2.circle(image, (center_x, center_y), radius=10, color=(0, 0, 255), thickness=-1)

                if prev_frame_width == 0 and prev_frame_height == 0:
                    prev_frame_width = center_x
                    prev_frame_height = center_y

                if not bool_locked:
                    left = int(pose_results.pose_landmarks.landmark[11].x * width)
                    right = int(pose_results.pose_landmarks.landmark[12].x * width)
                    left_fixed = int(left + (left - right) * threshold_horizontal)
                    right_fixed = int(right - (left - right) * threshold_horizontal)

                    upper = int(pose_results.pose_landmarks.landmark[12].y * height)
                    lower = int(pose_results.pose_landmarks.landmark[24].y * height)
                    upper_fixed = int(upper - (lower - upper) * threshold_vertical)
                    lower_fixed = int(lower + (lower - upper) * threshold_vertical)

                width_clap_l = int(pose_results.pose_landmarks.landmark[19].x * width)
                width_clap_r = int(pose_results.pose_landmarks.landmark[20].x * width)

                if (width_clap_l - width_clap_r) / width < threshold_clap and not bool_locked:
                    bool_locked = True
                    print("locked")
                    move = 5

                if bool_locked:
                    cv2.rectangle(image, (left_fixed, upper_fixed), (right_fixed, lower_fixed), (255, 0, 0), 2)

                    if center_x <= right_fixed and prev_frame_width > right_fixed:
                        print("right")
                        move = 1
                    if center_x >= left_fixed and prev_frame_width < left_fixed:
                        print("left")
                        move = 2
                    if center_x > right_fixed and prev_frame_width <= right_fixed:
                        print("left")
                        move = 2
                    if center_x < left_fixed and prev_frame_width >= left_fixed:
                        print("right")
                        move = 1
                    if center_y <= upper_fixed and prev_frame_height > upper_fixed:
                        print("jump")
                        move = 3
                    if center_y >= lower_fixed and prev_frame_height < lower_fixed:
                        print("crouch")
                        move = 4
                    if (width_clap_l - width_clap_r) / width < threshold_clap:
                        print("locked")
                        move = 5

                prev_frame_width = center_x
                prev_frame_height = center_y

                pose_output = f"({center_x}, {center_y}), {move}"

            # Hand detection
            hand_results = hands.process(image_rgb)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    hand_center_x = int((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x +
                                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x +
                                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x) / 3 * width)
                    hand_center_y = int((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y +
                                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y +
                                        hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y) / 3 * height)
                    cv2.circle(image, (hand_center_x, hand_center_y), radius=10, color=(0, 0, 255), thickness=-1) # Red dot for hand
                    hand_output = f"({hand_center_x}, {hand_center_y})"
                    # Update the previous hand coordinates
                    prev_hand_x, prev_hand_y = hand_center_x, hand_center_y
                    break
            else:
                # Use previous hand coordinates if no hand is detected
                hand_output = f"({prev_hand_x}, {prev_hand_y})"

            # Full body detection
            if pose_results.pose_landmarks:
                landmarks = []
                for idx in sorted(selected_landmarks, reverse=True):
                    landmark = pose_results.pose_landmarks.landmark[idx]
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    landmarks.append([x, y])
                    cv2.circle(image, (x, y), radius=5, color=(0, 255, 0), thickness=-1)
                fullbody_output = f"{landmarks}"
                # conn.sendall(f"{landmarks}\n".encode())

            # Combine all outputs into one line
            combined_output = f"{fullbody_output}, {hand_output}, {pose_output}"
            conn.sendall(f"{fullbody_output}, {hand_output}, {pose_output}".encode())
            print(combined_output)

            return image

        def main():
            cap = cv2.VideoCapture(0)
            prev_frame_time = 0
            new_frame_time = 0

            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
                 mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

                while cap.isOpened():
                    success, image = cap.read()
                    if not success:
                        print("Ignoring empty camera frame.")
                        break

                    image = cv2.resize(image, (fixed_width, fixed_height), interpolation=cv2.INTER_LINEAR)
                    image = detection(image, pose, hands)
                    image = cv2.flip(image, 1)

                    cv2.imshow('MediaPipe Pose', image)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

        if __name__ == "__main__":
            main()
