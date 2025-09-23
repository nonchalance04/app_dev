import tkinter as tk
import serial
import time


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
arduino_connection = None  # Connection to Arduino
is_running = False         # Is the traffic light running
timer_label = None         # Shows countdown timer
status_label = None        # Shows current status
main_window = None         # Main program window

# Current light sequence info
light_sequence = []        # array that has a value of colors (like ['RED', 'YELLOW', 'GREEN'])
current_light_number = 0   # index for the array light_sequence
should_repeat = False      # repeat sequence
seconds_left = 0          # remaining time the light will be on
timer_id = None           # ID for the countdown timer

# =============================================================================
# ARDUINO CONNECTION
# =============================================================================
def connect_to_arduino():
    # Try to connect to Arduino on COM3
    global arduino_connection
    try:
        arduino_connection = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)
        print("Arduino connected successfully!")
    except:
        print("Could not find Arduino")
        arduino_connection = None

def send_to_arduino(command):
    """Send a command to Arduino (like 'R' for Red, 'G' for Green)"""
    if arduino_connection:
        try:
            arduino_connection.write(command.encode())
        except:
            print("Error: Could not send command to Arduino")

# =============================================================================
# LIGHT TIMING SETTINGS
# =============================================================================
# Dictionary
# How long each light stays on (in seconds)
LIGHT_DURATIONS = {
    'R': 5,  # Red light = 5 seconds
    'Y': 2,  # Yellow light = 2 seconds  
    'G': 5   # Green light = 5 seconds
}

# Names to show on screen
LIGHT_NAMES = {
    'R': 'RED',
    'Y': 'YELLOW', 
    'G': 'GREEN'
}

# =============================================================================
# TIMER AND DISPLAY FUNCTIONS
# =============================================================================
def update_timer_display():
    """Update the timer display on screen"""
    if is_running:
        timer_label.config(text=f"Time Left: {seconds_left} seconds")
    else:
        timer_label.config(text="Time Left: 0 seconds")

def update_status_display(message):
    """Update the status message on screen"""
    status_label.config(text=f"Status: {message}")

def enable_all_buttons():
    """Turn on all the control buttons"""
    for button in all_buttons:
        button.config(state='normal')

def disable_control_buttons():
    """Turn off control buttons (but keep STOP button on)"""
    red_button.config(state='disabled')
    yellow_button.config(state='disabled')
    green_button.config(state='disabled')
    auto_button.config(state='disabled')
    stop_button.config(state='normal')

# =============================================================================
# MAIN TRAFFIC LIGHT LOGIC
# =============================================================================
def start_light_sequence(sequence, repeat=False):
    """Start showing a sequence of lights"""
    global is_running, light_sequence, current_light_number, should_repeat
    
    # Don't start if already running
    if is_running:
        return
    
    # Set up the sequence
    is_running = True
    light_sequence = sequence.copy()
    current_light_number = 0
    should_repeat = repeat
    
    # Disable buttons while running
    disable_control_buttons()
    
    # Start the first light
    show_current_light()

def show_current_light():
    """Turn on the current light and start its timer"""
    global seconds_left
    
    if not is_running:
        return
    
    # Get info about current light
    light_code = light_sequence[current_light_number]
    light_name = LIGHT_NAMES[light_code]
    
    # Send command to Arduino
    send_to_arduino(light_code)
    
    # Update display
    update_status_display(f"{light_name} LIGHT ON")
    
    # Set timer for this light
    seconds_left = LIGHT_DURATIONS[light_code]
    update_timer_display()
    
    # Start countdown
    start_countdown()

def start_countdown():
    """Start the countdown timer for current light"""
    global timer_id
    if main_window:
        timer_id = main_window.after(1000, countdown_tick)  # Call countdown_tick in 1 second

def countdown_tick():
    """Called every second to update the countdown"""
    global seconds_left, timer_id
    
    if not is_running:
        return
    
    # Reduce time by 1 second
    seconds_left -= 1
    update_timer_display()
    
    if seconds_left <= 0:
        # Time's up for this light - move to next
        go_to_next_light()
    else:
        # Schedule next countdown tick
        timer_id = main_window.after(1000, countdown_tick)

def go_to_next_light():
    """Move to the next light in the sequence"""
    global current_light_number
    
    current_light_number += 1
    
    # Check if we've finished all lights
    if current_light_number >= len(light_sequence):
        if should_repeat:
            # Start over from beginning
            current_light_number = 0
            show_current_light()
        else:
            # Sequence finished - stop everything
            stop_all_lights()
    else:
        # Show next light
        show_current_light()

def stop_all_lights():
    """Stop everything and turn off all lights"""
    global is_running, timer_id, seconds_left
    
    is_running = False
    
    # Cancel any running timer
    if timer_id and main_window:
        try:
            main_window.after_cancel(timer_id)
        except:
            pass
    timer_id = None
    
    # Reset timer value to 0
    seconds_left = 0
    
    # Turn off lights on Arduino
    send_to_arduino('S')  # 'S' = Stop command
    
    # Update display
    update_status_display("All Lights OFF")
    update_timer_display()
    
    # Turn buttons back on
    enable_all_buttons()

# =============================================================================
# BUTTON FUNCTIONS (What happens when you click each button)
# =============================================================================
def red_button_clicked():
    """RED button: Start with Red, then Yellow, then Green (repeats forever)"""
    start_light_sequence(['R', 'Y', 'G'], repeat=True)

def yellow_button_clicked():
    """YELLOW button: Start with Yellow, then Green, then Red (repeats forever)"""
    start_light_sequence(['Y', 'G', 'R'], repeat=True)

def green_button_clicked():
    """GREEN button: Start with Green, then Red, then Yellow (repeats forever)"""
    start_light_sequence(['G', 'R', 'Y'], repeat=True)

def default_button_clicked():
    """DEFAULT button: Normal traffic light sequence (repeats forever)"""
    start_light_sequence(['R', 'G', 'Y'], repeat=True)

def stop_button_clicked():
    """STOP button: Stop all lights"""
    stop_all_lights()

# =============================================================================
# CREATE THE WINDOW AND BUTTONS
# =============================================================================


    
def create_main_window():
    """Create the main program window with all buttons"""
    global timer_label, status_label, main_window
    global red_button, yellow_button, green_button, auto_button, stop_button, all_buttons

    from tryMenu import open_menu

    # Create main window
    window = tk.Tk()
    main_window = window
    window.title("Simple Traffic Light Controller")
    window.geometry("350x500")
    window.configure(bg='lightgray')

    def back_to_main():
        window.destroy()
        open_menu()
    def on_close():
        window.destroy()
        open_menu.deiconify()

    window.protocol("WM_DELETE_WINDOW", back_to_main)

    back_button = tk.Button(window, text="Back", command=back_to_main).pack(pady=10)

    
    # Title
    title_label = tk.Label(window, text="Traffic Light Controller", 
                          font=("Arial", 16, "bold"),
                          bg='lightgray')
    title_label.pack(pady=20)
    
    # Create all buttons
    red_button = tk.Button(window, text="RED", 
                          bg="red", fg="white", font=("Arial", 11, "bold"),
                          width=25, height=2, command=red_button_clicked)
    red_button.pack(pady=5)
    
    yellow_button = tk.Button(window, text="YELLOW", 
                             bg="orange", fg="black", font=("Arial", 11, "bold"),
                             width=25, height=2, command=yellow_button_clicked)
    yellow_button.pack(pady=5)
    
    green_button = tk.Button(window, text="GREEN", 
                            bg="green", fg="white", font=("Arial", 11, "bold"),
                            width=25, height=2, command=green_button_clicked)
    green_button.pack(pady=5)
    
    auto_button = tk.Button(window, text="DEFAULT MODE", 
                           bg="blue", fg="white", font=("Arial", 11, "bold"),
                           width=25, height=2, command=default_button_clicked)
    auto_button.pack(pady=5)
    
    stop_button = tk.Button(window, text="STOP", 
                           bg="darkred", fg="white", font=("Arial", 11, "bold"),
                           width=25, height=2, command=stop_button_clicked)
    stop_button.pack(pady=5)
    
    # Status display
    status_label = tk.Label(window, text="Status: Ready to Start", 
                           font=("Arial", 12), bg='lightgray')
    status_label.pack(pady=20)
    
    # Timer display
    timer_label = tk.Label(window, text="Timer: Not Running", 
                          font=("Arial", 14, "bold"), 
                          fg="blue", bg='lightgray')
    timer_label.pack(pady=10)
    
    # Keep track of all buttons for easy enable/disable
    all_buttons = [red_button, yellow_button, green_button, auto_button, stop_button]
    
    return window

# =============================================================================
# MAIN PROGRAM STARTS HERE
# =============================================================================
if __name__ == "__main__":
    print("Starting Traffic Light Controller...")
    
    # Connect to Arduino
    connect_to_arduino()
    
    # Create the window
    main_window = create_main_window()

    
    # Start the program
    main_window.mainloop()
    
    # Clean up when program ends
    if arduino_connection:
        arduino_connection.close()
        print("Arduino disconnected. Program ended.")