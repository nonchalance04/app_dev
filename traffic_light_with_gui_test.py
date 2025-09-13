from tkinter import *
import serial
import time

arduino = serial.Serial(port="/dev/ttyACM0")
time.sleep(2)

root = Tk()
root.title("Traffic Light GUI")

# Functions
def reset_lights():
    canvas.itemconfig(red_light, fill="gray")
    canvas.itemconfig(yellow_light, fill="gray")
    canvas.itemconfig(green_light, fill="gray")

def turn_red():
    reset_lights()
    canvas.itemconfig(red_light, fill="red")
    arduino.write("r".encode())

def turn_yellow():
    reset_lights()
    canvas.itemconfig(yellow_light, fill="yellow")
    arduino.write("y".encode())                                                                                                                                  

def turn_green():
    reset_lights()
    canvas.itemconfig(green_light, fill="green")
    arduino.write("g".encode())

title = Label(root, text="Traffic Monitoring System (TMS)" ,font=("Arial", 22), padx=10, pady=10)
title.pack(pady=10)

light_frame = Frame(root)
light_frame.pack(side="left", pady=20, padx=(30,0))

canvas = Canvas(light_frame, width=100, height=260, bg="black")
canvas.pack()


# Create 3 lights(circles)
red_light = canvas.create_oval(20,20,80,80, fill="gray")
yellow_light = canvas.create_oval(20,100,80,160, fill="gray")
green_light = canvas.create_oval(20, 180, 80, 240, fill="gray")

# Frame for buttons (right side)
button_frame = Frame(root, padx=20, pady=20)
button_frame.pack(side="right")

red_button = Button(button_frame, text="Red", width=10, pady=10 ,command=turn_red)
yellow_button = Button(button_frame, text="Yellow", width=10, pady=10 ,command=turn_yellow)
green_button = Button(button_frame, text="Green", width=10, pady=10 ,command=turn_green)
red_button.pack(pady=10, padx=(0,20))
yellow_button.pack(pady=10, padx=(0,20))
green_button.pack(pady=10, padx=(0,20))




root.mainloop()

