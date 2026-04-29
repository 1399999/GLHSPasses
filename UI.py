import tkinter as tk
from tkinter import filedialog
import time
import qrcode

class UI:

    # root = None
    # time_str = None
    # greeting2 = None

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Input Taker")
        self.root.geometry("300x300")

        self.old_btn = tk.Button(self.root, text = "Old Functionality", command = self.Old_func)
        self.new_btn = tk.Button(self.root, text = "New Functionality", command = self.New_func)

        self.old_btn.pack(pady=20)
        self.new_btn.pack(pady=20)
        
        self.is_old_window = None
        
        self.root.mainloop()

    def Take_input(self):
        self.start = time.time()

    def Old_func(self):
        self.is_old_window = True

        self.old_window = tk.Toplevel(self.root)
        self.old_window.title("Old")
        self.old_window.geometry("300x200")

        self.start = 0.0
        self.length = 0.0

        self.greeting = tk.Label(self.old_window, text="Enter student ID:")
        self.greeting.pack(pady=20)

        self.T = tk.Text(self.old_window, height = 1, width = 10)

        self.b1 = tk.Button(self.old_window, text = "Submit, Start Time", command = self.Take_input)
        self.b2 = tk.Button(self.old_window, text = "End Time", command = self.Take_output)

        self.greeting2 = tk.Label(self.old_window, text="Time: " + str(self.length))
        self.greeting3 = tk.Label(self.old_window, text="Output: " + str(self.length))

        self.T.pack()
        self.b1.pack(pady=20)
        self.b2.pack(pady=10)
        self.greeting2.pack(pady=20)
        self.greeting3.pack(pady=20)

    def New_func(self):
        self.is_old_window = False

        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("New")
        self.new_window.geometry("300x200")

        button = tk.Button(self.new_window, text='Open File', command=self.upload_action)
        self.T2 = tk.Label(self.new_window, height = 1, width = 100)
        self.T3 = tk.Label(self.new_window, height = 40, width = 100)

        button.pack()
        self.T2.pack(pady=20)
        self.T3.pack(pady=20)

    def Take_output(self):
        self.end = time.time()
        self.length = self.end - self.start
        self.greeting2.config(text="Time: " + str(self.length))
        self.greeting3.config(text="Output: " + self.T.get("1.0",tk.END))

        self.studentID = self.T.get("1.0",tk.END).strip()
        self.timeElpased = str(self.length)

        self.root.destroy()

    def upload_action(self, event=None):
        filename = filedialog.askopenfilename()
        self.T2.config(text="Selected: " + self.format_path(filename))

        self.lines = []

        with open(filename, 'r') as file:
            for line in file:
                self.lines.append(line.strip())
                self.T3.config(text=self.T3['text'] + line.strip() + "\n")

        for i in range(len(self.lines)):

            img = qrcode.make(self.lines[i])
            img.save(f"H:/QRCodeDump/{self.lines[i]}.png")

    def format_path(self, filename):
        if filename[:2] == "//":
            return "H:/" + "/".join(filename.split("/")[9:])
        else:
            return filename
    