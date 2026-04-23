import tkinter as tk
import time

root = tk.Tk()
root.title("Input Taker")
root.geometry("300x200")

start = 0.0
length = 0.0

def Take_input():
    global start
    start = time.time()

def Take_output():
    end = time.time()
    length = end - start
    greeting2.config(text=str(length))

greeting = tk.Label(text="Enter your student ID:")
greeting.pack(pady=20)

T = tk.Text(root, height = 1, width = 10)

b1 = tk.Button(root, text = "Time Start", command = Take_input)
b2 = tk.Button(root, text = "Time End", command = Take_output)

greeting2 = tk.Label(text=length)

T.pack()
b1.pack(pady=20)
b2.pack(pady=10)
greeting2.pack(pady=20)

root.mainloop()
