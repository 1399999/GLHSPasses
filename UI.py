import tkinter as tk
import time

class UI:

    # root = None
    # time_str = None
    # greeting2 = None

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Input Taker")
        self.root.geometry("300x300")
        self.start = 0.0
        self.length = 0.0

        self.greeting = tk.Label(text="Enter student ID:")
        self.greeting.pack(pady=20)

        self.T = tk.Text(self.root, height = 1, width = 10)

        self.b1 = tk.Button(self.root, text = "Submit, Start Time", command = self.Take_input)
        self.b2 = tk.Button(self.root, text = "End Time", command = self.Take_output)

        self.greeting2 = tk.Label(text="Time: " + str(self.length))
        self.greeting3 = tk.Label(text="Output: " + str(self.length))

        self.T.pack()
        self.b1.pack(pady=20)
        self.b2.pack(pady=10)
        self.greeting2.pack(pady=20)
        self.greeting3.pack(pady=20)

        self.root.mainloop()

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
    