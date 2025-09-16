import tkinter as tk
import serial
import time
import threading

# Connect to Arduino (change COM5 to your port!)
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
time.sleep(2)  # wait for Arduino reset

current_timer = None  # track countdown job
time_left = 0         # time remaining for current light
current_color = ""    # store current light color

def send_command(cmd):
    """Send command to Arduino and handle button states."""
    global current_timer, time_left
    arduino.write(cmd.encode())
    if cmd in ['r', 'g', 'y', 'd']:
        disable_buttons()   # disable buttons while a cycle runs
    elif cmd == 's':
        reset_timer()       # instantly reset timer
        enable_buttons()    # re-enable buttons immediately

def set_light(color):
    """Update GUI lights and start timer based on Arduino color message."""
    global time_left, current_color
    current_color = color  # store current color

    canvas.itemconfig(red_light, fill="red" if color == "RED" else "gray")
    canvas.itemconfig(yellow_light, fill="yellow" if color == "YELLOW" else "gray")
    canvas.itemconfig(green_light, fill="green" if color == "GREEN" else "gray")

    # Set timer duration based on color
    if color == "RED":
        time_left = 5
        start_timer()
    elif color == "GREEN":
        time_left = 5
        start_timer()
    elif color == "YELLOW":
        time_left = 2
        start_timer()
    elif color == "OFF":
        reset_timer()
        enable_buttons()

def start_timer():
    """Initialize countdown for the current light."""
    global current_timer
    if current_timer:
        root.after_cancel(current_timer)
    lbl_timer.config(text=f"{current_color}: {time_left}s left")  # show initial time
    current_timer = root.after(1000, countdown)

def countdown():
    """Update timer label every second until 0, showing color."""
    global time_left, current_timer
    if time_left > 0:
        time_left -= 1
        lbl_timer.config(text=f"{current_color}: {time_left}s left")
        current_timer = root.after(1000, countdown)
    else:
        lbl_timer.config(text="Waiting...")
        current_timer = None

def reset_timer():
    """Stop and reset the timer immediately."""
    global current_timer, time_left, current_color
    if current_timer:
        root.after_cancel(current_timer)
        current_timer = None
    time_left = 0
    current_color = ""
    lbl_timer.config(text="Waiting...")

def read_from_arduino():
    """Background thread to read messages from Arduino."""
    while True:
        try:
            line = arduino.readline().decode().strip()
            if line in ["RED", "YELLOW", "GREEN", "OFF"]:
                set_light(line)
        except:
            pass

def disable_buttons():
    btn_red.config(state="disabled")
    btn_yellow.config(state="disabled")
    btn_green.config(state="disabled")
    btn_default_mode.config(state="disabled")

def enable_buttons():
    btn_red.config(state="normal")
    btn_yellow.config(state="normal")
    btn_green.config(state="normal")
    btn_default_mode.config(state="normal")

# Start background thread to read Arduino messages
threading.Thread(target=read_from_arduino, daemon=True).start()

# ---------------- Tkinter GUI ---------------- #
root = tk.Tk()
root.title("Traffic Light Controller")

# Left: traffic light display
canvas = tk.Canvas(root, width=100, height=260, bg="black")
canvas.grid(row=0, column=0, padx=20, pady=20)

# Draw lights (start OFF = gray)
red_light = canvas.create_oval(20, 20, 80, 80, fill="gray")
yellow_light = canvas.create_oval(20, 90, 80, 150, fill="gray")
green_light = canvas.create_oval(20, 160, 80, 220, fill="gray")

# Right: control buttons + timer
frame = tk.Frame(root)
frame.grid(row=0, column=1, padx=20)

btn_red = tk.Button(frame, text="Red", width=10, height=2,
                    command=lambda: send_command('r'))
btn_red.pack(pady=5)

btn_yellow = tk.Button(frame, text="Yellow", width=10, height=2,
                       command=lambda: send_command('y'))
btn_yellow.pack(pady=5)

btn_green = tk.Button(frame, text="Green", width=10, height=2,
                      command=lambda: send_command('g'))
btn_green.pack(pady=5)

btn_default_mode = tk.Button(frame, text="Default Mode", width=10, height=2,
                             command=lambda: send_command('d'))
btn_default_mode.pack(pady=10)

btn_stop = tk.Button(frame, text="STOP", width=10, height=2,
                     bg="red", fg="white", command=lambda: send_command('s'))
btn_stop.pack(pady=10)

# Timer Label
lbl_timer = tk.Label(frame, text="Waiting...", font=("Arial", 14))
lbl_timer.pack(pady=20)

root.mainloop()
