import cv2
import os
import tkinter as tk
from tkinter import simpledialog, Entry, Label, Button, Frame, Checkbutton, IntVar

def draw_ruler_and_grid(img, draw_grid, step=50):
    height, width, _ = img.shape
    ruler_width = 40  # Width of the ruler area

    # Create space for ruler on the left and top
    img_with_ruler = cv2.copyMakeBorder(img, ruler_width, 0, ruler_width, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    # Draw horizontal and vertical rulers
    for i in range(0, width + 1, step):
        # Vertical ruler
        cv2.line(img_with_ruler, (ruler_width + i, 0), (ruler_width + i, ruler_width), (0, 0, 0), 2)
        cv2.putText(img_with_ruler, str(i), (ruler_width + i, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    for i in range(0, height + 1, step):
        # Horizontal ruler
        cv2.line(img_with_ruler, (0, ruler_width + i), (ruler_width, ruler_width + i), (0, 0, 0), 2)
        cv2.putText(img_with_ruler, str(i), (10, ruler_width + i + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    # Optional grid based on toggle
    if draw_grid:
        for x in range(0, width, step):
            cv2.line(img_with_ruler, (ruler_width + x, ruler_width), (ruler_width + x, height + ruler_width), (0, 255, 0), 1)
        for y in range(0, height, step):
            cv2.line(img_with_ruler, (ruler_width, ruler_width + y), (width + ruler_width, ruler_width + y), (0, 255, 0), 1)

    return img_with_ruler

def annotate(image_path, keypoints, output_image_path, keypoints_file_path, next_image_callback):
    img = cv2.imread(image_path)
    if img is None:
        print("Image not found:", image_path)
        return

    window = tk.Tk()
    window.title("Keypoint Annotation Tool")
    grid_var = IntVar(value=0)  # Grid is off by default

    def update_image():
        display_img = img.copy()
        for key, (x, y, visibility) in keypoints.items():
            if visibility:
                cv2.circle(display_img, (x, y), radius=6, color=(0, 0, 255), thickness=-1)
                cv2.putText(display_img, key, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        display_img_with_ruler = draw_ruler_and_grid(display_img, grid_var.get() == 1)
        cv2.imshow("Annotated Image", display_img_with_ruler)
        return display_img_with_ruler

    entries = {}
    visibility_vars = {}
    frame = Frame(window)
    frame.pack(side=tk.LEFT, fill=tk.Y)

    for idx, (key, (x, y, visibility)) in enumerate(keypoints.items()):
        Label(frame, text=key).grid(row=idx, column=0, sticky='w')
        ent_x = Entry(frame, width=5)
        ent_y = Entry(frame, width=5)
        ent_x.grid(row=idx, column=1)
        ent_y.grid(row=idx, column=2)
        ent_x.insert(0, str(x))
        ent_y.insert(0, str(y))
        entries[key] = (ent_x, ent_y)

        vis_var = IntVar(value=visibility)
        visibility_vars[key] = vis_var
        cb = Checkbutton(frame, variable=vis_var, command=lambda k=key: [on_test(), toggle_entry_state(k)])
        cb.grid(row=idx, column=3)

    def toggle_entry_state(key):
        if visibility_vars[key].get():
            entries[key][0].config(state='normal')
            entries[key][1].config(state='normal')
        else:
            entries[key][0].config(state='disabled')
            entries[key][1].config(state='disabled')
        entries[key][0].xview_moveto(1)
        entries[key][1].xview_moveto(1)

    def on_test():
        for key in keypoints:
            x, y, _ = keypoints[key]
            visibility = visibility_vars[key].get()
            try:
                keypoints[key] = (int(entries[key][0].get()), int(entries[key][1].get()), visibility)
            except ValueError:
                pass
        update_image()

    def on_save():
        annotated_image = update_image()
        cv2.imwrite(output_image_path, annotated_image)
        with open(keypoints_file_path, 'w') as file:
            for name, (x, y, visibility) in keypoints.items():
                file.write(f"{name}: ({x}, {y}, {visibility})\n")
        print("Annotation saved.")
        window.destroy()

    def on_save_and_next():
        on_save()
        next_image_callback()

    button_frame = Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=10, expand=True)

    # GUI elements for grid toggle
    grid_check = Checkbutton(window, text="Grid", variable=grid_var, command=update_image)
    grid_check.pack(side=tk.TOP, padx=10, pady=5)

    test_button = Button(button_frame, text="Test", command=on_test)
    test_button.pack(side=tk.TOP, padx=10, pady=5)

    save_button = Button(button_frame, text="Save", command=on_save)
    save_button.pack(side=tk.TOP, padx=10, pady=5)

    save_next_button = Button(button_frame, text="Save and Next", command=on_save_and_next)
    save_next_button.pack(side=tk.TOP, padx=10, pady=5)

    # Initialize the entry fields' state based on the visibility checkbox
    for key in keypoints:
        toggle_entry_state(key)

    update_image()
    window.mainloop()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = simpledialog.askstring("Input", "Enter the name of the folder:")
    if not folder_name:
        return

    base_path = os.path.join(current_dir, folder_name)
    frame_num = simpledialog.askstring("Input", "Enter starting frame number (e.g., 0010):")
    if not frame_num:
        frame_num = "0000"

    def next_image():
        nonlocal frame_num
        frame_num = f"{int(frame_num) + 1:04d}"
        image_path = os.path.join(base_path, f"Frame/frame_{frame_num}.jpg")
        output_image_path = os.path.join(base_path, f"Output/frame_{frame_num}.jpg")
        keypoints_file_path = os.path.join(base_path, f"Keypoints/frame_{frame_num}.txt")
        if os.path.exists(image_path):
            annotate(image_path, keypoints, output_image_path, keypoints_file_path, next_image)
        else:
            print("No more images to load.")

    image_path = os.path.join(base_path, f"Frame/frame_{frame_num}.jpg")
    output_image_path = os.path.join(base_path, f"Output/frame_{frame_num}.jpg")
    keypoints_file_path = os.path.join(base_path, f"Keypoints/frame_{frame_num}.txt")

    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    os.makedirs(os.path.dirname(keypoints_file_path), exist_ok=True)

    keypoints = {
        "nose": (744, 190, 1),
        "left_hand": (430, 280, 1),
        "left_elbow": (550, 330, 1),
        "left_shoulder": (655, 255, 1),
        "right_shoulder": (810, 265, 1),
        "right_elbow": (920, 330, 1),
        "right_hand": (1050, 300, 1),
        "left_hip": (640, 510, 1),
        "right_hip": (795, 520, 1),
        "left_knee": (0, 0, 0),
        "left_foot": (0, 0, 0),
        "right_knee": (0, 0, 0),
        "right_foot": (0, 0, 0)
    }

    annotate(image_path, keypoints, output_image_path, keypoints_file_path, next_image)

if __name__ == "__main__":
    main()