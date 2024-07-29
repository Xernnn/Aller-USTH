import cv2
import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def extract_frames(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return False
    
    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    cap.release()
    print(f"Extracted {frame_count} frames.")
    return True

def browse_video():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Set the initial directory to the script's directory
    initial_dir = os.path.dirname(os.path.abspath(__file__))
    
    video_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select Video File", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if not video_path:
        messagebox.showinfo("Cancelled", "Video selection cancelled.")
        return 
    
    output_folder = simpledialog.askstring("Output Folder", "Enter the folder name for output:")
    if not output_folder:
        messagebox.showinfo("Cancelled", "Output folder name entry cancelled.")
        return 
    
    video_output_dir = os.path.join(initial_dir, output_folder)
    output_image_path = os.path.join(video_output_dir, "Output")
    keypoints_file_path = os.path.join(video_output_dir, f"Keypoints")
    
    os.makedirs(video_output_dir, exist_ok=True)
    os.makedirs(output_image_path, exist_ok=True)
    os.makedirs(keypoints_file_path, exist_ok=True)
    shutil.copy(video_path, video_output_dir)

    frame_output_dir = os.path.join(video_output_dir, "Frame")
    success = extract_frames(video_path, frame_output_dir)
    
    if not success:
        messagebox.showerror("Error", "Failed to process the video.")

if __name__ == "__main__":
    browse_video()
    

