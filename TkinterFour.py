from tkinter import Tk, Frame, Label, Entry, Button

root = Tk()
root.title("Login Form")
root.geometry("500x150")

frame = Frame(root, width=300, height=250)
frame.pack(padx=10, pady=10)

username_label = Label(frame, text="Username")
username_label.grid(row=0, column=0, padx=10, pady=10)

username_entry = Entry(frame, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

password_label = Label(frame, text="Password")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = Entry(frame, width=30, font=("Arial", 12), show="*")
password_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

button_ok = Button(frame, padx=10, pady=10, text="Login", font=("Arial", 12),
                   width=10, bg="Green", fg="white")
button_ok.grid(row=2, column=1)

button_cancel = Button(frame, padx=10, pady=10, text="Cancel", font=("Arial", 12),
                       width=10, bg="Red", fg="white")
button_cancel.grid(row=2, column=2)

root.mainloop()
