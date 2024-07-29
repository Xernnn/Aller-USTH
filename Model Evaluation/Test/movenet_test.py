# Import TF and TF Hub libraries.
import tensorflow as tf
import numpy as np
import cv2 
threshold_clap = 0.15
threshold_horizontal = 0
threshold_upper = -0.25
threshold_lower = -0.15


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

threshold = 0.25

# Load the input image.
image_path = 'P_20240127_194656.jpg'
image = cv2.imread(image_path)
image = cv2.resize(image, (640,480))
height, width, _ = image.shape
input_image = tf.expand_dims(image, axis=0)
# Resize and pad the image to keep the aspect ratio and fit the expected size.
input_image = tf.image.resize_with_pad(input_image, 192, 192)

# Initialize the TFLite interpreter
model_path = '3.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# TF Lite format expects tensor type of float32.
input_image = tf.cast(input_image, dtype=tf.float32)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'], input_image.numpy())

interpreter.invoke()

# Output is a [1, 1, 17, 3] numpy array.
keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
keypoints = np.squeeze(np.multiply(keypoints_with_scores, [height,width,1]))
for keypoint in keypoints:
    ky, kx, ks = keypoint
    if ks > threshold:
        cv2.circle(image, (int(kx), int(ky)), 4, (0, 255, 0), -1)

# Draw edges
for edge, color in EDGES.items():
    p1, p2 = edge
    ky1, kx1, ks1 = keypoints[p1]
    ky2, kx2, ks2 = keypoints[p2]
    if ks1 > threshold and ks2 > threshold:
        cv2.line(image, (int(kx1), int(ky1)),(int(kx2), int(ky2)), COLORS[color], 2)
    center_width = int((keypoints[5][1] + keypoints[6][1]
            + (keypoints[11][1] + keypoints[12][1])/2)/3)
    center_height = int((keypoints[5][0] + keypoints[6][0]
            + (keypoints[11][0] + keypoints[12][0])/2)/3)
    cv2.circle(image, (center_width,center_height), radius=10, color=(0, 0, 255), thickness=-1)
    # Left/Right/Jump/Crouch
    # Width for left right
    left = int(keypoints[5][1])
    cv2.line(image, (left, 0), (left, height), (0, 0, 255), 2)
    right = int(keypoints[6][1])
    cv2.line(image, (right, 0), (right, height), (0, 0, 255), 2)
    left_fixed = int(left + (left - right) * threshold_horizontal)
    right_fixed = int(right - (left - right) * threshold_horizontal)

    # Height for jump crouch
    upper = int(keypoints[6][0])
    cv2.line(image, (0, upper), (width, upper), (0, 0, 255), 2)
    lower = int(keypoints[12][0])
    cv2.line(image, (0, lower), (width, lower), (0, 0, 255), 2)
    upper_fixed = int(upper - (lower - upper) * threshold_upper)
    lower_fixed = int(lower + (lower - upper) * threshold_lower)

    # Clap threshold
    width_clap_l = int(keypoints[9][1])
    cv2.line(image, (width_clap_l, 0), (width_clap_l, height), (0, 0, 255), 2)
    width_clap_r = int(keypoints[10][1])
    cv2.line(image, (width_clap_r, 0), (width_clap_r, height), (0, 0, 255), 2)   
cv2.imshow("image", image)
cv2.waitKey(0)
