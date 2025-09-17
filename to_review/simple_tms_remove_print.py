import tkinter as tk
import serial
import time
import threading

# Simple variables (like global variables in basic programming)
arduino = None
running = False
status_text = None
timer_text = None

# Button references for enabling/disabling
red_btn = None
yellow_btn = None
green_btn = None
auto_btn = None
stop_btn = None

# Try to connect to Arduino
def setup_arduino():
    global arduino
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)  # Change COM3 to your port
        time.sleep(2)
    except:
        print("No Arduino found")

# Send simple commands to Arduino
def send_command(command):
    global arduino
    if arduino:
        try:
            arduino.write(command.encode())
        except:
            print("Error sending to Arduino")

def update_timer(time_left):
    global timer_text
    if time_left > 0:
        timer_text.config(text=f"Timer: {time_left:.1f}s left")
    else:
        timer_text.config(text="Timer: --")

# Function to disable all color buttons except stop
def disable_color_buttons():
    global red_btn, yellow_btn, green_btn, auto_btn, stop_btn
    red_btn.config(state='disabled')
    yellow_btn.config(state='disabled')
    green_btn.config(state='disabled')
    auto_btn.config(state='disabled')
    stop_btn.config(state='normal')  # Keep stop button enabled

# Function to enable all buttons
def enable_all_buttons():
    global red_btn, yellow_btn, green_btn, auto_btn, stop_btn
    red_btn.config(state='normal')
    yellow_btn.config(state='normal')
    green_btn.config(state='normal')
    auto_btn.config(state='normal')
    stop_btn.config(state='normal')

# Simple function to wait and count down
def wait_with_timer(seconds, light_name):
    global running
    # update_status(light_name + " LIGHT")
    status_text.config(text="Status: " + light_name + " LIGHT")

    total_steps = int(seconds)  # 1 step per second

    for step in range(total_steps + 1):
        if not running:  # If someone pressed stop
            return False

        time_left = seconds - step
        update_timer(time_left)
        if step < total_steps:
            time.sleep(1.0)
    
    return True  # Completed successfully

# --- Simple helpers to run light sequences ---
# How long each light stays on (in seconds)
DURATIONS = {'R': 5, 'Y': 2, 'G': 5}

# Pretty names for display
NAMES = {'R': 'RED', 'Y': 'YELLOW', 'G': 'GREEN'}

def run_single_cycle(order, prefix=""):
    """Run one cycle like ['R','Y','G']. Returns False if stopped."""
    for code in order:
        send_command(code)
        name = f"{prefix}{NAMES.get(code, code)}"
        if not wait_with_timer(DURATIONS.get(code, 1), name):
            return False
    return True

def start_sequence(order, auto=False):
    """Start a sequence in the background. If auto=True, it repeats until stopped."""
    global running
    if running:
        return
    running = True
    
    # Disable other buttons when a sequence starts
    disable_color_buttons()

    def worker():
        global running
        if auto:
            # Repeat until stop
            while running and run_single_cycle(order, prefix="LOOP - "):
                if not running:
                    break
        else:
            run_single_cycle(order)
        running = False
        update_timer(0)
        # Re-enable all buttons when sequence completes
        enable_all_buttons()
        if status_text:
            status_text.config(text="Status: Ready")

    threading.Thread(target=worker, daemon=True).start()

# RED BUTTON: Start with red, then yellow, then green (LOOPS until stopped)
def red_button():
    # RED -> YELLOW -> GREEN (repeats forever)
    start_sequence(['R', 'Y', 'G'], auto=True)

# YELLOW BUTTON: Start with yellow, then green, then red (LOOPS until stopped)
def yellow_button():
    # YELLOW -> GREEN -> RED (repeats forever)
    start_sequence(['Y', 'G', 'R'], auto=True)

# GREEN BUTTON: Start with green, then red, then yellow (LOOPS until stopped)
def green_button():
    # GREEN -> RED -> YELLOW (repeats forever)
    start_sequence(['G', 'R', 'Y'], auto=True)

# DEFAULT BUTTON: Keep repeating red -> yellow -> green forever
def default_button():
    # Repeat RED -> YELLOW -> GREEN until stopped (DEFAULT MODE)
    start_sequence(['R', 'Y', 'G'], auto=True)

# STOP BUTTON: Stop everything
def stop_button():
    global running
    running = False
    send_command('S')
    status_text.config(text="STOPPED")
    update_timer(0)
    # Re-enable all buttons when stopped
    enable_all_buttons()

# Create the window and buttons
def create_window():
    global status_text, timer_text, red_btn, yellow_btn, green_btn, auto_btn, stop_btn
    
    # Make the main window
    window = tk.Tk()
    window.title("Traffic Light Controller")
    window.geometry("400x550")
    window.configure()
    
    # Title at the top
    title = tk.Label(window, text="Traffic Monitoring System", 
                    font=("Arial", 18, "bold")
                    )
    title.pack(pady=20)
    
    # Buttons in a single column with uniform width
    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=10, fill=tk.X)

    red_btn = tk.Button(buttons_frame, text="RED", 
                        bg="red", fg="white",
                        font=("Arial", 12, "bold"), 
                        width=20, height=2,
                        command=red_button)
    red_btn.pack(pady=6)

    yellow_btn = tk.Button(buttons_frame, text="YELLOW", 
                           bg="orange", fg="black",
                           font=("Arial", 12, "bold"), 
                           width=20, height=2,
                           command=yellow_button)
    yellow_btn.pack(pady=6)

    green_btn = tk.Button(buttons_frame, text="GREEN", 
                          bg="green", fg="white",
                          font=("Arial", 12, "bold"), 
                          width=20, height=2,
                          command=green_button)
    green_btn.pack(pady=6)

    auto_btn = tk.Button(buttons_frame, text="DEFAULT MODE", 
                         bg="blue", fg="white",
                         font=("Arial", 12, "bold"), 
                         width=20, height=2,
                         command=default_button)
    auto_btn.pack(pady=6)

    stop_btn = tk.Button(buttons_frame, text="STOP ALL", 
                         bg="gray", fg="white",
                         font=("Arial", 12, "bold"), 
                         width=20, height=2,
                         command=stop_button)
    stop_btn.pack(pady=6)
    
    # Status and Timer displays
    status_text = tk.Label(window, text="Status: Ready", 
                          font=("Arial", 14), 
                          fg="#333333")
    status_text.pack(pady=20)
    
    timer_text = tk.Label(window, text="Timer: --", 
                         font=("Arial", 16, "bold"), 
                         fg="#0D6EFD")
    timer_text.pack(pady=5)
    
    return window

# Main program starts here
if __name__ == "__main__":
    # Connect to Arduino first
    setup_arduino()
    
    # Create and show the window
    main_window = create_window()
    
    # Start the program
    main_window.mainloop()
    
    # Close Arduino when program ends
    if arduino:
        arduino.close()
        print("Arduino disconnected")