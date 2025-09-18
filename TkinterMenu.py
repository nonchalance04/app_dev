import tkinter as tk

def action(name):
    print(f"{name} Selected")

root = tk.Tk()
root.title("Main Menu")
root.geometry("400x500")
root.configure(bg="#1a1a1a")


tk.Label(root, text="MAIN MENU", font=("Arial Black", 20, "bold"),
         fg="white", bg="#1a1a1a").pack(pady=30)

button_style = {"font": ("Arial", 12, "bold"), "bg": "#00bfff",
                "fg": "black", "width": 25, "height": 2, "bd": 4}


buttons = [
    "TMS APPLICATION",
    "HUMIDITY & TEMPERATURE",
    "LOCK / UNLOCK SYSTEM",
    "ITEM DETECTOR SYSTEM",
    "DISTANCE MEASURE SYSTEM"
]

for b in buttons:
    tk.Button(root, text=b, command=lambda x=b: action(x), **button_style).pack(pady=10)

root.mainloop()
