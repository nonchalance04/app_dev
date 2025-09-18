from tkinter import Tk, Frame, Label, Entry, Button

def open_menu():
    menu = Tk()
    menu.title("Main Menu")
    menu.geometry("400x500")
    menu.configure(bg="#1a1a1a")

    Label(menu, text="MAIN MENU", font=("Arial Black", 20, "bold"), fg="white", bg="#1a1a1a").pack(pady=30)

    buttons = [
        "TMS APPLICATION",
        "HUMIDITY & TEMPERATURE",
        "LOCK / UNLOCK SYSTEM",
        "ITEM DETECTOR SYSTEM",
        "DISTANCE MEASURE SYSTEM"
    ]

    for b in buttons:
        Button(menu, text=b, font=("Arial", 12, "bold"), bg="#00bfff", fg="black", width=25, height=2, bd=4).pack(pady=10)

    menu.mainloop()

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "manginasal" and password == "chickenjoy123":
        root.destroy()  
        open_menu()      
    else:
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')

root = Tk()
root.title("Login Form")
root.geometry("500x150")

frame = Frame(root, width=300, height=250)
frame.pack(padx=10, pady=10)

Label(frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
username_entry = Entry(frame, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

Label(frame, text="Password").grid(row=1, column=0, padx=10, pady=10)
password_entry = Entry(frame, width=30, font=("Arial", 12), show="*")
password_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

Button(frame, text="Login", font=("Arial", 12), width=10, bg="Green", fg="white", command=login).grid(row=2, column=1)
Button(frame, text="Cancel", font=("Arial", 12), width=10, bg="Red", fg="white", command=root.quit).grid(row=2, column=2)

root.mainloop()


button_cancel = Button(frame, padx=10, pady=10, text="Cancel", font=("Arial", 12),
                       width=10, bg="Red", fg="white", command=root.quit)
button_cancel.grid(row=2, column=2)

root.mainloop()
