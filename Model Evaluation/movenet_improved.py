import tensorflow as tf
import numpy as np
import keyboard as kb
import cv2
import time


EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

COLORS = {
    'y': (0,255,255),
    'm': (255,0,255),
    'c': (255,255,0)
}

prev_frame_time = 0
p_time = []
prev_frame_width = 0
prev_frame_height = 0
threshold = 0.25
bool = False
threshold_clap = 0.15
threshold_horizontal = 0
threshold_upper = 0.25
threshold_lower = 0.4
center_points = []
count = 0
lock_lr = False
lock_cj = False
arr_lr = []
arr_cj = []
frame_count = 5
wait = 0

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="3.tflite")
interpreter.allocate_tensors()

# Get cam
cap = cv2.VideoCapture("WIN_20240501_22_20_47_Pro.mp4")
cap.set(cv2.CAP_PROP_FPS, 60)
while cap.isOpened():
    ret, frame = cap.read()
    count += 1
    if not ret:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        break
    height, width, _ = frame.shape

    # Input
    image = frame.copy()
    image = np.expand_dims(image, axis=0)
    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    image = tf.image.resize_with_pad(image, 192, 192)

    # Output
    # TF Lite format expects tensor type of float32.
    input_image = tf.cast(image, dtype=tf.float32)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))

    interpreter.invoke()

    # Output is a [1, 1, 17, 3] numpy array.
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    # print(keypoints_with_scores)

    # Draw keypoints
    keypoints = np.squeeze(np.multiply(keypoints_with_scores, [height,width,1]))
    for keypoint in keypoints:
        ky, kx, ks = keypoint
        if ks > threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)

    # Draw edges
    for edge, color in EDGES.items():
        p1, p2 = edge
        ky1, kx1, ks1 = keypoints[p1]
        ky2, kx2, ks2 = keypoints[p2]
        if ks1 > threshold and ks2 > threshold:
            cv2.line(frame, (int(kx1), int(ky1)),(int(kx2), int(ky2)), COLORS[color], 2)
    
    # Movement
    # Center point
    center_width = int((keypoints[5][1] + keypoints[6][1]
            + (keypoints[11][1] + keypoints[12][1])/2)/3)
    center_height = int((keypoints[5][0] + keypoints[6][0]
            + (keypoints[11][0] + keypoints[12][0])/2)/3)
    cv2.circle(frame, (center_width,center_height), radius=10, color=(0, 0, 255), thickness=-1)
    if prev_frame_width == 0 and prev_frame_height == 0:
        prev_frame_width = center_width
        prev_frame_height = center_height
    # Left/Right/Jump/Crouch
    if bool == False:
    # Width for left right
        left = int(keypoints[5][1])
        cv2.line(frame, (left, 0), (left, height), (255, 0, 0), 2)
        right = int(keypoints[6][1])
        cv2.line(frame, (right, 0), (right, height), (255, 0, 0), 2)
        left_fixed = int(left + (left - right) * threshold_horizontal)
        right_fixed = int(right - (left - right) * threshold_horizontal)

        # Height for jump crouch
        upper = int(keypoints[6][0])
        cv2.line(frame, (0, upper), (width, upper), (255, 0, 0), 2)
        lower = int(keypoints[12][0])
        cv2.line(frame, (0, lower), (width, lower), (255, 0, 0), 2)
        upper_fixed = int(upper + (lower - upper) * threshold_upper)
        lower_fixed = int(lower - (lower - upper) * threshold_lower)

    # Clap threshold
    width_clap_l = int(keypoints[9][1])
    cv2.line(frame, (width_clap_l, 0), (width_clap_l, height), (255, 0, 0), 2)
    width_clap_r = int(keypoints[10][1])
    cv2.line(frame, (width_clap_r, 0), (width_clap_r, height), (255, 0, 0), 2)      
    if (width_clap_l - width_clap_r)/width < threshold_clap and bool == False:
        bool = True
        print("locked")
        kb.send("space")
    bool = True
    if bool:
        frame_thres = 0.14*(int(keypoints[5][1]) - int(keypoints[6][1]))
        arr_lr.append(center_width)
        arr_cj.append(center_height)
        if len(arr_lr) > frame_count:
            arr_lr.pop(0)
        if len(arr_cj) > frame_count:
            arr_cj.pop(0)        
        if lock_lr == False and len(arr_lr) == frame_count and arr_lr == sorted(arr_lr) and arr_lr[4] - arr_lr[0] > frame_thres:
            print(count)
            print("left")
            kb.send("a")
            lock_lr = True
        if lock_lr == False and len(arr_lr) == frame_count and arr_lr == sorted(arr_lr, reverse = True) and arr_lr[4] - arr_lr[0] < -frame_thres:
            print(count)
            print("right")
            kb.send("d")
            lock_lr = True
        if lock_lr == True and len(arr_lr) == frame_count and arr_lr == sorted(arr_lr) and arr_lr[4] - arr_lr[0] <= frame_thres:
            lock_lr = False
        if lock_lr == True and len(arr_lr) == frame_count and arr_lr == sorted(arr_lr, reverse = True) and arr_lr[4] - arr_lr[0] >= -frame_thres:
            lock_lr = False
        if lock_cj == False and len(arr_cj) == 5 and arr_cj == sorted(arr_cj) and arr_cj[4] - arr_cj[0] > 30:
            print(count)
            print("crouch")
            kb.send("s")
            lock_cj = True
        if lock_cj == False and len(arr_cj) == 5 and arr_cj == sorted(arr_cj, reverse = True) and arr_cj[4] - arr_cj[0] < -30:
            print(count)
            print("jump")
            kb.send("w")
            lock_cj = True
        if lock_cj == True:
            wait += 1
            if wait > 60:
                wait = 0
                lock_cj = False
        


    # Get fps
    frame = cv2.flip(frame, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    # print(1/fps)
    # p_time.append(1/fps)
    fps = int(fps) 
    fps = str(fps) 

    # Track center point
    center_points.append([center_height, center_width])

    # Show
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('MoveNet Lightning', frame)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break

# with open("output_movenet.txt", "a") as f:
#   for center_point in center_points:
#     print(center_point, file=f)
# print(np.mean(p_time[1:]))
print(int(keypoints[5][1]) - int(keypoints[6][1]))
print(left_fixed, right_fixed)
print(lower_fixed, upper_fixed)
cap.release()
cv2.destroyAllWindows()
