import tkinter as tk
from tkinter import messagebox

def run_timer(t):
    if t >= 0:
        txtoutput.delete("1.0", tk.END)
        txtoutput.insert(tk.END, str(t))

        if t == 0:
            print("Time up!")
            return

        root.after(1000, run_timer, t - 2)  # count by 2

def timer():
    try:
        insert = int(txtinsert.get())

        if insert < 0:
            messagebox.showinfo("Error", "Enter a positive number")
            return

        # 👉 Make sure it starts from an even number
        if insert % 2 != 0:
            insert -= 1   # convert odd → even

        run_timer(insert)

    except ValueError:
        messagebox.showinfo("Error", "Please enter a valid number")

# GUI
root = tk.Tk()
root.title("Timer")

tk.Label(root, text="Enter time:").grid(row=0, column=0, padx=5, pady=10)

txtinsert = tk.Entry(root)
txtinsert.grid(row=0, column=1, padx=5, pady=10)

tk.Button(root, text="Start Timer", command=timer).grid(row=1, column=0, columnspan=2, pady=10)

txtoutput = tk.Text(root, height=5, width=20)
txtoutput.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()