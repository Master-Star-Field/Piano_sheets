import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk
import json

video_path = "vid_1.mp4"
output_folder = "frames"
global rectangles
global n
global Rectangles
global frame_paths

frame_paths = [f"{output_folder}/{f}" for f in os.listdir(output_folder)]
rectangles = []
Rectangles = {}
topx, topy, botx, boty = 0, 0, 0, 0

def create_frames(output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Extract every 20th frame and save it as an image
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_number % 20 == 0:
            cv2.imwrite(f"{output_folder}/frame_{frame_number}.png", frame)
        frame_number += 1

    cap.release()

def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y

def update_sel_rect(event):
    global botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)

def save_selection(event):
    global topx, topy, botx, boty, rectangles
    rectangles.append([topx,  topy,  botx,  boty])
    draw_saved_rectangles()

def draw_saved_rectangles():
    global rectangles
    for rect in rectangles:
        canvas.create_rectangle(rect[0], rect[1], rect[2], rect[3], outline="red", width=3)

def next_frame(event):
    global rectangles, control, frame_paths
    print(rectangles)
    Rectangles[str(n)] = rectangles
    with open('rectangles.json', 'w') as f:
        json.dump(Rectangles, f)
    rectangles = []
    frame = cv2.imread(frame_paths[n])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'frame1/frame_{str(n)}.png', binary)

    window.destroy()



n = 0
for path in frame_paths:
    window = tk.Tk()
    window.title("Select Area")
    img = ImageTk.PhotoImage(Image.open(path))
    window.geometry('%dx%d' % (img.width(), img.height()))
    window.configure(background='grey')

    img = ImageTk.PhotoImage(Image.open(path))
    canvas = tk.Canvas(window, width=img.width(), height=img.height(), borderwidth=0, highlightthickness=0)
    canvas.pack(expand=True)
    window.update()
    canvas.img = img
    canvas.create_image(0, 0, image=img, anchor=tk.NW)

    rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2, 2), fill='', outline='white')

    canvas.bind('<ButtonRelease-1>', save_selection)
    canvas.bind('<Button-1>', get_mouse_posn)
    canvas.bind('<B1-Motion>', update_sel_rect)
    window.bind('n', next_frame)
    n += 1

    window.mainloop()
