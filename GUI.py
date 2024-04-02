import tkinter as tk
import requests  #imported for python client
from tkinter import ttk  #Imported for updating GUI style
from PIL import Image, ImageTk
import logging
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import datetime
import pytz
from camera import *

# Set up logging with US/Eastern timezone
eastern = pytz.timezone('US/Eastern')

# Root Menu for user registration and login
root = tk.Tk()
root.title("User Login")
#define style
style = ttk.Style(root)
style.theme_use("clam")

#Create a log file to track activities
# Set up logging
logging.basicConfig(
    filename='activity_log.txt',
    level=logging.INFO,
    format='%(message)s',
)


# Function for the log information including date and time and message
def log_activity(message):
  current_time = datetime.now(eastern).strftime('%Y-%m-%d %I:%M:%S %p')
  logging.info(f"{current_time} - {message}")


# Function to move the robot forward through Flask App
def move_forward(currentState, userName):
  currentState.config(text="Current State: Forward")
  log_activity(f"{userName} clicked Forward button.")
  try:
    url_fwd = requests.get("http://192.168.1.28:4444/forward", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_fwd.json()


# Function to move the robot backward through Flask App
def move_backward(currentState, userName):
  currentState.config(text="Current State: Backward")
  log_activity(f"{userName} clicked Backward button.")
  try:
    url_bwd = requests.get("http://192.168.1.28:4444/backward", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_bwd.json()


# Function to move the robot left through Flask App
def move_left(currentState, userName):
  currentState.config(text="Current State: Left")
  log_activity(f"{userName} clicked Left Move button.")
  try:
    url_left = requests.get("http://192.168.1.28:4444/left", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_left.json()


# Function to move the robot right through Flask App
def move_right(currentState, userName):
  currentState.config(text="Current State: Right")
  log_activity(f"{userName} clicked Right Move button.")
  try:
    url_right = requests.get("http://192.168.1.28:4444/right", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_right.json()


# Function to start the robot through Flask App
def move_start(currentState, userName):
  currentState.config(text="Current State: Start")
  log_activity(f"{userName} clicked Start button.")
  try:
    url_start = requests.get("http://192.168.1.28:4444/start", timeout=1)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_start.json()


# Function to stop the robot through Flask App
def move_stop(currentState, userName):
  currentState.config(text="Current State: Stop")
  log_activity(f"{userName} clicked Stop button.")
  try:
    url_stop = requests.get("http://192.168.1.28:4444/stop", timeout=10)
  except requests.exceptions.RequestException:
    currentState.config(text="Current State: No Connection")
  else:
    return url_stop.json()


# Function to show log file directly in a text region. Only show the rows with the username included. One user will not see other user's log information and the same user can see all the log information on record including login and logout.


def show_log_content(text_widget, userName):
  try:
    log_file_path = 'activity_log.txt'
    with open(log_file_path, 'r') as file:
      lines = file.readlines()

    # Display only the lines containing the userName
    log_content = "\n".join(line for line in lines if userName in line)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, log_content)

    # Scroll to the top to show the latest log information
    text_widget.yview(tk.END)
  except Exception as e:
    # Handle file not found or other exceptions
    print()
    messagebox.showerror("Error", f"Error opening log file: {e}")


#Function to log out user.  The logout will send a message to the log file and go back to the root window for login and registration
def exit_logout(firstName, lastName, userName, gui_window,
                loggedin_window):  #Function to exit the program
  activity = f"{userName} has logged out."
  log_activity(activity)
  gui_window.destroy()
  loggedin_window.destroy()
  root.deiconify()


# Function for the GUI including the definations for all the GUI elements and related python client functions. Python client will send a Request GET signal to the FLASK app for robot car movement.
def GUI(firstName, lastName, user_name,
        loggedin_win):  #Function to create GUI after user logged in
  global state_label, user_window
  user_window = tk.Toplevel()
  user_window.title("GUI")
  user_window.geometry("600x400")

  # Create four grid cells as Frame widgets without background colors
  frame1 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    relief=tk.SUNKEN,
                    borderwidth=2)
  frame1.grid(row=0, column=1, padx=2, pady=2)

  frame2 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    relief=tk.SUNKEN,
                    borderwidth=2)
  frame2.grid(row=1, column=1, padx=2, pady=2)

  frame3 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    )
  frame3.grid(row=0, column=0, padx=2, pady=2)

  frame4 = tk.Frame(user_window,
                    width=400,
                    height=200,
                    )
  frame4.grid(row=1, column=0, padx=2, pady=2)

  # Create a frame for direction buttons in the first grid cell
  direction_frame = tk.Frame(frame1)
  direction_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
  # Create a width for all the buttons
  button_width = 3
  # Add direction buttons to the frame
  btn_Label = ttk.Label(direction_frame, text="Direction Control Buttons")
  btn_fwd = ttk.Button(direction_frame,
                       text="↑",
                       command=lambda: move_forward(current_state, user_name),
                       width=button_width)
  btn_bkwd = ttk.Button(
      direction_frame,
      text="↓",
      command=lambda: move_backward(current_state, user_name),
      width=button_width)
  btn_left = ttk.Button(direction_frame,
                        text="←",
                        command=lambda: move_left(current_state, user_name),
                        width=button_width)
  btn_right = ttk.Button(direction_frame,
                         text="→",
                         command=lambda: move_right(current_state, user_name),
                         width=button_width)
  btn_stop = ttk.Button(direction_frame,
                        text="●",
                        command=lambda: move_stop(current_state, user_name),
                        width=button_width,
                        style='Red.TButton')
  btn_start = ttk.Button(direction_frame,
                         text="●",
                         command=lambda: move_start(current_state, user_name),
                         width=button_width,
                         style='Green.TButton')
  btn_Label.grid(row=0, column=0, columnspan=5)

  btn_fwd.grid(row=1, column=2)
  btn_bkwd.grid(row=3, column=2)
  btn_start.grid(row=2, column=1, padx=0)
  btn_stop.grid(row=2, column=3)
  btn_left.grid(row=2, column=0, padx=0)
  btn_right.grid(row=2, column=4)

  # Define the lable for the movement state
  current_state = ttk.Label(direction_frame,
                            text="Current State: No action now")
  current_state.grid(row=4, column=0, columnspan=5)
  # Log frame showing a button to disply the log file
  log_frame = tk.Frame(frame2)
  log_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
  log_Label = ttk.Label(log_frame,
                        text="Log feed information                 ")
  log_Label.grid(row=0, column=0, columnspan=2)
  # Create a scrolled text widget for log display
  log_text = scrolledtext.ScrolledText(log_frame,
                                       wrap=tk.WORD,
                                       width=50,
                                       height=10,
                                       font=('TkDefaultFont', 8))
  log_text.grid(row=1, column=0, columnspan=2, pady=10)

  # Function to update log content periodically
  def update_log_content():
    show_log_content(log_text, user_name)
    log_text.after(
        1000, update_log_content
    )  # Schedule the next update after 1000 milliseconds (1 second)

  # Update the log content when the GUI is created
  show_log_content(log_text, user_name)

  # Start the periodic update
  update_log_content()
  cap = cv.VideoCapture("New_NEW_FIxed.MP4")
  def display_normal_vid():

      while True:
          ret, vd_frame = cap.read()
          if ret:
              pre_process = process(vd_frame)
              pre_process = mask(pre_process)
              left_line, right_line = detect_lines(pre_process)

              perspective, new_frame = predict_turn(vd_frame)

              new_frame = draw_lines(right_line, left_line, new_frame)

              cv.imshow("new", new_frame)


              if cv.waitKey(1) & 0xFF == ord('q'):
                  continue

  # Video feed frame
  video_frame = tk.Canvas(frame3)
  video_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
  video_Label = ttk.Label(video_frame, text="Video feed with image overlay")
  video_Label.grid(row=0, column=0, columnspan=2)
  videoinput1_Label = ttk.Label(video_frame, text="")
  videoinput1_Label.grid(row=1, column=0, columnspan=2)
  videoinput2_Label = ttk.Label(video_frame, text="")
  videoinput2_Label.grid(row=2, column=0, columnspan=2)
  # Blank frame left for future use
  blank_frame = tk.Frame(frame4)
  blank_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
  ogvideo_Label = ttk.Label(blank_frame)
  ogvideo_Label.grid(row=3, column=0, columnspan=2)

  #Create an exit button to quite the program
  exit_button = ttk.Button(
      user_window,
      text="Logout",
      command=lambda: exit_logout(firstName, lastName, user_name, user_window,
                                  loggedin_win))
  exit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=10)
  display_normal_vid()
  root.mainloop()


# Create a custom style for the red stop button
style.configure('Red.TButton', foreground='red')
# Create a custom style for the green start button
style.configure('Green.TButton', foreground='green')

