from tkinter import *
from tkinter import ttk
from random import shuffle

root = Tk()
root.title("BS COMPUTER SCIENCE")
root.geometry("500x150")

label = ttk.Label(root, text="BS5AA", font=("Arial", 10, "bold"), wraplength=150)
label.pack()

def answer():
    answer_list = ["Single", "Married", "Widowed"]
    shuffle(answer_list)
    sagot = answer_list.pop()
    label.config(text=sagot)

def answer1():
    answer1_list = ["Male", "Female"]
    shuffle(answer1_list)
    sagot1 = answer1_list.pop()
    label.config(text=sagot1)

btn = Button(root, text="Civil Status")
btn1 = Button(root, text="Gender")

btn.pack()
btn1.pack()

btn.config(command=answer)
btn1.config(command=answer1)

root.mainloop()
