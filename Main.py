import tkinter as tk
from tkinter import filedialog
import time
import pynput.mouse
from pynput.mouse import Controller, Button
import json
import webbrowser

# Global variable to hold recorded events and the current file
recorded_events = []
current_file = None  # To hold the currently selected file for playback

# Initialize mouse controller for playback
mouse_controller = Controller()

# Define functions for the buttons
def on_record():
    root.focus_force()  # Keep the window in focus
    record_button.config(text="Stop", command=on_stop)
    recorded_events.clear()  # Clear any previous recordings
    
    # Start the listener to record mouse events
    global listener
    listener = pynput.mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()

def on_stop():
    root.focus_force()  # Keep the window in focus
    record_button.config(text="Record", command=on_record)
    
    # Stop the listener
    listener.stop()
    
    # Open file dialog to save the recording
    save_recording()

def on_move(x, y):
    recorded_events.append(('move', x, y, time.time()))  # Record mouse movement with timestamp

def on_click(x, y, button, pressed):
    if pressed:
        recorded_events.append(('click', x, y, time.time(), button.name))  # Record mouse click with timestamp

def save_recording():
    root.focus_force()  # Keep the window in focus
    file_path = filedialog.asksaveasfilename(defaultextension=".MHCK", filetypes=[("MHCK Files", "*.MHCK"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                json.dump(recorded_events, file)
        except Exception as e:
            print(f"Error saving file: {e}")

def load_file():
    """Load an existing .MHCK file and update the label."""
    global current_file
    root.focus_force()  # Keep the window in focus
    file_path = filedialog.askopenfilename(filetypes=[("MHCK Files", "*.MHCK"), ("All Files", "*.*")])
    if file_path:
        current_file = file_path
        selected_file_label.config(text=f"Selected File: {file_path}")
        print(f"Loaded file: {file_path}")

def play_recording():
    global current_file
    root.focus_force()  # Keep the window in focus
    if current_file:
        try:
            with open(current_file, 'r') as file:
                events = json.load(file)
            
            start_time = events[0][3]  # Get initial timestamp
            for event in events:
                event_type = event[0]
                if event_type == 'move':
                    _, x, y, timestamp = event
                    time.sleep(timestamp - start_time)  # Wait for the time difference
                    mouse_controller.position = (x, y)
                elif event_type == 'click':
                    _, x, y, timestamp, button_name = event
                    time.sleep(timestamp - start_time)
                    mouse_controller.position = (x, y)
                    button = Button.left if button_name == 'left' else Button.right
                    mouse_controller.click(button)
                start_time = timestamp  # Update the start time
        except Exception as e:
            print(f"Error playing file: {e}")
    else:
        print("No file selected for playback!")

def open_options():
    """Open an options tab with five buttons."""
    options_window = tk.Toplevel(root)
    options_window.title("Options")
    options_window.geometry("300x200")
    
    # Create five buttons
    for i in range(1, 6):
        option_button = tk.Button(options_window, text=f"Option {i}", command=lambda: print("WIP"))
        option_button.pack(pady=5)

def open_help():
    """Open an HTML help file in the default web browser."""
    help_file_path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
    if help_file_path:
        webbrowser.open(help_file_path)

# Create the main window
root = tk.Tk()
root.title("Mouse Recorder & Player")

# Set window size
root.geometry("500x300")

# Create a label to display the currently selected file
selected_file_label = tk.Label(root, text="Selected File: None", bg="lightgray", anchor="w")
selected_file_label.pack(fill="x", padx=10, pady=5)

# Create a toolbar frame (top section)
toolbar = tk.Frame(root, bg="lightgray", height=50)
toolbar.pack(side="top", fill="x")

# Set Button 1 to load an existing file
button1 = tk.Button(toolbar, text="Load File", command=load_file)
button1.pack(side="left", padx=10)

# Set Button 3 to open the Options tab
button3 = tk.Button(toolbar, text="Options", command=open_options)
button3.pack(side="left", padx=10)

# Set Button 4 to open a Help HTML file
button4 = tk.Button(toolbar, text="Help", command=open_help)
button4.pack(side="left", padx=10)

# Create the main action frame (where Record and Play buttons are placed)
action_frame = tk.Frame(root)
action_frame.pack(pady=20)

# Create the "Record" button
record_button = tk.Button(action_frame, text="Record", command=on_record, width=12, height=2)
record_button.pack(side="left", padx=20)

# Create the "Play" button
play_button = tk.Button(action_frame, text="Play", command=play_recording, width=12, height=2)
play_button.pack(side="left", padx=20)

# Start the main GUI loop
root.mainloop()
