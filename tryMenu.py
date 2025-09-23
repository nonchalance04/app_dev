from tkinter import Tk, Frame, Label, Entry, Button
from tms import create_main_window



def open_menu():
    menu = Tk()
    menu.title("Main Menu")
    menu.geometry("400x500")
    menu.configure(bg="#1a1a1a")

    Label(menu, text="MAIN MENU", font=("Arial Black", 20, "bold"), fg="white", bg="#1a1a1a").pack(pady=30)

    def app1():
        menu.destroy()
        create_main_window()

    def app2():
        print("HUMIDITY & TEMPERATURE")
    def app3():
        print("LOCK / UNLOCK SYSTEM")
    def app4():
        print("ITEM DETECTOR SYSTEM")
    def app5():
        print("DISTANCE MEASURE SYSTEM")

    # Dictionary corresponds to APP_NAME:APP_FUNCTION
    buttons = {
        "TMS APPLICATION":app1,
        "HUMIDITY & TEMPERATURE":app2,
        "LOCK / UNLOCK SYSTEM":app3,
        "ITEM DETECTOR SYSTEM":app4,
        "DISTANCE MEASURE SYSTEM":app5
    }



    for b, apps in buttons.items():
        Button(menu, text=b, font=("Arial", 12, "bold"), bg="#00bfff", fg="black", width=25, height=2, bd=4, command=apps).pack(pady=10)

    def close_window():
        menu.destroy()

    menu.protocol("WM_DELETE_WINDOW", close_window)

    menu.mainloop()



def show_login():
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

    def login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "manginasal" and password == "chickenjoy123":
            root.destroy()  
            open_menu()      
        else:
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

    Button(frame, text="Login", font=("Arial", 12), width=10, bg="Green", fg="white", command=login).grid(row=2, column=1)
    Button(frame, text="Cancel", font=("Arial", 12), width=10, bg="Red", fg="white", command=root.quit).grid(row=2, column=2)

    # root.mainloop()


    button_cancel = Button(frame, padx=10, pady=10, text="Cancel", font=("Arial", 12),
                        width=10, bg="Red", fg="white", command=root.quit)
    button_cancel.grid(row=2, column=2)
    root.mainloop()

if __name__ == "__main__":
    show_login()
