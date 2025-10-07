import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import threading
import time
import winsound
import re

# Configuration
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
BEEP_FREQUENCY = 1000  # Hz
BEEP_DURATION = 100     # milliseconds

# Distance thresholds (in cm)
VERY_CLOSE = 10
CLOSE = 20
MEDIUM = 40
FAR = 60

# Global variables
ser = None
is_running = False
last_beep_time = 0
root = None
connection_monitor_running = True

# GUI widgets (global references)
distance_label = None
distance_value_label = None
status_label = None
proximity_label = None
log_text = None
canvas = None

def calculate_beep_interval(distance):
    """
    Calculate beep interval based on distance.
    Closer objects = faster beeping
    Returns interval in seconds, or None if too far
    """
    if distance < VERY_CLOSE:
        return 0.02  # Very fast beeping (10ms interval - extremely rapid)
    elif distance < CLOSE:
        return 0.5  # Fast beeping
    elif distance < MEDIUM:
        return 0.7  # Medium beeping
    elif distance < FAR:
        return 0.8  # Slow beeping
    else:
        return None  # No beeping

def get_proximity_status(distance):
    """Get proximity status text and color based on distance"""
    if distance < VERY_CLOSE:
        return "VERY CLOSE!", "#FF0000", "#FFE0E0"
    elif distance < CLOSE:
        return "Close", "#FF6600", "#FFE8D0"
    elif distance < MEDIUM:
        return "Medium", "#FFAA00", "#FFF4D0"
    elif distance < FAR:
        return "Far", "#00AA00", "#E0FFE0"
    else:
        return "Out of Range", "#666666", "#F0F0F0"

def log_message(message):
    """Add message to log with timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {message}\n")
    log_text.see(tk.END)

def update_visual_indicator(distance):
    """Update the visual distance indicator bar"""
    canvas.delete("all")
    
    # Calculate bar width (max 400px for 100cm)
    max_distance = 100
    bar_width = min(400, (distance / max_distance) * 400)
    
    # Determine color based on proximity
    if distance < VERY_CLOSE:
        color = "#FF0000"
    elif distance < CLOSE:
        color = "#FF6600"
    elif distance < MEDIUM:
        color = "#FFAA00"
    elif distance < FAR:
        color = "#00AA00"
    else:
        color = "#666666"
    
    # Draw background
    canvas.create_rectangle(0, 0, 400, 30, fill="#E0E0E0", outline="#999999")
    
    # Draw distance bar
    canvas.create_rectangle(0, 0, bar_width, 30, fill=color, outline="")
    
    # Draw threshold markers
    for threshold, label in [(VERY_CLOSE, "10"), (CLOSE, "20"), (MEDIUM, "40"), (FAR, "60")]:
        x = (threshold / max_distance) * 400
        canvas.create_line(x, 0, x, 30, fill="white", width=2)
        canvas.create_text(x, 35, text=label, font=("Arial", 8))

def read_serial():
    """Read data from serial port in a separate thread"""
    global ser, is_running, last_beep_time
    
    while is_running:
        try:
            if ser and ser.in_waiting > 0:
                # Read line from Arduino
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Extract distance in cm using regex
                match = re.search(r'Distance:\s*([\d.]+)\s*cm', line)
                
                if match:
                    distance = float(match.group(1))
                    current_time = time.time()
                    
                    # Update GUI in main thread
                    root.after(0, update_distance_display, distance)
                    
                    # Calculate beep interval based on distance
                    beep_interval = calculate_beep_interval(distance)
                    
                    # Beep if within range (always enabled)
                    if beep_interval is not None:
                        if current_time - last_beep_time >= beep_interval:
                            try:
                                winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION)
                                last_beep_time = current_time
                                distance_inches = distance * 0.393701
                                root.after(0, log_message, f"Distance: {distance:.2f} cm / {distance_inches:.2f} in - BEEP!")
                            except:
                                pass  # Ignore beep errors
                    
            time.sleep(0.01)  # Small delay to prevent CPU overload
            
        except Exception as e:
            root.after(0, log_message, f"Error reading serial: {e}")
            time.sleep(0.1)

def update_distance_display(distance):
    """Update the distance display in GUI"""
    distance_inches = distance * 0.393701
    distance_value_label.config(text=f"{distance:.2f} cm / {distance_inches:.2f} in")
    
    # Update proximity status
    status_text, fg_color, bg_color = get_proximity_status(distance)
    proximity_label.config(text=status_text, fg=fg_color, bg=bg_color)
    
    # Update visual indicator
    update_visual_indicator(distance)

def connect_serial():
    """Connect to Arduino"""
    global ser, is_running
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        
        is_running = True
        
        # Start reading thread
        thread = threading.Thread(target=read_serial, daemon=True)
        thread.start()
        
        # Update GUI
        root.after(0, lambda: status_label.config(text="Status: Connected", fg="#00AA00"))
        root.after(0, lambda: log_message("Connected successfully!"))
        
        return True
        
    except serial.SerialException:
        return False

def disconnect_serial():
    """Disconnect from Arduino"""
    global ser, is_running
    
    is_running = False
    time.sleep(0.1)  # Wait for thread to finish
    
    if ser and ser.is_open:
        ser.close()
    
    # Update GUI
    root.after(0, lambda: status_label.config(text="Status: Disconnected", fg="#FF6600"))
    root.after(0, lambda: distance_value_label.config(text="-- cm / -- in"))
    root.after(0, lambda: proximity_label.config(text="Not Connected", fg="#666666", bg="#F0F0F0"))
    
    # Clear visual indicator
    root.after(0, lambda: canvas.delete("all"))
    root.after(0, lambda: canvas.create_rectangle(0, 0, 400, 30, fill="#E0E0E0", outline="#999999"))

def monitor_connection():
    """Monitor Arduino connection status automatically"""
    global ser, connection_monitor_running
    
    while connection_monitor_running:
        try:
            # Check if we're currently connected
            if ser is None or not ser.is_open:
                # Try to connect
                if connect_serial():
                    root.after(0, lambda: log_message(f"Arduino detected on {SERIAL_PORT}"))
            else:
                # Check if connection is still alive
                try:
                    # Try to read the port status
                    if not ser.is_open:
                        raise serial.SerialException("Port closed")
                except:
                    # Connection lost
                    root.after(0, lambda: log_message("Arduino disconnected"))
                    disconnect_serial()
            
            time.sleep(2)  # Check every 2 seconds
            
        except Exception as e:
            time.sleep(2)  # Wait before retrying

def on_closing():
    """Handle window closing"""
    global is_running, connection_monitor_running
    
    connection_monitor_running = False
    is_running = False
    time.sleep(0.2)  # Wait for threads to finish
    if ser and ser.is_open:
        ser.close()
    root.destroy()

def create_gui():
    """Create the main GUI"""
    global root, distance_label, distance_value_label, status_label, proximity_label
    global log_text, canvas
    
    root = tk.Tk()
    root.title("Ultrasonic Proximity Monitor")
    root.geometry("600x900")
    root.resizable(True, True)
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Header Frame
    header_frame = tk.Frame(root, bg="#2C3E50", height=80)
    header_frame.pack(fill=tk.X, padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(header_frame, text="🔊 Ultrasonic Proximity Monitor", 
                          font=("Arial", 20, "bold"), bg="#2C3E50", fg="white")
    title_label.pack(pady=20)
    
    # Main content frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
    
    # Status section
    status_frame = tk.Frame(main_frame, bg="white")
    status_frame.pack(fill=tk.X, pady=(0, 8))
    
    status_label = tk.Label(status_frame, text="Status: Disconnected", 
                           font=("Arial", 12), fg="#FF6600", bg="white")
    status_label.pack()
    
    # Distance display section
    distance_frame = tk.Frame(main_frame, bg="#F8F9FA", relief=tk.RIDGE, borderwidth=2)
    distance_frame.pack(fill=tk.X, pady=(0, 8), padx=10)
    
    distance_label = tk.Label(distance_frame, text="Distance:", 
                             font=("Arial", 12), bg="#F8F9FA")
    distance_label.pack(pady=(8, 3))
    
    distance_value_label = tk.Label(distance_frame, text="-- cm / -- in", 
                                   font=("Arial", 24, "bold"), bg="#F8F9FA", fg="#2C3E50")
    distance_value_label.pack(pady=(0, 8))
    
    # Proximity status
    proximity_label = tk.Label(distance_frame, text="Not Connected", 
                              font=("Arial", 14, "bold"), fg="#666666", bg="#F0F0F0",
                              relief=tk.RAISED, borderwidth=2, padx=15, pady=8)
    proximity_label.pack(pady=(0, 10))
    
    # Visual indicator
    indicator_frame = tk.Frame(main_frame, bg="white")
    indicator_frame.pack(fill=tk.X, pady=(0, 8))
    
    tk.Label(indicator_frame, text="Visual Distance Indicator:", 
            font=("Arial", 11), bg="white").pack(anchor=tk.W)
    
    canvas = tk.Canvas(indicator_frame, width=400, height=30, bg="white", highlightthickness=0)
    canvas.pack(pady=(5, 0))
    canvas.create_rectangle(0, 0, 400, 30, fill="#E0E0E0", outline="#999999")
    
    # Info section
    info_frame = tk.LabelFrame(main_frame, text="Distance Ranges", 
                              font=("Arial", 10, "bold"), bg="white", fg="#2C3E50")
    info_frame.pack(fill=tk.X, pady=(0, 8))
    
    ranges = [
        ("< 10 cm", "Very Close - Very Fast Beeping", "#FF0000"),
        ("< 20 cm", "Close - Fast Beeping", "#FF6600"),
        ("< 40 cm", "Medium - Medium Beeping", "#FFAA00"),
        ("< 60 cm", "Far - Slow Beeping", "#00AA00"),
        ("> 60 cm", "Out of Range - No Beeping", "#666666")
    ]
    
    for dist, desc, color in ranges:
        range_frame = tk.Frame(info_frame, bg="white")
        range_frame.pack(fill=tk.X, padx=8, pady=1)
        
        tk.Label(range_frame, text="●", font=("Arial", 12), 
                fg=color, bg="white").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(range_frame, text=f"{dist}:", font=("Arial", 9, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(range_frame, text=desc, font=("Arial", 9), 
                bg="white", fg="#555555").pack(side=tk.LEFT)
    
    # Log section
    log_frame = tk.LabelFrame(main_frame, text="Activity Log", 
                             font=("Arial", 11, "bold"), bg="white", fg="#2C3E50")
    log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
    
    log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Consolas", 9),
                                         bg="#F8F9FA", fg="#2C3E50", relief=tk.SUNKEN, wrap=tk.WORD)
    log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Initial log message
    log_message("Application started. Monitoring for Arduino connection...")
    log_message(f"Configured for {SERIAL_PORT} at {BAUD_RATE} baud")
    
    # Start connection monitoring thread
    monitor_thread = threading.Thread(target=monitor_connection, daemon=True)
    monitor_thread.start()
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    return root

def main():
    """Main function to start the GUI"""
    gui = create_gui()
    gui.mainloop()

if __name__ == "__main__":
    main()
