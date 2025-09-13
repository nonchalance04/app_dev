import serial
import time

arduino = serial.Serial(port="/dev/pts/3")
time.sleep(2)

print("Press 'r' for Red, 'y' for Yellow, 'g' for Green, 'q' to quit.")

while True:
    cmd = input("Enter command: ").strip().lower()

    if cmd == "q":
        print("Exiting...")
        break
    elif cmd in ["r", "y", "g"]:
        arduino.write(cmd.encode())
        print(f"Send '{cmd}' to Arduino")
    else:
        print("Invalid input. Use 'r', 'y', 'g', or 'q'.")

arduino.close()