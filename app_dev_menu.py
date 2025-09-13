from tkinter import *
from tkinter import font

root = Tk()
root.title("Main Menu")
root.geometry("400x500")
root.configure(bg="#1e1e1e")

title_font = font.Font(family="Arial Black", size=20, weight="bold")
button_font = font.Font(family="Arial Black", size=12)

title_label = Label(root, text="Main Menu", font=title_font, bg="#1e1e1e", fg="white")
title_label.pack(pady=30)

button_style = {
    "font": button_font,
    "bg": "#00bfff",
    "fg": "black",
    "activebackground": "#1ca9c9",
    "activeforeground": "white",
    "relief": "flat",
    "width": 25,
    "height":2
}

buttons = [
    "TMS APPLICATION",
    "HUMIDITY & TEMPERATURE",
    "LOCK / UNLOCK SYSTEM",
    "ITEM DETECTOR SYSTEM", 
    "DISTANCE MEASURE SYSTEM"
]

for text in buttons:
    btn = Button(root, text=text, **button_style)
    btn.pack(pady=10)

root.mainloop()