import tkinter as tk
from tkinter import ttk
import serial
import threading
import winsound
import time

def create_dht_window():
    """Create and return the DHT11 sensor dashboard window."""
    # Serial connection
    ser = serial.Serial('COM3', 9600, timeout=1)
    last_value = ""  # store last line to detect changes
    
    # Tkinter window
    root = tk.Tk()
    root.title("DHT11 Sensor Dashboard")
    root.geometry("1200x700")
    root.configure(bg="#f5f7fa")
    
    # Main container
    main_container = tk.Frame(root, bg="#f5f7fa")
    main_container.pack(fill="both", expand=True, padx=25, pady=20)
    
    # Header
    heading_frame = tk.Frame(main_container, bg="#34495e", relief="flat", bd=0)
    heading_frame.pack(fill="x", pady=(0, 25))
    
    heading = tk.Label(heading_frame, text="🌡️ DHT11 Sensor Monitor",
                       font=("Segoe UI", 26, "bold"),
                       fg="white", bg="#34495e", pady=20)
    heading.pack()
    
    # Status bar
    status_var = tk.StringVar(value="🔄 Initializing connection...")
    status_label = tk.Label(main_container, textvariable=status_var,
                            font=("Segoe UI", 11), fg="#95a5a6", bg="#f5f7fa")
    status_label.pack(pady=(0, 20))
    
    # Cards container
    cards_container = tk.Frame(main_container, bg="#f5f7fa")
    cards_container.pack(expand=True, fill="both", padx=10)
    
    # Variables
    temp_var = tk.StringVar(value="Temp: -- °C")
    hum_var = tk.StringVar(value="Humidity: -- %")
    dp_var = tk.StringVar(value="Dew Point: -- °C")
    rh_var = tk.StringVar(value="RH (calc): -- %")
    hi_var = tk.StringVar(value="Heat Index: -- °C")
    
    def make_card(parent, text_var, color, icon, title):
        """Create modern sensor card."""
        card = tk.Frame(parent, bg="white", relief="solid", bd=0,
                        highlightbackground="#dfe6e9", highlightthickness=1)
    
        # Color accent bar at top
        accent = tk.Frame(card, bg=color, height=4)
        accent.pack(fill="x")
    
        # Content area
        content = tk.Frame(card, bg="white")
        content.pack(expand=True, fill="both", padx=(10, 20), pady=20)
    
        # Title
        title_label = tk.Label(content, text=title,
                               font=("Segoe UI", 11), fg="#7f8c8d", bg="white")
        title_label.pack(anchor="w", pady=(0, 10))
    
        # Icon and value in horizontal layout
        value_frame = tk.Frame(content, bg="white")
        value_frame.pack(fill="x")
    
        icon_label = tk.Label(value_frame, text=icon,
                              font=("Segoe UI", 32), fg=color, bg="white")
        icon_label.pack(side="left", padx=(0, 15))
    
        value_label = tk.Label(value_frame, textvariable=text_var,
                               font=("Segoe UI", 18, "bold"),
                               fg="#2c3e50", bg="white", anchor="w")
        value_label.pack(side="left", fill="x", expand=True)
    
        return card
    
    # Card specifications
    cards_specs = [
        (temp_var, "#e74c3c", "🌡️", "TEMPERATURE"),
        (hum_var, "#3498db", "💧", "HUMIDITY"),
        (hi_var, "#f39c12", "🔥", "HEAT INDEX"),
        (dp_var, "#27ae60", "🌿", "DEW POINT"),
        (rh_var, "#9b59b6", "📊", "RELATIVE HUMIDITY"),
    ]
    
    # Store card references
    cards_list = []
    
    # Create two rows
    top_row = tk.Frame(cards_container, bg="#f5f7fa")
    top_row.pack(fill="both", expand=True, pady=(0, 15))
    
    bottom_row = tk.Frame(cards_container, bg="#f5f7fa")
    bottom_row.pack(fill="both", expand=True)
    
    # Place first 3 cards in top row
    for i in range(3):
        var, color, icon, title = cards_specs[i]
        card = make_card(top_row, var, color, icon, title)
        card.pack(side="left", fill="both", expand=True, padx=8)
        cards_list.append(card)
    
    # Place remaining 2 cards in bottom row with spacers for centering
    spacer_left = tk.Frame(bottom_row, bg="#f5f7fa")
    spacer_left.pack(side="left", fill="both", expand=True)
    
    for i in range(3, 5):
        var, color, icon, title = cards_specs[i]
        card = make_card(bottom_row, var, color, icon, title)
        card.pack(side="left", fill="both", expand=True, padx=8)
        cards_list.append(card)
    
    spacer_right = tk.Frame(bottom_row, bg="#f5f7fa")
    spacer_right.pack(side="left", fill="both", expand=True)
    
    # Assign card references for flash effects
    temp_card = cards_list[0]
    hum_card = cards_list[1]
    hi_card = cards_list[2]
    dp_card = cards_list[3]
    rh_card = cards_list[4]
    
    def update_display(line):
        """Parse Arduino data and update labels."""
        try:
            parts = line.split(",")  # split by commas
            for p in parts:
                p = p.strip()
                if p.startswith("Temp:"):
                    temp_var.set(p)
                    temp_card.configure(bg="#ffebee")
                    root.after(300, lambda: temp_card.configure(bg="white"))
                elif p.startswith("Humidity:"):
                    hum_var.set(p)
                    hum_card.configure(bg="#e3f2fd")
                    root.after(300, lambda: hum_card.configure(bg="white"))
                elif p.startswith("Dew Point:"):
                    dp_var.set(p)
                    dp_card.configure(bg="#e8f5e8")
                    root.after(300, lambda: dp_card.configure(bg="white"))
                elif p.startswith("RH"):
                    rh_var.set(p)
                    rh_card.configure(bg="#f3e5f5")
                    root.after(300, lambda: rh_card.configure(bg="white"))
                elif p.startswith("Heat Index:"):
                    hi_var.set(p)
                    hi_card.configure(bg="#fff3e0")
                    root.after(300, lambda: hi_card.configure(bg="white"))
    
            # Update status with timestamp
            timestamp = time.strftime("%I:%M:%S %p")
            status_var.set(f"✅ Last updated: {timestamp}")
    
        except Exception as e:
            status_var.set("⚠️ Error parsing data")
    
    def read_serial():
        """Continuously read from Arduino and update GUI with beep only if value changes."""
        nonlocal last_value
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line and line != last_value:  # update only when value changes
                    last_value = line
                    update_display(line)
                    winsound.Beep(1000, 150)  # short beep when updated
    
    def start_thread():
        t = threading.Thread(target=read_serial, daemon=True)
        t.start()
    
    def on_closing():
        from tryMenu import open_menu
        """Handle window close event - close serial connection and destroy window."""
        try:
            if ser and ser.is_open:
                ser.close()
                print("Serial connection closed.")
        except Exception as e:
            print(f"Error closing serial: {e}")
        root.destroy()
        open_menu()
    
    # Set the window close protocol
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start background thread
    start_thread()
    
    return root


# Run directly if this file is executed
if __name__ == "__main__":
    root = create_dht_window()
    root.mainloop()
