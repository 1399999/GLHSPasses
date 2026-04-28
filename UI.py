import tkinter as tk
import time

class UI():
    global root, start, length, T

    def __init__(self):
        root = tk.Tk()
        root.title("Input Taker")
        root.geometry("300x300")
        self.start = 0.0
        self.length = 0.0

        greeting = tk.Label(text="Enter student ID:")
        greeting.pack(pady=20)

        T = tk.Text(root, height = 1, width = 10)

        b1 = tk.Button(root, text = "Submit, Start Time", command = self.Take_input)
        b2 = tk.Button(root, text = "End Time", command = self.Take_output)

        greeting2 = tk.Label(text="Time: " + str(length))
        greeting3 = tk.Label(text="Output: " + str(length))

        T.pack()
        b1.pack(pady=20)
        b2.pack(pady=10)
        greeting2.pack(pady=20)
        greeting3.pack(pady=20)

        root.mainloop()

    def Take_input(self):
        self.start = time.time()

    def Take_output(self):
        self.end = time.time()
        self.length = self.end - self.start
        self.greeting2.config(text="Time: " + str(self.length))
        self.greeting3.config(text="Output: " + self.T.get("1.0",tk.END))

        self.studentID = self.T.get("1.0",tk.END).strip()
        self.timeElpased = str(self.length)

        self.root.destroy()
    